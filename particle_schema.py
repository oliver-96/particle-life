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


PARTICLE_INTERACTIONS = np.array([
    # 0   1  2  3  4
    [0.5, 0, 0, 0, 0],  # Type 0 interactions
    [0, 0.5, 0, -0.1, 0.2],  # Type 1 interactions
    [0, 0.1, 0, -0.15, 1],   # Type 2 interactions 
    [0, -0.07, 0.02, -0.1, 0.5],   # Type 3 interactions    
    [0, -0.07, 0.02, -0.1, 0.5],   # Type 4 interactions
   
])