import numpy as np

PARTICLE_TYPES = {
    'type_0': {
        'colour': (255, 255, 255),
        'radius': 5,
        'mass': 1,
        'type': 0
    },

    'type_1': {
        'colour': (255, 0, 0),
        'radius': 5,
        'mass': 1,
        'type': 1
    },

    'type_2': {
        'colour': (0, 255, 0),
        'radius': 5,
        'mass': 1,
        'type': 2
    },

    'type_3': {
        'colour': (0, 0, 255),
        'radius': 5,
        'mass': 1,
        'type': 3
    },

    'type_4': {
        'colour': (0, 255, 255),
        'radius': 5,
        'mass': 1,
        'type': 4
    }
}

PARTICLE_INTERACTIONS_DICT = {
    'type_0': {
        'type_0': 0.5,
        'type_1': 0,
        'type_2': 0,
        'type_3': 0,
        'type_4': 0
    },
    'type_1': {
        'type_0': 0,
        'type_1': 0.5,
        'type_2': 0.3,
        'type_3': 0,
        'type_4': 0
    },
    'type_2': {
        'type_0': 0,
        'type_1': 0,
        'type_2': 0.5,
        'type_3': 0.3,
        'type_4': 0
    },
    'type_3': {
        'type_0': 0,
        'type_1': 0,
        'type_2': 0,
        'type_3': 0.5,
        'type_4': 0.3
    },
    'type_4': {
        'type_0': 0,
        'type_1': 0,
        'type_2': 0,
        'type_3': 0,
        'type_4': 0.5
    }
}

sorted_particles_interaction_dict = sorted(PARTICLE_INTERACTIONS_DICT.keys()) 
PARTICLE_INTERACTIONS = np.array([[PARTICLE_INTERACTIONS_DICT[row][col] for col in sorted_particles_interaction_dict] for row in sorted_particles_interaction_dict])
