import numpy as np
import pygame as pg
from particle_schema import PARTICLE_TYPES, PARTICLE_INTERACTIONS

DRAG = 0.1

class Particle:
    particle_list = []

    def __init__(self, x, y, ptype):
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([0, 0], dtype=float)
        self.acc = np.array([0, 0], dtype=float)

        self.ptype = ptype
        self.colour = PARTICLE_TYPES[ptype]['colour']
        self.radius = PARTICLE_TYPES[ptype]['radius']
        self.mass = PARTICLE_TYPES[ptype]['mass']

        Particle.particle_list.append(self)

    def update(self):
        drag_force = self.vel**2 * DRAG * np.sign(self.vel) * -1
        self.acc += drag_force
        self.vel += (self.acc )
        self.pos += self.vel
        self.acc *= 0

    def boundary(self, width, height):

        if self.pos[0] < self.radius:
            self.pos[0] = self.radius
            self.vel[0] *= -1

        if self.pos[0] > width - self.radius:
            self.pos[0] = width - self.radius
            self.vel[0] *= -1
        
        if self.pos[1] < self.radius:
            self.pos[1] = self.radius
            self.vel[1] *= -1
        
        if self.pos[1] > height - self.radius:
            self.pos[1] = height - self.radius
            self.vel[1] *= -1
        
    
    def draw(self, screen):
        pg.draw.circle(screen, self.colour, self.pos, self.radius)


def particle_rules(Particle):

    min_distance = 10
    max_distance = 100
    space = 20

    for i in range(len(Particle.particle_list)):
        for j in range(i+1, len(Particle.particle_list)):
            particle_1 = Particle.particle_list[i]
            particle_2 = Particle.particle_list[j]

            g_1 = PARTICLE_INTERACTIONS[particle_1.ptype][particle_2.ptype]
            g_2 = PARTICLE_INTERACTIONS[particle_2.ptype][particle_1.ptype]

            # Calculate distance between particles
            direction = particle_1.pos - particle_2.pos
            distance = np.linalg.norm(direction)

            if distance < min_distance:
                distance = min_distance
            
            unit_vector = direction / distance if distance != 0 else np.array([0, 0], dtype=float)

            if distance > max_distance:
                g_1 = 0
                g_2 = 0

            separation = distance - (particle_1.radius + particle_2.radius + space)

            if separation < 0:
                g_1 = -1
                g_2 = -1

                    # Calculate force of gravity
            force_1 =  ((particle_1.mass * particle_2.mass) / distance) * unit_vector * g_1
            force_2 =  ((particle_1.mass * particle_2.mass) / distance) * unit_vector * g_2


            # Apply force to particles
            particle_1.acc -= force_1 / particle_1.mass
            particle_2.acc += force_2 / particle_2.mass

    



