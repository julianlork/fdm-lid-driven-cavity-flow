from config import configuration as cfg
from simulation import grid as gs
from simulation import solver as sv
from visualization import animation as anim
from visualization import plots as plt
import numpy as np


def main() -> None:

    anim_config = cfg.AnimationConfig(
        export_dir="./sim_out/periodic_drive"
    )
    sim_config = cfg.SimulationConfig(
        simulation_time_in_sec=160.0,
        lid_velocity_fcn=lambda t: np.sin(t/3),
        reynolds_number=2000,
    )
    sim_grid = gs.Grid(sim_config)
    anim_renderer = anim.ConcentrationRenderer(anim_config, sim_config, sim_grid)
    print(anim_renderer.img_capture_rate)
    solver = sv.Solver(sim_config, sim_grid)
    result = solver.run(anim_renderer)
    plt.export_velocity_stream_plot(result, anim_config, sim_grid)


if __name__ == '__main__':
    main()
