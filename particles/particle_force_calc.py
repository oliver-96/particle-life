import numpy as np
from numba import njit  

from sim_config.setup_schema import MIN_DISTANCE, MAX_FORCE_DISTANCE

@njit()
def calculate_forces(normalised_distances, g_values):
    n = normalised_distances.shape[0]
    forces = np.empty(n, dtype=np.float32)

    for i in range(n):
        d = normalised_distances[i]
        g = g_values[i]

        if d <= MIN_DISTANCE:
            forces[i] = (d / MIN_DISTANCE) - 1.0

        elif d <= MAX_FORCE_DISTANCE:
            forces[i] = g / (MAX_FORCE_DISTANCE - MIN_DISTANCE) * (d - MIN_DISTANCE)

        elif d <= 1.0:
            forces[i] = g / (1.0 - MAX_FORCE_DISTANCE) * (1.0 - d)

        else:
            forces[i] = 0.0

    return forces

@njit
def accumulate_forces(i_indices, j_indices, force_1, force_2, acc):
    for idx in range(i_indices.shape[0]):
        i = i_indices[idx]
        j = j_indices[idx]

        for d in range(2):
            acc[i, d] -= force_1[idx, d]
            acc[j, d] += force_2[idx, d]
