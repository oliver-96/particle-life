import numpy as np
import pygame as pg
from collections import defaultdict

from particle_schema import PARTICLE_TYPES, PARTICLE_INTERACTIONS

DRAG = 0.1
min_distance = 10
max_distance = 100
force_factor = 0.001
space = 20
GRID_SIZE = max_distance * 1.25 / 2

class Particle:
    particle_list = []
    grid = defaultdict(list)


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
        
    def get_grid_pos(self):
        return (int(self.pos[0] // GRID_SIZE), int(self.pos[1] // GRID_SIZE))
    
    def draw(self, screen):
        pg.draw.circle(screen, self.colour, self.pos, self.radius)


def update_grid():
    Particle.grid.clear()
    for particle in Particle.particle_list:
        grid_pos = particle.get_grid_pos()
        Particle.grid[grid_pos].append(particle)



def particle_rules_grid(Particle):
    update_grid()
    checked_pairs = set()

    for (gx, gy), cell_particles in Particle.grid.items():

        for particle in cell_particles:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    neighbour_pos = (gx + dx, gy + dy)
                    for neighbour in Particle.grid.get(neighbour_pos, []):
                        if particle != neighbour and (particle, neighbour) not in checked_pairs:
                            particle_interaction(particle, neighbour)
                            checked_pairs.add((particle, neighbour))
                            checked_pairs.add((neighbour, particle))


def particle_interaction(particle_1, particle_2):
    g_1 = PARTICLE_INTERACTIONS[particle_1.ptype][particle_2.ptype]
    g_2 = PARTICLE_INTERACTIONS[particle_2.ptype][particle_1.ptype]

    # Calculate distance between particles
    direction = particle_1.pos - particle_2.pos
    distance = np.linalg.norm(direction)
    unit_vector = direction / distance if distance != 0 else np.array([0, 0], dtype=float)

    normalised_distance = distance / max_distance

    force_mag_1 = force_function(normalised_distance, g_1)
    force_mag_2 = force_function(normalised_distance, g_2)


    # if distance < min_distance:
    #     distance = min_distance
    
    # unit_vector = direction / distance if distance != 0 else np.array([0, 0], dtype=float)

    # if distance > max_distance:
    #     g_1 = 0
    #     g_2 = 0

    # separation = distance - (particle_1.radius + particle_2.radius + space)

    # if separation < 0:
    #     g_1 = -1
    #     g_2 = -1

            # Calculate force of gravity
    force_1 =  force_mag_1 * unit_vector * max_distance * force_factor
    force_2 =  force_mag_2 * unit_vector * max_distance * force_factor


    # Apply force to particles
    particle_1.acc -= force_1
    particle_2.acc += force_2


def force_function(distance, g):
    MIN_DISTANCE = 0.3
    MAX_FORCE_DISTANCE = (MIN_DISTANCE + 1) / 2


    if distance <= MIN_DISTANCE:
        force_mag = (distance / MIN_DISTANCE) - 1

    if distance > MIN_DISTANCE and distance <= MAX_FORCE_DISTANCE:
        force_mag = g / (MAX_FORCE_DISTANCE - MIN_DISTANCE) * (distance - MIN_DISTANCE)
    
    if distance > MAX_FORCE_DISTANCE and distance <= 1:
        force_mag = g / (1 - MAX_FORCE_DISTANCE) * (1 - distance)
    
    if distance > 1:
        force_mag = 0
    
    return force_mag
    



    



