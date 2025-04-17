import numpy as np
import pygame as pg
from collections import defaultdict

from particle_schema import PARTICLE_TYPES, PARTICLE_INTERACTIONS

DRAG = 0.1
MIN_DISTANCE = 0.4
MAX_DISTANCE = 60
FORCE_FACTOR = 0.002
GRID_SIZE = MAX_DISTANCE * 1.25

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

    p1_pos_array = np.array([p.pos for p in p1_list])  # Particle 1 positions
    p2_pos_array = np.array([p.pos for p in p2_list])  # Particle 2 positions

    directions_array = p1_pos_array - p2_pos_array 
    distance_sqs_array = np.sum(directions_array * directions_array, axis=1)

    mask = distance_sqs_array <= MAX_DISTANCE**2

    directions_array = directions_array[mask]
    distance_sqs_array = distance_sqs_array[mask]

    p1_list = [item for i, item in enumerate(p1_list) if mask[i]]
    p2_list = [item for i, item in enumerate(p2_list) if mask[i]]

    p1_types = np.array([p.ptype for p in p1_list])
    p2_types = np.array([p.ptype for p in p2_list])


    distances_array = np.sqrt(distance_sqs_array)
    unit_vectors = np.where(distances_array[:, None] > 0, directions_array / distances_array[:, None], 0)

    g_1_values = np.array([PARTICLE_INTERACTIONS[p1][p2] for p1, p2 in zip(p1_types, p2_types)])
    g_2_values = np.array([PARTICLE_INTERACTIONS[p2][p1] for p1, p2 in zip(p1_types, p2_types)])

    normalised_distances = distances_array / MAX_DISTANCE

    force_mags_1 = force_function(normalised_distances, g_1_values)
    force_mags_2 = force_function(normalised_distances, g_2_values)

    forces_1 = force_mags_1[:, None] * unit_vectors * MAX_DISTANCE * FORCE_FACTOR
    forces_2 = force_mags_2[:, None] * unit_vectors * MAX_DISTANCE * FORCE_FACTOR
    
    for p1, p2, f1, f2 in zip(p1_list, p2_list, forces_1, forces_2):
        p1.acc -= f1
        p2.acc += f2


def force_function(distances, g_values):
    MAX_FORCE_DISTANCE = (MIN_DISTANCE + 1) / 2

    forces = np.zeros_like(distances)

    # Zone 1: distance <= MIN_DISTANCE
    mask1 = distances <= MIN_DISTANCE
    forces[mask1] = (distances[mask1] / MIN_DISTANCE) - 1

    # Zone 2: MIN_DISTANCE < distance <= MAX_FORCE_DISTANCE
    mask2 = (distances > MIN_DISTANCE) & (distances <= MAX_FORCE_DISTANCE)
    forces[mask2] = g_values[mask2] / (MAX_FORCE_DISTANCE - MIN_DISTANCE) * (distances[mask2] - MIN_DISTANCE)

    # Zone 3: MAX_FORCE_DISTANCE < distance <= 1
    mask3 = (distances > MAX_FORCE_DISTANCE) & (distances <= 1)
    forces[mask3] = g_values[mask3] / (1 - MAX_FORCE_DISTANCE) * (1 - distances[mask3])

    # Zone 4: distance > 1 — forces remain 0
    return forces