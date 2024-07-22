import numpy as np
from numba import jit, prange


@jit(nopython=True, parallel=False)
def get_streamline_update(omega, psi, n, h) -> np.ndarray:
    for i in prange(1, n - 1):
        for j in prange(1, n - 1):
            psi[i, j] = 0.25 * ((h ** 2) * omega[i, j] + psi[i + 1, j] + psi[i - 1, j] + psi[i, j + 1] + psi[i, j - 1])
    return psi
