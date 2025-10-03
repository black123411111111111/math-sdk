"""Test file for verifying game runs correctly before full simulation."""

from gamestate import GameState
from game_config import GameConfig
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":
    # Small test simulation
    num_threads = 2
    batching_size = 1000
    compression = True
    profiling = False

    # Small simulation counts for testing
    num_sim_args = {
        "base": int(1e3),  # 1k simulations for quick test
        "bonus": int(5e2),  # 500 simulations  
        "superspin": int(5e2),  # 500 simulations
    }

    config = GameConfig()
    gamestate = GameState(config)

    print("Running test simulation...")
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
    print("Test complete!")
