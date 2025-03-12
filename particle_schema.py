PARTICLE_TYPES = {
    'type_1': {
        'colour': (255, 0, 0),
        'radius': 5,
        'mass': 1
    },

    'type_2': {
        'colour': (0, 255, 0),
        'radius': 5,
        'mass': 1
    },

    'type_3': {
        'colour': (0, 0, 255),
        'radius': 5,
        'mass': 1
    }
}

PARTICLE_INTERACTIONS = {
    'type_1': {
        'type_1': 0.5,
        'type_2': -0.2,
        'type_3': 0.1
    },

    'type_2': {
        'type_1': 0.1,
        'type_2': 0.6,
        'type_3': -0.1
    },

    'type_3': {
        'type_1': -0.1,
        'type_2': 0.3,
        'type_3': 0.5
    }
}