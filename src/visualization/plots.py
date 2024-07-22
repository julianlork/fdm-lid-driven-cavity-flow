from config.configuration import AnimationConfig
from simulation.results import SimulationResult
from simulation.grid import Grid
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np

FIGSIZE = (8, 6)


def export_velocity_stream_plot(result: SimulationResult, config: AnimationConfig, grid: Grid,
                                filename: str = "velocity_stream.png") -> None:
    Path(config.export_dir).mkdir(exist_ok=True, parents=True)
    export_path = Path.joinpath(Path(config.export_dir), filename)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    _ = ax.contourf(
        grid.grid_y,
        grid.grid_x,
        np.sqrt(result.u_x ** 2 + result.u_y ** 2),
        np.arange(0, 1, 0.05)
    )
    _ = ax.streamplot(
        grid.grid_y.T,
        grid.grid_x.T,
        result.u_x.T,
        result.u_y.T,
        density=1.5,
        color="tab:cyan"
    )
    _ = ax.axis("equal")
    _ = ax.set_title("Velocity stream")

    plt.savefig(f"{export_path}")
