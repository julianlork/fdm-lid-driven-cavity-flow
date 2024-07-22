from dataclasses import dataclass
from typing import Callable


# Verbose Type hinting
Time = float
Velocity = float


@dataclass
class SimulationConfig:
    num_nodes: int = 101
    temporal_step_size_in_sec: float = 1e-3
    simulation_time_in_sec: float = 60.
    reynolds_number: int = 500
    lid_velocity_fcn: Callable[[Time], Velocity] = lambda t: 1.0


@dataclass
class AnimationConfig:
    animation_time_in_sec: float = 10.
    frames_per_second: int = 30
    filename: str = 'animation.gif'
    export_dir: str = "./sim_out/"


