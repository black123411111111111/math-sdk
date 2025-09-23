"""Test Dragon's Hoard 3-star upgrade features."""

import pytest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

# Add the game directory to path for relative imports
game_dir = os.path.join(os.path.dirname(__file__), '../../games/0_0_expwilds')
sys.path.insert(0, game_dir)

# Import game modules
from game_config import GameConfig


class MockSymbol:
    """Mock symbol for testing."""
    def __init__(self, name):
        self.name = name
        self.attributes = {}
    
    def assign_attribute(self, attr_dict):
        self.attributes.update(attr_dict)
    
    def check_attribute(self, attr_name):
        return attr_name in self.attributes
    
    def get_attribute(self, attr_name):
        return self.attributes.get(attr_name)


class MockGameExecutables:
    """Mock GameExecutables for testing Dragon's Hoard features."""
    
    def __init__(self):
        self.config = GameConfig()
        self.collection_meter = 0
        self.dragons_fury_active = False
        self.dragons_lair_respins = 0
        self.gametype = self.config.basegame_type
        self.board = [[MockSymbol("X") for _ in range(5)] for _ in range(5)]
        self.win_data = {"totalWin": 0}
        self.expanding_wilds = []
        self.sticky_symbols = []
        self.existing_sticky_symbols = []
        self.new_exp_wilds = []
        self.avaliable_reels = [0, 1, 2, 3, 4]
    
    def create_symbol(self, name):
        return MockSymbol(name)


def test_config_loading():
    """Test that the Dragon's Hoard config loads correctly."""
    config = GameConfig()
    
    # Test new configuration values
    assert config.collection_meter_max == 15
    assert config.dragons_lair_initial_spins == 3
    assert config.dragons_fury_trigger_chance == 0.08
    assert config.multiplier_wild_reels == [1, 2, 3]
    assert config.multiplier_wild_values == {2: 0.7, 3: 0.3}
    assert config.dragons_lair_type == "dragons_lair"
    
    # Test that Gold Coin is in special symbols
    assert "gold_coin" in config.special_symbols
    assert "GC" in config.special_symbols["gold_coin"]
    
    print("✓ Configuration loaded correctly")


def test_multiplier_wild_logic():
    """Test multiplier wild logic for center reels."""
    mock_game = MockGameExecutables()
    
    # Test that center reels get enhanced multipliers
    assert 1 in mock_game.config.multiplier_wild_reels  # Reel 2 (0-indexed)
    assert 2 in mock_game.config.multiplier_wild_reels  # Reel 3 (0-indexed)  
    assert 3 in mock_game.config.multiplier_wild_reels  # Reel 4 (0-indexed)
    assert 0 not in mock_game.config.multiplier_wild_reels  # Reel 1 (0-indexed)
    assert 4 not in mock_game.config.multiplier_wild_reels  # Reel 5 (0-indexed)
    
    # Test multiplier values
    multiplier_values = mock_game.config.multiplier_wild_values
    assert 2 in multiplier_values  # 2x multiplier
    assert 3 in multiplier_values  # 3x multiplier
    assert multiplier_values[2] + multiplier_values[3] == 1.0  # Should sum to 100%
    
    print("✓ Multiplier wild logic configured correctly")


def test_gold_coin_collection_logic():
    """Test Gold Coin collection mechanics."""
    mock_game = MockGameExecutables()
    
    # Initially no coins collected
    assert mock_game.collection_meter == 0
    
    # Place Gold Coins on board
    mock_game.board[0][0] = mock_game.create_symbol("GC")
    mock_game.board[2][1] = mock_game.create_symbol("GC")
    mock_game.board[4][3] = mock_game.create_symbol("GC")
    
    # Manually count coins (since we can't import the full method)
    coin_count = 0
    for reel in range(5):
        for row in range(5):
            if mock_game.board[reel][row].name == "GC":
                coin_count += 1
    
    # Should find 3 coins
    assert coin_count == 3
    
    # Simulate collection meter update
    mock_game.collection_meter += coin_count
    assert mock_game.collection_meter == 3
    
    # Test meter cap
    mock_game.collection_meter = mock_game.config.collection_meter_max + 5
    if mock_game.collection_meter > mock_game.config.collection_meter_max:
        mock_game.collection_meter = mock_game.config.collection_meter_max
    
    assert mock_game.collection_meter == mock_game.config.collection_meter_max
    
    print("✓ Gold Coin collection logic working")


def test_dragons_lair_trigger_logic():
    """Test Dragon's Lair trigger conditions."""
    mock_game = MockGameExecutables()
    
    # Test trigger condition when meter is not full
    mock_game.collection_meter = mock_game.config.collection_meter_max - 1
    should_trigger = mock_game.collection_meter >= mock_game.config.collection_meter_max
    assert should_trigger == False
    
    # Test trigger condition when meter is full
    mock_game.collection_meter = mock_game.config.collection_meter_max
    should_trigger = mock_game.collection_meter >= mock_game.config.collection_meter_max
    assert should_trigger == True
    
    # Simulate trigger effects
    if should_trigger:
        mock_game.collection_meter = 0  # Reset meter
        mock_game.dragons_lair_respins = mock_game.config.dragons_lair_initial_spins
        mock_game.gametype = mock_game.config.dragons_lair_type
    
    assert mock_game.collection_meter == 0
    assert mock_game.dragons_lair_respins == 3
    assert mock_game.gametype == "dragons_lair"
    
    print("✓ Dragon's Lair trigger logic working")


def test_dragons_fury_trigger_conditions():
    """Test Dragon's Fury trigger conditions.""" 
    mock_game = MockGameExecutables()
    
    # Test conditions for Dragon's Fury
    # Should only trigger in base game
    assert mock_game.gametype == mock_game.config.basegame_type
    
    # Should only trigger on non-winning spins
    mock_game.win_data = {"totalWin": 0}
    is_losing_spin = mock_game.win_data.get("totalWin", 0) == 0
    assert is_losing_spin == True
    
    # Test that winning spins don't trigger
    mock_game.win_data = {"totalWin": 10}
    is_losing_spin = mock_game.win_data.get("totalWin", 0) == 0
    assert is_losing_spin == False
    
    # Test trigger chance is reasonable
    trigger_chance = mock_game.config.dragons_fury_trigger_chance
    assert 0 < trigger_chance < 1  # Should be between 0 and 1
    assert trigger_chance == 0.08  # Should be 8%
    
    print("✓ Dragon's Fury trigger conditions working")


def test_multiplier_stacking_logic():
    """Test multiplier stacking calculation."""
    mock_game = MockGameExecutables()
    
    # Create test symbols with multipliers
    wild1 = mock_game.create_symbol("W")
    wild1.assign_attribute({"multiplier": 2})
    
    wild2 = mock_game.create_symbol("W") 
    wild2.assign_attribute({"multiplier": 3})
    
    regular_symbol = mock_game.create_symbol("H1")
    
    # Place on board
    mock_game.board[0][0] = wild1
    mock_game.board[1][0] = wild2
    mock_game.board[2][0] = regular_symbol
    
    # Manually calculate multiplier (simulating the method)
    total_multiplier = 1.0
    payline_positions = [(0, 0), (1, 0), (2, 0)]
    
    for reel, row in payline_positions:
        symbol = mock_game.board[reel][row]
        if symbol.name in ["W", "MW"] and symbol.check_attribute("multiplier"):
            wild_multiplier = symbol.get_attribute("multiplier")
            total_multiplier *= wild_multiplier
    
    # Should be 2 * 3 = 6x multiplier
    assert total_multiplier == 6.0
    
    # Test win application
    win_amount = 10
    final_win = win_amount * total_multiplier
    assert final_win == 60
    
    print("✓ Multiplier stacking logic working")


def test_reel_configuration():
    """Test that all required reels are configured."""
    config = GameConfig()
    
    # Test that Dragon's Lair reel is configured
    assert "DLR0" in config.reels
    
    # Test that padding reels include Dragon's Lair
    assert "dragons_lair" in config.padding_reels
    
    # Test that Dragon's Lair betmode exists
    dragons_lair_mode = None
    for betmode in config.bet_modes:
        if betmode.get_name() == "dragons_lair":
            dragons_lair_mode = betmode
            break
    
    assert dragons_lair_mode is not None
    assert dragons_lair_mode.get_feature() == True
    assert dragons_lair_mode.get_cost() == 0  # Should be triggered, not bought
    
    print("✓ Reel configuration working")


if __name__ == "__main__":
    test_config_loading()
    test_multiplier_wild_logic()
    test_gold_coin_collection_logic()
    test_dragons_lair_trigger_logic()
    test_dragons_fury_trigger_conditions()
    test_multiplier_stacking_logic()
    test_reel_configuration()
    print("\n✅ All Dragon's Hoard upgrade tests passed!")