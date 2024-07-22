from typing import Protocol
from abc import abstractmethod
from simulation.results import SimulationResult
from config.configuration import AnimationConfig
from config.configuration import SimulationConfig
from simulation.grid import Grid
from matplotlib import pyplot as plt
from matplotlib import animation as animation
from pathlib import Path
import numpy as np

FIG_SIZE = (8, 8)
VECTOR_FIELD_STEP = 5
CONTOUR_F_LEVELS = list(np.arange(0, 0.4, 0.005)) + list(np.arange(0.4, 1, 0.1))


class AnimationRenderer(Protocol):
    @property
    @abstractmethod
    def img_capture_rate(self) -> int:
        ...

    def capture_frame(self, results: SimulationResult, time_in_sec: float) -> None:
        ...

    def finalize(self) -> None:
        ...


class ConcentrationRenderer:
    def __init__(self, anim_config: AnimationConfig, sim_config: SimulationConfig, grid: Grid) -> None:
        self.anim_config = anim_config
        self.sim_config = sim_config
        self.grid = grid
        self.img_capture_rate = _get_image_capture_rate(
            self.anim_config.animation_time_in_sec,
            self.anim_config.frames_per_second,
            self.sim_config.simulation_time_in_sec,
            self.sim_config.temporal_step_size_in_sec,
        )
        self.__post_init__()

    def __post_init__(self) -> None:
        self.figure = plt.figure(figsize=FIG_SIZE)
        self.grid_specs = self.figure.add_gridspec(6, 1)
        self.ax1 = self.figure.add_subplot(self.grid_specs[0, 0])
        self.ax2 = self.figure.add_subplot(self.grid_specs[1:, 0])
        self.ax1.axis('off')
        self.ax1.set_title("Lid-Velocity")
        self.ax2.axis('equal')
        self.artist_container = []

    def capture_frame(self, results: SimulationResult, time_in_sec: float) -> None:
        lid_velocity_vector = self.ax1.quiver(
            0,
            0,
            self.sim_config.lid_velocity_fcn(time_in_sec),
            0,
            color='tab:blue',
            scale=4.,
        )

        concentration_contour = self.ax2.contourf(
            self.grid.grid_y,
            self.grid.grid_x,
            results.conc,
            CONTOUR_F_LEVELS,
        )

        velocity_vector_field = self.ax2.quiver(
            self.grid.grid_y[::VECTOR_FIELD_STEP, ::VECTOR_FIELD_STEP],
            self.grid.grid_x[::VECTOR_FIELD_STEP, ::VECTOR_FIELD_STEP],
            results.u_x[::VECTOR_FIELD_STEP, ::VECTOR_FIELD_STEP],
            results.u_y[::VECTOR_FIELD_STEP, ::VECTOR_FIELD_STEP],
            color='tab:blue',
            scale=10.
        )

        self.ax2.axis('equal')

        self.artist_container.append([
            lid_velocity_vector,
            concentration_contour,
            velocity_vector_field,
        ])

        print(f"Frame Capture {len(self.artist_container)}; Elapsed Simulation Time: {time_in_sec:.2f} s;")

    def finalize(self) -> None:
        print("Rendering results - this might take a while.")
        Path(self.anim_config.export_dir).mkdir(exist_ok=True, parents=True)
        export_path = Path.joinpath(Path(self.anim_config.export_dir), self.anim_config.filename)
        gif_writer = animation.PillowWriter(fps=self.anim_config.frames_per_second)
        anim = animation.ArtistAnimation(self.figure, self.artist_container, blit=False)
        anim.save(f'{export_path}', writer=gif_writer)
        plt.close(self.figure)


def _get_image_capture_rate(anim_time_sec: float, frames_per_sec: int, sim_time_sec: float,
                            step_size_sec: float) -> int:
    required_number_of_frames = frames_per_sec * anim_time_sec
    total_number_of_sim_iterations = sim_time_sec / step_size_sec
    return int(total_number_of_sim_iterations / required_number_of_frames)
