"""Template game configuration file, detailing required user-specified inputs."""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode


class GameConfig(Config):
    """Template configuration class."""

    def __init__(self):
        super().__init__()
        self.game_id = "0_0_expwilds"
        self.provider_number = 0
        self.working_name = "Premium Dragon Wilds"  # Premium branding
        self.wincap = 10000  # Increased win cap for premium appeal
        self.win_type = "lines"
        self.rtp = 0.96  # Standard RTP for premium games
        
        # Add Dragons Lair game type
        self.dragons_lair_type = "dragons_lair"
        
        self.construct_paths()

        # Game Dimensions - Enhanced premium setup
        self.num_reels = 5
        self.num_rows = [5] * self.num_reels  # Optionally include variable number of rows per reel
        
        # Enhanced Paytable with better premium payouts
        self.paytable = {
            # Premium Wild pays (enhanced)
            (5, "W"): 50,  # Increased from 20
            (4, "W"): 25,  # Increased from 10  
            (3, "W"): 10,  # Increased from 5
            # High symbols - premium fantasy theme
            (5, "H1"): 40,  # Dragon - premium symbol
            (4, "H1"): 20,
            (3, "H1"): 8,
            (5, "H2"): 30,  # Phoenix 
            (4, "H2"): 15,
            (3, "H2"): 6,
            (5, "H3"): 25,  # Unicorn
            (4, "H3"): 12,
            (3, "H3"): 5,
            (5, "H4"): 20,  # Griffin
            (4, "H4"): 10,
            (3, "H4"): 4,
            # Medium symbols - gems/crystals
            (5, "M1"): 15,  # Ruby
            (4, "M1"): 6,
            (3, "M1"): 2,
            (5, "M2"): 12,  # Emerald
            (4, "M2"): 5,
            (3, "M2"): 1.5,
            # Low symbols - enhanced values
            (5, "L1"): 8,
            (4, "L1"): 3,
            (3, "L1"): 1,
            (5, "L2"): 6,
            (4, "L2"): 2,
            (3, "L2"): 0.8,
            (5, "L3"): 5,
            (4, "L3"): 1.5,
            (3, "L3"): 0.6,
            # Gold Coin - Collection symbol
            (99, "GC"): 0,  # Triggers collection, no line pay
            (99, "X"): 0,  # only included for symbol register
        }
        # Enhanced Paylines - 25 premium paylines for better hit frequency
        self.paylines = {
            # Horizontal lines
            1: [0, 0, 0, 0, 0],
            2: [1, 1, 1, 1, 1],
            3: [2, 2, 2, 2, 2],
            4: [3, 3, 3, 3, 3],
            5: [4, 4, 4, 4, 4],
            # Zigzag patterns 
            6: [0, 1, 0, 1, 0],
            7: [1, 2, 1, 2, 1],
            8: [2, 3, 2, 3, 2],
            9: [3, 4, 3, 4, 3],
            10: [1, 0, 1, 0, 1],
            11: [2, 1, 2, 1, 2],
            12: [3, 2, 3, 2, 3],
            13: [4, 3, 4, 3, 4],
            # Diagonal lines
            14: [0, 1, 2, 3, 4],
            15: [4, 3, 2, 1, 0],
            # V-shaped patterns
            16: [0, 1, 2, 1, 0],
            17: [1, 2, 3, 2, 1],
            18: [2, 3, 4, 3, 2],
            19: [4, 3, 2, 3, 4],
            20: [3, 2, 1, 2, 3],
            # Additional premium patterns
            21: [0, 2, 1, 2, 0],
            22: [1, 3, 2, 3, 1],
            23: [2, 4, 3, 4, 2],
            24: [0, 1, 3, 1, 0],
            25: [4, 2, 1, 2, 4],
        }
        self.include_padding = True
        
        # Enhanced Special Symbols for premium features
        self.special_symbols = {
            "wild": ["W"],
            "scatter": ["S"],
            "multiplier": ["W"],
            "prize": ["P"],
            "bonus": ["B"],  # New bonus symbol
            "mega_wild": ["MW"],  # New mega wild 
            "gold_coin": ["GC"],  # New Gold Coin symbol for Hoard Collection
        }

        # Enhanced Free Spin System with progressive triggers
        self.freespin_triggers = {
            self.basegame_type: {3: 10, 4: 15, 5: 20},  # Enhanced free spins
            self.freegame_type: {3: 5, 4: 8, 5: 12}  # Retriggers enabled
        }
        
        # Enhanced Anticipation mechanics for premium feel
        self.anticipation_triggers = {
            self.basegame_type: min(self.freespin_triggers[self.basegame_type].keys()) - 1,
        }
        
        # Dragon's Hoard Collection Feature Settings
        self.collection_meter_max = 15  # Gold coins needed to trigger Dragon's Lair
        self.dragons_lair_initial_spins = 3  # Starting re-spins in bonus
        self.dragons_fury_trigger_chance = 0.08  # 8% chance on non-winning spins
        
        # Multiplier Wilds Configuration (reels 2, 3, 4 only)
        self.multiplier_wild_reels = [1, 2, 3]  # 0-indexed reels 2, 3, 4
        self.multiplier_wild_values = {2: 0.7, 3: 0.3}  # 70% chance 2x, 30% chance 3x
        # Enhanced Reels with premium symbol distribution
        reels = {
            "BR0": "BR0.csv",      # Original base reel
            "PBR0": "PBR0.csv",    # Premium base reel with better symbol distribution
            "FR0": "FR0.csv",      # Original free reel
            "PFR0": "PFR0.csv",    # Premium free reel with enhanced features
            "SSR": "SSR.csv",      # Superspin reel
            "SSWCAP": "SSWCAP.csv", # Superspin wincap reel
            "DLR0": "DLR0.csv",    # Dragon's Lair bonus reel
        }
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(os.path.join(self.reels_path, f))

        # Enhanced reel assignments for premium experience
        self.padding_reels = {
            "basegame": self.reels["PBR0"],    # Use premium base reel
            "freegame": self.reels["PFR0"],    # Use premium free reel
            "superspin": self.reels["SSR"],
            "dragons_lair": self.reels["DLR0"], # Dragon's Lair bonus reel
        }

        self.bet_modes = [
            # Enhanced Base Game Mode
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    # Enhanced Wincap Distribution
                    Distribution(
                        criteria="wincap",
                        quota=0.0005,  # More exclusive for premium feel
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"PBR0": 1},
                                self.freegame_type: {"PFR0": 1},
                            },
                            "mult_values": {
                                # Progressive multipliers for premium experience
                                self.freegame_type: {
                                    2: 150, 3: 100, 5: 80, 10: 50, 20: 30, 50: 15, 100: 5, 200: 2, 500: 1
                                }
                            },
                            "landing_wilds": {0: 50, 1: 30, 2: 15, 3: 8, 4: 2, 5: 1},  # Up to 5 wilds
                            "scatter_triggers": {3: 1, 4: 3, 5: 5},  # Better scatter frequency
                            "force_wincap": True,
                            "force_freegame": True,
                        },
                    ),
                    # Enhanced Free Game Distribution
                    Distribution(
                        criteria="freegame",
                        quota=0.08,  # Increased frequency
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"PBR0": 1},
                                self.freegame_type: {"PFR0": 1},
                            },
                            "mult_values": {
                                self.freegame_type: {
                                    2: 300, 3: 200, 5: 120, 10: 80, 20: 40, 50: 20, 100: 8, 200: 3
                                }
                            },
                            "landing_wilds": {0: 100, 1: 50, 2: 25, 3: 10, 4: 3},
                            "scatter_triggers": {3: 2, 4: 4, 5: 6},
                            "force_wincap": False,
                            "force_freegame": True,
                        },
                    ),
                    # Premium High Win Distribution
                    Distribution(
                        criteria="bigwin",
                        quota=0.02,
                        conditions={
                            "reel_weights": {self.basegame_type: {"PBR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                    # Standard Win Distribution
                    Distribution(
                        criteria="basegame",
                        quota=0.45,
                        conditions={
                            "reel_weights": {self.basegame_type: {"PBR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                    # No Win Distribution
                    Distribution(
                        criteria="0",
                        quota=0.45,  # Balanced for good hit frequency
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {self.basegame_type: {"PBR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                ],
            ),
            # Premium Bonus Buy Mode - Enhanced
            BetMode(
                name="bonus",
                cost=100.0,  # More accessible bonus buy
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    # Guaranteed premium feature entry
                    Distribution(
                        criteria="wincap",
                        quota=0.002,  # Higher chance for bonus buy
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"PBR0": 1},
                                self.freegame_type: {"PFR0": 1},
                            },
                            "mult_values": {
                                self.freegame_type: {
                                    2: 100, 3: 80, 5: 60, 10: 40, 20: 25, 50: 15, 100: 8, 200: 3, 500: 1
                                }
                            },
                            "landing_wilds": {0: 30, 1: 25, 2: 20, 3: 15, 4: 8, 5: 2},
                            "scatter_triggers": {3: 1, 4: 2, 5: 3},
                            "force_wincap": True,
                            "force_freegame": True,
                        },
                    ),
                    # Premium Free Game Distribution
                    Distribution(
                        criteria="freegame",
                        quota=0.998,  # Almost guaranteed entry
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"PBR0": 1},
                                self.freegame_type: {"PFR0": 1},
                            },
                            "mult_values": {
                                self.freegame_type: {
                                    2: 200, 3: 150, 5: 100, 10: 70, 20: 40, 50: 20, 100: 10, 200: 5
                                }
                            },
                            "scatter_triggers": {3: 1, 4: 2, 5: 4},
                            "landing_wilds": {0: 50, 1: 30, 2: 15, 3: 8, 4: 3},
                            "force_wincap": False,
                            "force_freegame": True,
                        },
                    ),
                ],
            ),
            # Enhanced Superspin Mode - Premium Hold & Win
            BetMode(
                name="superspin",
                cost=25,  # More accessible 
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    # Premium Jackpot Distribution
                    Distribution(
                        criteria="wincap",
                        quota=0.002,  # Higher jackpot chance
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"SSR": 1, "SSWCAP": 8},  # Enhanced jackpot weights
                            },
                            "prize_values": {
                                # Enhanced prize ladder
                                1: 5, 2: 8, 5: 15, 10: 25, 25: 40, 50: 60, 100: 80, 250: 50,
                                500: 30, 1000: 15, 2500: 8, 5000: 4, 10000: 2
                            },
                            "force_wincap": True,
                            "force_freegame": False,
                        },
                    ),
                    # Premium Win Distribution  
                    Distribution(
                        criteria="bigwin", 
                        quota=0.15,  # Better big win frequency
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"SSR": 1, "SSWCAP": 2},
                            },
                            "prize_values": {
                                1: 100, 2: 150, 5: 200, 10: 250, 25: 200, 50: 150, 
                                100: 100, 250: 60, 500: 30, 1000: 10
                            },
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                    # Standard Win Distribution
                    Distribution(
                        criteria="basegame",
                        quota=0.7,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"SSR": 1},
                            },
                            "prize_values": {
                                1: 500, 2: 300, 5: 200, 10: 100, 25: 50, 50: 30, 
                                100: 15, 250: 8, 500: 3, 1000: 1
                            },
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                    # Dead Spin Distribution  
                    Distribution(
                        criteria="0",
                        quota=0.148,
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {self.basegame_type: {"SSR": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                            "prize_values": {1: 1000},  # Minimal prize values for dead spins
                        },
                    ),
                ],
            ),
            # Dragon's Lair Hold & Win Bonus Mode
            BetMode(
                name="dragons_lair",
                cost=0,  # Triggered by collection, no cost
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    # Jackpot Distribution for Dragon's Lair
                    Distribution(
                        criteria="wincap",
                        quota=0.005,  # 0.5% jackpot chance
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {"dragons_lair": {"DLR0": 1}},
                            "prize_values": {
                                # Enhanced jackpot values
                                10: 5, 25: 10, 50: 15, 100: 20, 250: 25, 500: 20,
                                1000: 15, 2500: 10, 5000: 5, 10000: 3
                            },
                            "force_wincap": True,
                            "force_freegame": False,
                        },
                    ),
                    # High Win Distribution
                    Distribution(
                        criteria="bigwin",
                        quota=0.15,
                        conditions={
                            "reel_weights": {"dragons_lair": {"DLR0": 1}},
                            "prize_values": {
                                5: 50, 10: 100, 25: 150, 50: 200, 100: 150,
                                250: 100, 500: 50, 1000: 20, 2500: 5
                            },
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                    # Standard Win Distribution
                    Distribution(
                        criteria="basegame",
                        quota=0.7,
                        conditions={
                            "reel_weights": {"dragons_lair": {"DLR0": 1}},
                            "prize_values": {
                                1: 300, 2: 250, 5: 200, 10: 150, 25: 100,
                                50: 50, 100: 25, 250: 10, 500: 3
                            },
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                    # Low/No Win Distribution
                    Distribution(
                        criteria="0",
                        quota=0.145,
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {"dragons_lair": {"DLR0": 1}},
                            "prize_values": {1: 1000},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                ],
            ),
        ]
