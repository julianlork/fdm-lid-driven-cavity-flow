import numpy as np
from numba import jit, prange


@jit(nopython=True, parallel=False)
def get_velocity_update(psi, u_x, u_y, n, h) -> tuple[np.ndarray, np.ndarray]:
    for i in prange(1, n - 1):
        for j in prange(1, n - 1):
            u_x[i, j] = (psi[i, j + 1] - psi[i, j - 1]) / (2 * h)
            u_y[i, j] = -(psi[i + 1, j] - psi[i - 1, j]) / (2 * h)
    return u_x, u_y
