import numpy as np
from numba import jit, prange


def get_vorticity_boundaries(omega, psi, n, h, u_lid, t) -> np.ndarray:
    omega[1:n-1, 0] = -(8 * psi[1:n-1, 1] - psi[1:n-1, 2]) / (2*(h**2))  # Bottom boundary
    omega[1:n-1, n-1] = -(8 * psi[1:n-1, n-2] - psi[1:n-1, n-3]) / (2*(h**2)) - (3 * u_lid(t)) / h  # Top boundary
    omega[0, 1:n-1] = -(8 * psi[1, 1:n-1] - psi[2, 1:n-1]) / (2*(h**2))  # Left boundary
    omega[n-1, 1:n-1] = -(8 * psi[n-2, 1:n-1] - psi[n-3, 1:n-1]) / (2*(h**2))  # Right boundary
    return omega


@jit(nopython=True, parallel=False)
def get_vorticity_update(omega, n, h, u_x, u_y, dt, re) -> np.ndarray:
    for i in prange(1, n-1):
        for j in prange(1, n-1):
            omega[i, j] += dt * _get_vorticity_derivatives(omega, i, j, re, h, u_x, u_y)
    return omega


@jit(nopython=True, parallel=False)
def _get_vorticity_derivatives(omega, i, j, re, h, u_x, u_y) -> np.ndarray:
    term_a = (1/re) * (omega[i + 1, j] + omega[i, j + 1] + omega[i - 1, j] + omega[i, j - 1] - 4 * omega[i, j])/(h**2)
    term_b = u_x[i, j] * (omega[i + 1, j] - omega[i - 1, j]) / (2 * h)
    term_c = u_y[i, j] * (omega[i, j + 1] - omega[i, j - 1]) / (2 * h)

    return term_a - term_b - term_c
