import numpy as np
from numba import jit, prange


@jit(nopython=True, parallel=False)
def get_concentration_update(conc, u_x, u_y, n, h, dt) -> np.ndarray:
    for i in prange(1, n - 1):
        for j in prange(1, n):
            term_u = (u_x[i, j] * dt / h) * (conc[i, j] - conc[i - 1, j]) if u_x[i, j] >= 0 \
                else ((u_x[i, j]) * dt / h) * (conc[i + 1, j] - conc[i, j])
            term_v = (u_y[i, j] * dt / h) * (conc[i, j] - conc[i, j - 1]) if u_y[i, j] >= 0 \
                else ((u_y[i, j]) * dt / h) * (conc[i, j + 1] - conc[i, j])

            conc[i, j] = conc[i, j] - term_u
            conc[i, j] = conc[i, j] - term_v

    return conc
