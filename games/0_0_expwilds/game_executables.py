"""Executables related to updating expanding wilds and collecting prize values."""

import random
from copy import deepcopy
from game_calculations import GameCalculations
from src.calculations.statistics import get_random_outcome


class GameExecutables(GameCalculations):
    """Executable functions used for expanding wild game."""

    def update_with_existing_wilds(self) -> None:
        """Replace drawn boards with existing sticky-wilds with enhanced mechanics."""
        updated_exp_wild = []
        for expwild in self.expanding_wilds:
            # Enhanced multiplier system - progressive increases
            current_mult = expwild.get("mult", 2)
            # Progressive multiplier enhancement during free spins
            if self.gametype == self.config.freegame_type and hasattr(self, 'current_fs') and self.current_fs > 1:
                # Increase multiplier by 1x every 2 spins, max 10x
                mult_increase = min((self.current_fs - 1) // 2, 8)
                new_mult_on_reveal = current_mult + mult_increase
            else:
                new_mult_on_reveal = get_random_outcome(
                    self.get_current_distribution_conditions()["mult_values"][self.gametype]
                )
            
            expwild["mult"] = new_mult_on_reveal
            updated_exp_wild.append({"reel": expwild["reel"], "row": 0, "mult": new_mult_on_reveal})
            
            # Enhanced wild expansion - can create mega wilds
            for row, _ in enumerate(self.board[expwild["reel"]]):
                if new_mult_on_reveal >= 50:  # Mega wild threshold
                    self.board[expwild["reel"]][row] = self.create_symbol("MW")  # Mega Wild
                    self.board[expwild["reel"]][row].assign_attribute({"multiplier": new_mult_on_reveal})
                else:
                    self.board[expwild["reel"]][row] = self.create_symbol("W")
                    self.board[expwild["reel"]][row].assign_attribute({"multiplier": new_mult_on_reveal})

    def assign_new_wilds(self, max_num_new_wilds: int):
        """Assign unused reels to have sticky symbol."""
        self.new_exp_wilds = []
        for _ in range(max_num_new_wilds):
            if len(self.avaliable_reels) > 0:
                chosen_reel = random.choice(self.avaliable_reels)
                chosen_row = random.choice([i for i in range(self.config.num_rows[chosen_reel])])
                self.avaliable_reels.remove(chosen_reel)

                wr_mult = get_random_outcome(
                    self.get_current_distribution_conditions()["mult_values"][self.gametype]
                )
                expwild_details = {"reel": chosen_reel, "row": chosen_row, "mult": wr_mult}
                self.board[expwild_details["reel"]][expwild_details["row"]] = self.create_symbol("W")
                self.board[expwild_details["reel"]][expwild_details["row"]].assign_attribute(
                    {"multiplier": wr_mult}
                )
                self.new_exp_wilds.append(expwild_details)

    # Superspin prize modes
    def check_for_new_prize(self) -> list:
        """Check for prizes landing on most recent reveal."""
        new_sticky_symbols = []
        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                if (
                    self.board[reel][row].check_attribute("prize")
                    and (reel, row) not in self.existing_sticky_symbols
                ):
                    sym_details = {
                        "reel": reel,
                        "row": row,
                        "prize": self.board[reel][row].get_attribute("prize"),
                    }
                    new_sticky_symbols.append(sym_details)
                    self.sticky_symbols.append(deepcopy(sym_details))
                    self.existing_sticky_symbols.append((sym_details["reel"], sym_details["row"]))

        return new_sticky_symbols

    def replace_board_with_stickys(self) -> None:
        """replace with stickys and update special array."""
        for sym in self.sticky_symbols:
            self.board[sym["reel"]][sym["row"]] = self.create_symbol("P")
            self.board[sym["reel"]][sym["row"]].assign_attribute({"prize": sym["prize"]})

    def get_final_board_prize(self) -> dict:
        """Get final board win."""
        total_win = 0.0
        winning_pos = []
        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                if self.board[reel][row].check_attribute("prize"):
                    total_win += self.board[reel][row].get_attribute("prize")
                    winning_pos.append(
                        {"reel": reel, "row": row, "value": self.board[reel][row].get_attribute("prize")},
                    )

        return_data = {"totalWin": total_win, "wins": winning_pos}
        return return_data

    # Premium Cascading Mechanics
    def premium_cascade_check(self) -> bool:
        """Check if cascade should trigger based on premium conditions."""
        if self.gametype == self.config.freegame_type:
            # Enhanced cascade chance in free spins
            return self.win_data["totalWin"] > 0 and random.random() < 0.3  # 30% cascade chance
        else:
            # Standard cascade in base game
            return self.win_data["totalWin"] > 5  # Cascade on wins > 5x

    def execute_premium_cascade(self) -> None:
        """Execute premium cascade with enhanced features."""
        if not self.premium_cascade_check():
            return
            
        # Remove winning symbols and apply gravity
        self.remove_winning_symbols()
        self.apply_symbol_gravity()
        self.fill_empty_positions()
        
        # Add cascade multiplier progression
        if not hasattr(self, 'cascade_multiplier'):
            self.cascade_multiplier = 1
        self.cascade_multiplier = min(self.cascade_multiplier + 1, 5)  # Max 5x cascade multiplier
        
        # Apply cascade multiplier to subsequent wins
        if hasattr(self, 'win_data') and self.win_data.get("totalWin", 0) > 0:
            self.win_data["totalWin"] *= self.cascade_multiplier

    def remove_winning_symbols(self) -> None:
        """Remove symbols that contributed to wins."""
        if not hasattr(self, 'winning_positions'):
            return
            
        for pos in self.winning_positions:
            reel, row = pos
            # Replace with special cascade symbol temporarily
            self.board[reel][row] = self.create_symbol("X")

    def apply_symbol_gravity(self) -> None:
        """Apply gravity effect to make symbols fall down."""
        for reel_idx in range(self.config.num_reels):
            # Collect non-empty symbols from bottom to top
            reel_symbols = []
            for row_idx in range(self.config.num_rows[reel_idx] - 1, -1, -1):
                symbol = self.board[reel_idx][row_idx]
                if symbol.name != "X":  # Not empty/cascaded
                    reel_symbols.append(symbol)
            
            # Fill from bottom with existing symbols
            for row_idx in range(self.config.num_rows[reel_idx] - 1, -1, -1):
                if reel_symbols:
                    self.board[reel_idx][row_idx] = reel_symbols.pop(0)
                else:
                    self.board[reel_idx][row_idx] = self.create_symbol("X")

    def fill_empty_positions(self) -> None:
        """Fill empty positions with new symbols."""
        for reel_idx in range(self.config.num_reels):
            for row_idx in range(self.config.num_rows[reel_idx]):
                if self.board[reel_idx][row_idx].name == "X":
                    # Draw new symbol from reel strip
                    new_symbol = self.draw_symbol_from_reel(reel_idx)
                    self.board[reel_idx][row_idx] = new_symbol

    def draw_symbol_from_reel(self, reel_idx: int):
        """Draw a new symbol from the appropriate reel strip."""
        reel_weights = self.get_current_distribution_conditions().get("reel_weights", {})
        current_reel_set = reel_weights.get(self.gametype, {})
        
        # Default to base reel if no specific reel set
        if not current_reel_set:
            current_reel_set = {"BR0": 1}
            
        reel_name = get_random_outcome(current_reel_set)
        reel_strip = self.config.reels[reel_name][reel_idx]
        
        # Random position on reel strip
        symbol_name = random.choice(reel_strip)
        return self.create_symbol(symbol_name)

    # Enhanced Wild Assignment with Progressive Features
    def enhanced_wild_assignment(self, max_num_new_wilds: int):
        """Enhanced wild assignment with progressive features."""
        if not hasattr(self, 'wild_progression_level'):
            self.wild_progression_level = 0
            
        # Progressive wild enhancement based on free spin count
        if self.gametype == self.config.freegame_type and hasattr(self, 'current_fs'):
            bonus_wilds = min(self.current_fs // 3, 2)  # Bonus wilds every 3 spins
            max_num_new_wilds += bonus_wilds
            
        self.assign_new_wilds(max_num_new_wilds)

    # Premium Anticipation System
    def trigger_premium_anticipation(self) -> bool:
        """Enhanced anticipation system for premium feel."""
        scatter_count = self.count_special_symbols("scatter")
        
        if scatter_count == 2:
            # 2 scatters - premium anticipation with enhanced effects
            self.anticipation = "premium_tease"
            return True
        elif scatter_count == 1 and random.random() < 0.15:
            # 1 scatter - subtle anticipation
            self.anticipation = "subtle_tease" 
            return True
        
        return False
