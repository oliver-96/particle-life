from particles.particle import ParticleSystems

def initialise_particles(testing=False):
    particle_manager = ParticleSystems()

    if testing:
        num_particles = 2000
        particle_manager.add_system(num_particles, 0, testing=True)
    else:
        particle_manager.add_system(100, 0)
        particle_manager.add_system(100, 1)
        particle_manager.add_system(100, 2)
        particle_manager.add_system(100, 3)
        particle_manager.add_system(100, 4)
        particle_manager.add_system(100, 5)
        particle_manager.add_system(100, 6)
        # particle_manager.add_system(100, 7)
        # particle_manager.add_system(100, 8)

    
    return particle_manager