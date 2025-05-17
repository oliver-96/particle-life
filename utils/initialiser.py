from particles_array.particle import ParticleSystems

def initialise_particles(testing=False):
    particle_manager = ParticleSystems()

    if testing:
        num_particles = 1000
        particle_manager.add_system(num_particles, 0, testing=True)
    else:
        particle_manager.add_system(200, 0)
        particle_manager.add_system(200, 1)
        particle_manager.add_system(200, 2)
        particle_manager.add_system(200, 3)
    
    return particle_manager