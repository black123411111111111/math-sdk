"""Main file for generating results - no optimization version."""

from gamestate import GameState
from game_config import GameConfig
from utils.rgs_verification import execute_all_tests
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":

    # Enhanced simulation parameters for premium game
    num_threads = 8  # Optimized threading
    batching_size = 100000  # Larger batches for better performance
    compression = True
    profiling = False

    # Enhanced simulation counts for premium accuracy
    num_sim_args = {
        "base": int(5e5),  # 500k simulations for base game
        "bonus": int(2e5),  # 200k simulations for bonus
        "superspin": int(3e5),  # 300k simulations for superspin
    }

    # Run without optimization first
    run_conditions = {
        "run_sims": True,
        "run_optimization": False, 
        "run_analysis": False,
        "run_format_checks": True,
    }

    config = GameConfig()
    gamestate = GameState(config)

    if run_conditions["run_sims"]:
        print("Running simulations...")
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

    if run_conditions["run_format_checks"]:
        print("Running format checks...")
        execute_all_tests(config)
    
    print("Complete!")
