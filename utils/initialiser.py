from particles.particle import Particle

def initialise_particles(testing=False):
    if testing:
        num_particles = 675
        Particle.create_particles_testing(num_particles)
    else:
        Particle.create_particles(150, 'type_0')
        Particle.create_particles(150, 'type_1')
        Particle.create_particles(150, 'type_2')
        Particle.create_particles(150, 'type_3')