"""Executables related to updating expanding wilds and collecting prize values."""

import random
from copy import deepcopy
from game_calculations import GameCalculations
from src.calculations.statistics import get_random_outcome


class GameExecutables(GameCalculations):
    """Executable functions used for expanding wild game."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize collection meter and Dragon's Fury state
        self.collection_meter = 0
        self.dragons_fury_active = False
        self.dragons_lair_respins = 0

    def update_with_existing_wilds(self) -> None:
        """Replace drawn boards with existing sticky-wilds with enhanced mechanics."""
        updated_exp_wild = []
        for expwild in self.expanding_wilds:
            # Enhanced multiplier system - progressive increases
            current_mult = expwild.get("mult", 2)
            
            # Check if this is a center reel wild (reels 2, 3, 4) for multiplier enhancement
            if expwild["reel"] in self.config.multiplier_wild_reels:
                # Apply Dragon Wild multiplier (2x or 3x) for center reels
                dragon_mult = get_random_outcome(self.config.multiplier_wild_values)
                new_mult_on_reveal = current_mult * dragon_mult
            else:
                # Progressive multiplier enhancement during free spins for other reels
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

                # Check if this is a center reel for Dragon Wild multiplier
                if chosen_reel in self.config.multiplier_wild_reels:
                    # Apply Dragon Wild multiplier (2x or 3x) for center reels
                    dragon_mult = get_random_outcome(self.config.multiplier_wild_values)
                    wr_mult = 2 * dragon_mult  # Base 2x multiplied by dragon multiplier
                else:
                    # Standard multiplier for other reels
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

    # Gold Coin Collection and Dragon's Lair Mechanics
    def check_for_gold_coins(self) -> int:
        """Check for Gold Coin symbols and update collection meter."""
        gold_coins_found = 0
        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                if self.board[reel][row].name == "GC":
                    gold_coins_found += 1
        
        # Update collection meter
        self.collection_meter += gold_coins_found
        
        # Cap at maximum
        if self.collection_meter > self.config.collection_meter_max:
            self.collection_meter = self.config.collection_meter_max
            
        return gold_coins_found

    def check_dragons_lair_trigger(self) -> bool:
        """Check if collection meter is full to trigger Dragon's Lair."""
        return self.collection_meter >= self.config.collection_meter_max

    def trigger_dragons_lair(self) -> None:
        """Initialize Dragon's Lair hold-and-win bonus."""
        # Reset collection meter
        self.collection_meter = 0
        
        # Initialize Dragon's Lair state
        self.dragons_lair_respins = self.config.dragons_lair_initial_spins
        
        # Switch to Dragon's Lair game mode
        self.gametype = self.config.dragons_lair_type
        
        # Initialize empty board for hold-and-win
        self.initialize_dragons_lair_board()

    def initialize_dragons_lair_board(self) -> None:
        """Create empty board for Dragon's Lair bonus."""
        for reel in range(self.config.num_reels):
            for row in range(self.config.num_rows[reel]):
                self.board[reel][row] = self.create_symbol("X")

    def execute_dragons_lair_spin(self) -> dict:
        """Execute a single Dragon's Lair re-spin."""
        # Draw new symbols for empty positions
        self.fill_empty_dragons_lair_positions()
        
        # Check for new prize symbols
        new_prizes = self.check_for_new_prize()
        
        # If new prizes found, reset re-spins
        if new_prizes:
            self.dragons_lair_respins = self.config.dragons_lair_initial_spins
        else:
            self.dragons_lair_respins -= 1
        
        # Check if bonus should end
        if self.dragons_lair_respins <= 0:
            return self.end_dragons_lair()
        
        return {"continue": True, "respins_left": self.dragons_lair_respins}

    def fill_empty_dragons_lair_positions(self) -> None:
        """Fill empty positions in Dragon's Lair with new symbols."""
        reel_weights = self.get_current_distribution_conditions().get("reel_weights", {})
        current_reel_set = reel_weights.get(self.gametype, {"DLR0": 1})
        reel_name = get_random_outcome(current_reel_set)
        
        for reel_idx in range(self.config.num_reels):
            for row_idx in range(self.config.num_rows[reel_idx]):
                if self.board[reel_idx][row_idx].name == "X":
                    # Draw new symbol from Dragon's Lair reel strip
                    reel_strip = self.config.reels[reel_name][reel_idx]
                    symbol_name = random.choice(reel_strip)
                    new_symbol = self.create_symbol(symbol_name)
                    
                    # If it's a prize symbol, assign random prize value
                    if symbol_name == "P":
                        prize_values = self.get_current_distribution_conditions().get("prize_values", {1: 1000})
                        prize_value = get_random_outcome(prize_values)
                        new_symbol.assign_attribute({"prize": prize_value})
                    
                    self.board[reel_idx][row_idx] = new_symbol

    def end_dragons_lair(self) -> dict:
        """End Dragon's Lair bonus and calculate final win."""
        final_win_data = self.get_final_board_prize()
        
        # Check for jackpot (full screen of prizes)
        total_positions = sum(self.config.num_rows)
        prize_positions = len(final_win_data["wins"])
        
        if prize_positions >= total_positions * 0.8:  # 80% or more filled
            final_win_data["jackpot"] = True
            
        # Reset game state
        self.gametype = self.config.basegame_type
        
        return final_win_data

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

    # Dragon's Fury Random Event System
    def check_dragons_fury_trigger(self) -> bool:
        """Check if Dragon's Fury should trigger on non-winning spin."""
        # Only trigger on non-winning spins in base game
        if (self.gametype == self.config.basegame_type and 
            self.win_data.get("totalWin", 0) == 0 and 
            random.random() < self.config.dragons_fury_trigger_chance):
            return True
        return False

    def execute_dragons_fury(self) -> dict:
        """Execute Dragon's Fury random event."""
        # Randomly choose between two outcomes
        fury_outcome = random.choice(["symbol_cluster", "gold_coins"])
        
        if fury_outcome == "symbol_cluster":
            return self.add_high_paying_cluster()
        else:
            return self.add_gold_coin_cluster()

    def add_high_paying_cluster(self) -> dict:
        """Add cluster of high-paying symbols to guarantee a win."""
        # Choose a high-paying symbol
        high_symbols = ["H1", "H2", "H3", "H4"]  # Dragons, Phoenix, Unicorn, Griffin
        chosen_symbol = random.choice(high_symbols)
        
        # Choose a random starting position
        start_reel = random.randint(0, 2)  # Start from reel 0, 1, or 2
        start_row = random.randint(0, 3)   # Start from row 0, 1, 2, or 3
        
        # Create cluster (2x2 or 3x2 pattern)
        cluster_positions = []
        cluster_size = random.choice([4, 6])  # 2x2 or 3x2
        
        for i in range(2):  # 2 reels wide
            for j in range(cluster_size // 2):  # 2 or 3 rows tall
                reel_pos = start_reel + i
                row_pos = start_row + j
                
                # Ensure within bounds
                if (reel_pos < self.config.num_reels and 
                    row_pos < self.config.num_rows[reel_pos]):
                    self.board[reel_pos][row_pos] = self.create_symbol(chosen_symbol)
                    cluster_positions.append((reel_pos, row_pos))
        
        return {
            "event": "dragons_fury_symbols",
            "symbol": chosen_symbol,
            "positions": cluster_positions
        }

    def add_gold_coin_cluster(self) -> dict:
        """Add multiple Gold Coin symbols to boost collection meter."""
        coin_count = random.randint(3, 6)  # 3-6 gold coins
        coin_positions = []
        
        # Choose random positions for gold coins
        available_positions = []
        for reel in range(self.config.num_reels):
            for row in range(self.config.num_rows[reel]):
                available_positions.append((reel, row))
        
        # Randomly select positions for coins
        selected_positions = random.sample(available_positions, min(coin_count, len(available_positions)))
        
        for reel, row in selected_positions:
            self.board[reel][row] = self.create_symbol("GC")
            coin_positions.append((reel, row))
        
        # Update collection meter
        self.collection_meter += len(coin_positions)
        if self.collection_meter > self.config.collection_meter_max:
            self.collection_meter = self.config.collection_meter_max
        
        return {
            "event": "dragons_fury_coins",
            "coin_count": len(coin_positions),
            "positions": coin_positions,
            "collection_meter": self.collection_meter
        }

    # Multiplier Stacking for Multiple Wilds
    def calculate_payline_multiplier(self, payline_positions: list) -> float:
        """Calculate total multiplier for a payline with multiple wilds."""
        total_multiplier = 1.0
        
        for reel, row in payline_positions:
            symbol = self.board[reel][row]
            if symbol.name in ["W", "MW"] and symbol.check_attribute("multiplier"):
                wild_multiplier = symbol.get_attribute("multiplier")
                total_multiplier *= wild_multiplier
        
        return total_multiplier

    def apply_multiplier_to_win(self, win_data: dict, payline_positions: list) -> dict:
        """Apply multiplier stacking to win amount."""
        if not win_data or win_data.get("totalWin", 0) == 0:
            return win_data
        
        payline_multiplier = self.calculate_payline_multiplier(payline_positions)
        
        if payline_multiplier > 1.0:
            win_data["totalWin"] *= payline_multiplier
            win_data["multiplier_applied"] = payline_multiplier
        
        return win_data
