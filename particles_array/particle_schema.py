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
        'colour': (0, 255, 255),
    }
}

PARTICLE_INTERACTIONS_DICT = {
    0: {
        0: 0.5,
        1: 0.3,
        2: 0,
        3: 0,
    },
    1: {
        0: 0,
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