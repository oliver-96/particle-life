import numpy as np

# Particle simulation configuration
WIDTH, HEIGHT = 800, 800
DT = 0.01

# Particle properties
RADIUS = 2
MIN_DISTANCE = 0.3
MAX_DISTANCE = 80
MAX_FORCE_DISTANCE = (MIN_DISTANCE + 1) / 2

DRAG = 0.05
FORCE_FACTOR = 3

GRID_SIZE = MAX_DISTANCE * 1.25


# Colour
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLOUR_MAP = {
    0: WHITE,
    1: RED,
    2: GREEN,
    3: BLUE
}

#  Particle types
PARTICLE_INTERACTIONS_DICT = {
    0: {
        0: 0.5,
        1: 0,
        2: 0,
        3: 0,
    },
    1: {
        0: 0.3,
        1: 0.5,
        2: 0.3,
        3: 0,
    },
    2: {
        0: 0,
        1: 0,
        2: 0.5,
        3: 0.3,
    },
    3: {
        0: 0,
        1: 0,
        2: 0,
        3: 0.5,
    },
}

sorted_particles_interaction_dict = sorted(PARTICLE_INTERACTIONS_DICT.keys()) 
PARTICLE_INTERACTIONS = np.array([[PARTICLE_INTERACTIONS_DICT[row][col] for col in sorted_particles_interaction_dict] for row in sorted_particles_interaction_dict])