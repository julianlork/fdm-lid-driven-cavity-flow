from __future__ import annotations
from config.configuration import SimulationConfig
from simulation.grid import Grid
from simulation.velocity import get_velocity_update
from simulation.transport import get_concentration_update
from simulation.streamline import get_streamline_update
from simulation.vorticity import get_vorticity_update, get_vorticity_boundaries
from simulation.results import SimulationResult
from visualization.animation import AnimationRenderer


class Solver:
    def __init__(self, config: SimulationConfig, grid: Grid) -> None:
        self.grid = grid
        self.dt = config.temporal_step_size_in_sec
        self.n = grid.num_nodes
        self.h = grid.h
        self.lid_velocity = config.lid_velocity_fcn
        self.reynolds = config.reynolds_number
        self.termination_time = config.simulation_time_in_sec
        self.sim_results = SimulationResult(grid.num_nodes)

    def run(self, anim_renderer: AnimationRenderer | None = None) -> SimulationResult:
        t = .0
        iteration = 0

        self.sim_results.u_x[:, -1] = self.lid_velocity(t)
        self.sim_results.conc[0, :] = 1.0

        while t <= self.termination_time:
            iteration += 1
            t += self.dt

            self.sim_results.omega = get_vorticity_boundaries(self.sim_results.omega, self.sim_results.psi, self.n, self.h, self.lid_velocity, t)
            self.sim_results.omega = get_vorticity_update(self.sim_results.omega, self.n, self.h, self.sim_results.u_x, self.sim_results.u_y, self.dt, self.reynolds)
            self.sim_results.psi = get_streamline_update(self.sim_results.omega, self.sim_results.psi, self.n, self.h)
            self.sim_results.u_x, self.sim_results.u_y = get_velocity_update(self.sim_results.psi, self.sim_results.u_x, self.sim_results.u_y, self.n, self.h)
            self.sim_results.conc = get_concentration_update(self.sim_results.conc, self.sim_results.u_x, self.sim_results.u_y, self.n, self.h, self.dt)

            if anim_renderer is not None and iteration % anim_renderer.img_capture_rate == 0:
                anim_renderer.capture_frame(self.sim_results, t)

        if anim_renderer is not None:
            anim_renderer.finalize()

        return self.sim_results
