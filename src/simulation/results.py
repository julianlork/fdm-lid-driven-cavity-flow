import numpy as np


class SimulationResult:

    def __init__(self, num_nodes: int) -> None:
        self.omega = np.zeros((num_nodes, num_nodes))
        self.psi = np.zeros((num_nodes, num_nodes))
        self.conc = np.zeros((num_nodes, num_nodes))
        self.u_x = np.zeros((num_nodes, num_nodes))
        self.u_y = np.zeros((num_nodes, num_nodes))
