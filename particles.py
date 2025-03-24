import numpy as np
import pygame as pg
from collections import defaultdict

from particle_schema import PARTICLE_TYPES, PARTICLE_INTERACTIONS

DRAG = 0.1
min_distance = 10
max_distance = 60
force_factor = 0.002
space = 20
GRID_SIZE = max_distance * 1.25

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
        REBOUND = 2

        if self.pos[0] < self.radius:
            self.pos[0] = self.radius
            self.vel[0] *= -1 * REBOUND

        if self.pos[0] > width - self.radius:
            self.pos[0] = width - self.radius
            self.vel[0] *= -1 * REBOUND
        
        if self.pos[1] < self.radius:
            self.pos[1] = self.radius
            self.vel[1] *= -1 * REBOUND
        
        if self.pos[1] > height - self.radius:
            self.pos[1] = height - self.radius
            self.vel[1] *= -1 * REBOUND
        
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

    interactions = []  

    for (gx, gy), cell_particles in Particle.grid.items():
        num_particles = len(cell_particles)
        
        # Intra-cell interactions
        for i in range(num_particles):
            for j in range(i + 1, num_particles):
                p1, p2 = cell_particles[i], cell_particles[j]

                interactions.append((p1, p2))

        # Interactions with neighboring cells

        for dx, dy in [(1,-1), (1,0), (1,1),(0,1)]:
            neighbour_pos = (gx + dx, gy + dy)
            if neighbour_pos not in Particle.grid:
                continue

            neighbour_particles = Particle.grid[neighbour_pos]

            for p1 in cell_particles:
                for p2 in neighbour_particles:
                    interactions.append((p1, p2))


    if not interactions:
        return 

    p1_list, p2_list = zip(*interactions)

    p1_array = np.array([p.pos for p in p1_list])  # Particle 1 positions
    p2_array = np.array([p.pos for p in p2_list])  # Particle 2 positions


    p1_types = np.array([p.ptype for p in p1_list])
    p2_types = np.array([p.ptype for p in p2_list])
    directions_array = p1_array - p2_array 
    distance_sqs_array = np.sum(directions_array * directions_array, axis=1)
    mask = distance_sqs_array <= max_distance**2
    directions_array = directions_array[mask]
    distance_sqs_array = distance_sqs_array[mask]
    p1_types = p1_types[mask]
    p2_types = p2_types[mask]  
    p1_list = [item for i, item in enumerate(p1_list) if mask[i]]
    p2_list = [item for i, item in enumerate(p2_list) if mask[i]]


    distances_array = np.sqrt(distance_sqs_array)
    unit_vectors = np.where(distances_array[:, None] > 0, directions_array / distances_array[:, None], 0)

    g_1_values = np.array([PARTICLE_INTERACTIONS[p1][p2] for p1, p2 in zip(p1_types, p2_types)])
    g_2_values = np.array([PARTICLE_INTERACTIONS[p2][p1] for p1, p2 in zip(p1_types, p2_types)])

    normalised_distances = distances_array / max_distance

    force_mags_1 = np.vectorize(force_function)(normalised_distances, g_1_values)
    force_mags_2 = np.vectorize(force_function)(normalised_distances, g_2_values)

    forces_1 = force_mags_1[:, None] * unit_vectors * max_distance * force_factor
    forces_2 = force_mags_2[:, None] * unit_vectors * max_distance * force_factor

    for i in range(len(p1_list)):
        p1_list[i].acc -= forces_1[i]
        p2_list[i].acc += forces_2[i]


def force_function(distance, g):
    MIN_DISTANCE = 0.4
    MAX_FORCE_DISTANCE = (MIN_DISTANCE + 1) / 2


    if distance <= MIN_DISTANCE:
        return (distance / MIN_DISTANCE) - 1

    elif distance <= MAX_FORCE_DISTANCE:
        return g / (MAX_FORCE_DISTANCE - MIN_DISTANCE) * (distance - MIN_DISTANCE)
    
    elif distance <= 1:
        return g / (1 - MAX_FORCE_DISTANCE) * (1 - distance)
    
    else:
        return 0