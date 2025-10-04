"""Main file for generating results - medium simulation size."""

from gamestate import GameState
from game_config import GameConfig
from utils.rgs_verification import execute_all_tests
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":

    # Medium simulation parameters - balance between accuracy and speed
    num_threads = 8
    batching_size = 50000
    compression = True
    profiling = False

    # Medium simulation counts - sufficient for Stake Engine upload
    num_sim_args = {
        "base": int(5e4),  # 50k simulations for base game
        "bonus": int(2e4),  # 20k simulations for bonus
        "superspin": int(3e4),  # 30k simulations for superspin
    }

    config = GameConfig()
    gamestate = GameState(config)

    print("Running medium simulations (50k/20k/30k)...")
    create_books(
        gamestate,
        config,
        num_sim_args,
        batching_size,
        num_threads,
        compression,
        profiling,
    )

    print("Generating configs...")
    generate_configs(gamestate)

    print("Running format checks...")
    execute_all_tests(config)
    
    print("Complete!")
