import numpy as np
from config import configuration as cfg


DIM_X = 1.0
DIM_Y = 1.0


class Grid:
    """
    Grid class for the lid-driven cavity simulation.

    Attributes:
        num_nodes (int): Number of grid nodes in each dimension.
        h (float): Grid spacing in the x- and y-dimension.
        x (np.ndarray): Array of x-coordinates.
        y (np.ndarray): Array of y-coordinates.
        grid_x (np.ndarray): 2D meshgrid array for x-coordinates.
        grid_y (np.ndarray): 2D meshgrid array for y-coordinates.
    """

    def __init__(self, config: cfg.SimulationConfig) -> None:

        """
        Initialize grid with provided simulation configuration.

        :param config: Simulation configuration.
        """

        self.num_nodes = config.num_nodes
        self.h = DIM_X / (self.num_nodes - 1)
        self.x = np.linspace(0., DIM_X, self.num_nodes)
        self.y = np.linspace(0., DIM_Y, self.num_nodes)
        self.grid_x, self.grid_y = np.meshgrid(self.x, self.y)
        self.validate_grid()

    def validate_grid(self) -> None:
        """
        Validates the grid parameters to ensure they are within acceptable ranges.
        """
        if self.num_nodes < 2:
            raise ValueError("num_nodes must be greater than 1.")
        if self.h <= 0:
            raise ValueError("h must be positive.")
