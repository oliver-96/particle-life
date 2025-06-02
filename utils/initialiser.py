from particles.particle import ParticleSystems

def initialise_particles(testing=False):
    particle_manager = ParticleSystems()

    if testing:
        num_particles = 1500
        particle_manager.add_system(num_particles, 0, testing=True)
    else:
        particle_manager.add_system(600, 0)
        particle_manager.add_system(600, 1)
        particle_manager.add_system(600, 2)
        # particle_manager.add_system(300, 3)
        # particle_manager.add_system(300, 4)
        # particle_manager.add_system(150, 5)
        # particle_manager.add_system(150, 6)
    
    return particle_manager