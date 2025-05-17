import numpy as np
from numba import njit

from sim_config.setup_schema import MIN_DISTANCE, MAX_FORCE_DISTANCE

@njit
def calculate_forces(normalised_distances, g_values):

    forces = np.zeros_like(normalised_distances)

    # Zone 1: distance <= MIN_DISTANCE
    mask1 = normalised_distances <= MIN_DISTANCE
    forces[mask1] = (normalised_distances[mask1] / MIN_DISTANCE) - 1

    # Zone 2: MIN_DISTANCE < distance <= MAX_FORCE_DISTANCE
    mask2 = (normalised_distances > MIN_DISTANCE) & (normalised_distances <= MAX_FORCE_DISTANCE)
    forces[mask2] = g_values[mask2] / (MAX_FORCE_DISTANCE - MIN_DISTANCE) * (normalised_distances[mask2] - MIN_DISTANCE)

    # Zone 3: MAX_FORCE_DISTANCE < distance <= 1
    mask3 = (normalised_distances > MAX_FORCE_DISTANCE) & (normalised_distances <= 1)
    forces[mask3] = g_values[mask3] / (1 - MAX_FORCE_DISTANCE) * (1 - normalised_distances[mask3])

    # Zone 4: distance > 1 — forces remain 0
    return forces
    