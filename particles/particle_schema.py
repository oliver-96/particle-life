import numpy as np

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
    7: {
        'colour': (128, 128, 128),
    },
    8: {
        'colour': (128, 0, 0),
    },
    9: {
        'colour': (0, 128, 0),
    },
    10: {
        'colour': (0, 0, 128),
    },
    11: {
        'colour': (128, 128, 0),
    },
}

num_types = len(PARTICLE_TYPES)
PARTICLE_INTERACTIONS = np.random.rand(num_types, num_types)
