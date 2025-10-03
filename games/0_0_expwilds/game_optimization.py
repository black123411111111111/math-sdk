"""Set conditions/parameters for optimization program program"""

from optimization_program.optimization_config import (
    ConstructScaling,
    ConstructParameters,
    ConstructConditions,
    verify_optimization_input,
)


class OptimizationSetup:
    """Handle all game mode optimization parameters."""

    def __init__(self, game_config):
        self.game_config = game_config
        self.game_config.opt_params = {
            "base": {
                "conditions": {
                    "wincap": ConstructConditions(rtp=0.008, av_win=8000, search_conditions=8000).return_dict(),  # Enhanced wincap
                    "0": ConstructConditions(rtp=0, av_win=0, search_conditions=0).return_dict(),
                    "freegame": ConstructConditions(
                        rtp=0.35, hr=180, search_conditions={"symbol": "scatter"}  # Enhanced free game RTP
                    ).return_dict(),
                    "bigwin": ConstructConditions(hr=50, rtp=0.14, av_win=200).return_dict(),  # Big win condition
                    "basegame": ConstructConditions(hr=4.2, rtp=0.462).return_dict(),  # Base game RTP (total = 0.96)
                },
                "scaling": ConstructScaling(
                    [
                        {
                            "criteria": "basegame",
                            "scale_factor": 1.3,  # Enhanced scaling
                            "win_range": (1, 2),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "basegame",
                            "scale_factor": 1.8,  # Enhanced premium scaling
                            "win_range": (10, 30),  # Better win range
                            "probability": 1.0,
                        },
                        {
                            "criteria": "bigwin",  # New scaling for big wins
                            "scale_factor": 1.5,
                            "win_range": (50, 200),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 0.7,  # Enhanced freegame scaling
                            "win_range": (800, 1500),  # Better range
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 1.4,  # Enhanced big freegame wins
                            "win_range": (2000, 5000),
                            "probability": 1.0,
                        },
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=8000,  # Enhanced simulation count
                    num_per_fence=15000,  # Better optimization depth
                    min_m2m=3,  # Enhanced range
                    max_m2m=10,  # Enhanced range
                    pmb_rtp=1.0,
                    sim_trials=8000,  # Enhanced trial count
                    test_spins=[30, 75, 150],  # Better test distribution
                    test_weights=[0.4, 0.4, 0.2],  # Enhanced weighting
                    score_type="rtp",
                ).return_dict(),
            },
            "bonus": {
                "conditions": {
                    "wincap": ConstructConditions(rtp=0.01, av_win=5000, search_conditions=5000).return_dict(),
                    "freegame": ConstructConditions(rtp=0.96, hr="x").return_dict(),
                },
                "scaling": ConstructScaling(
                    [
                        {
                            "criteria": "freegame",
                            "scale_factor": 0.9,
                            "win_range": (20, 50),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 0.8,
                            "win_range": (1000, 2000),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 1.2,
                            "win_range": (3000, 4000),
                            "probability": 1.0,
                        },
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[10, 20, 50],
                    test_weights=[0.6, 0.2, 0.2],
                    score_type="rtp",
                ).return_dict(),
            },
            "superspin": {
                "conditions": {
                    "wincap": ConstructConditions(rtp=0.01, av_win=5000, search_conditions=5000).return_dict(),
                    "0": ConstructConditions(rtp=0, av_win=0, search_conditions=0).return_dict(),
                    "basegame": ConstructConditions(hr=1.9, rtp=0.96).return_dict(),
                },
                "scaling": ConstructScaling(
                    [
                        {
                            "criteria": "freegame",
                            "scale_factor": 3,
                            "win_range": (200, 500),
                            "probability": 1.0,
                        },
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[10, 20, 50],
                    test_weights=[0.6, 0.2, 0.2],
                    score_type="rtp",
                ).return_dict(),
            },
        }

        verify_optimization_input(self.game_config, self.game_config.opt_params)
