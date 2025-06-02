import numpy as np
from sim_config.setup_schema import MIN_DISTANCE

#  Particle types
PARTICLE_TYPES = {
    0: {
        'colour': (255, 255, 255),
    },

    1: {
        'colour': (255, 0, 0),
    },

    2: {
        'colour': (0, 255, 0),
    },

    3: {
        'colour': (0, 0, 255),
    },
    4: {
        'colour': (255, 255, 0),
    },
    5: {
        'colour': (255, 0, 255),
    },
    6: {
        'colour': (0, 255, 255),
    },
}

num_types = len(PARTICLE_TYPES)
PARTICLE_INTERACTIONS = np.random.rand(num_types, num_types)
