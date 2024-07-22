from config import configuration as cfg
from simulation import grid as gs
from simulation import solver as sv
from visualization import animation as anim
from visualization import plots as plt
import numpy as np


def main() -> None:

    anim_config = cfg.AnimationConfig(
        export_dir="./sim_out/constant_drive"
    )
    sim_config = cfg.SimulationConfig()
    sim_grid = gs.Grid(sim_config)
    anim_renderer = anim.ConcentrationRenderer(anim_config, sim_config, sim_grid)
    solver = sv.Solver(sim_config, sim_grid)
    result = solver.run(anim_renderer)
    plt.export_velocity_stream_plot(result, anim_config, sim_grid)


if __name__ == '__main__':
    main()
