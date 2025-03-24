PARTICLE_TYPES = {
    'type_0': {
        'colour': (255, 255, 255),
        'radius': 5,
        'mass': 1
    },

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
    },

    'type_4': {
        'colour': (0, 255, 255),
        'radius': 5,
        'mass': 1
    }
}


PARTICLE_INTERACTIONS = {
    'type_0': {
        'type_0': 0.5,
    },
    
    'type_1': {
        'type_1': 0.7,
        'type_2': 0.0,

        'type_3': -0.1,
        'type_4': 0
    },

    'type_2': {
        'type_1': -0.6,
        'type_2': 0,

        'type_3': -0.15, 
        'type_4': 1
    },

    'type_3': {
        'type_1': 0.1,
        'type_2': -0.08,
        'type_3': 0.2,
        'type_4': 0.1

    },

    'type_4': {
        'type_1': 0.03,
        'type_2': 0.02,
        'type_3': -0.1,
        'type_4': -0.1
    }

}