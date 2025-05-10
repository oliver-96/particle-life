import pygame
import numpy as np
import sys
from numba import njit

WIDTH, HEIGHT = 700, 700
DT = 0.01
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RADIUS = 2
INITAL_VELOCITY = 0
MIN_DISTANCE = 0.3
MAX_DISTANCE = 80
DRAG = 0.05
FORCE_FACTOR = 5


colour_map = {
    0: WHITE,
    1: RED,
    2: GREEN,
    3: BLUE
}

PARTICLE_INTERACTIONS_DICT = {
    0: {
        0: 0.5,
        1: -0.1,
        2: 0,
        3: 0,
    },
    1: {
        0: 0.1,
        1: 0.5,
        2: 0.3,
        3: 0,
    },
    2: {
        0: 0,
        1: 0,
        2: 0.5,
        3: 0.3,
    },
    3: {
        0: 0,
        1: 0,
        2: 0,
        3: 0.5,
    },
}

sorted_particles_interaction_dict = sorted(PARTICLE_INTERACTIONS_DICT.keys()) 
PARTICLE_INTERACTIONS = np.array([[PARTICLE_INTERACTIONS_DICT[row][col] for col in sorted_particles_interaction_dict] for row in sorted_particles_interaction_dict])

class ParticleSystems:
    def __init__(self):
        self.pos = np.empty((0, 2), dtype=np.float32)
        self.vel = np.empty((0, 2), dtype=np.float32)
        self.acc = np.empty((0, 2), dtype=np.float32)
        self.system_type = np.empty(0, dtype=int)

    def add_system(self, number_of_particles, system_type):
        pos_array = np.random.rand(number_of_particles, 2) * [WIDTH, HEIGHT]
        vel_array = np.random.randn(number_of_particles, 2) * INITAL_VELOCITY
        acc_array = np.zeros((number_of_particles, 2))
        system_type_array = np.full(number_of_particles, system_type)

        self.pos = np.vstack([self.pos, pos_array])
        self.vel = np.vstack([self.vel, vel_array])
        self.acc = np.vstack([self.acc, acc_array])
        self.system_type = np.concatenate([self.system_type, system_type_array])

    def update_particles(self):
        drag_force = self.vel**2 * DRAG * np.sign(self.vel) * -1
        self.acc += drag_force

        self.vel += self.acc * DT
        self.pos += self.vel * DT

    def apply_boundary_conditions(self):
        for dim, limit in enumerate([WIDTH, HEIGHT]):
            self.pos[:, dim] = np.mod(self.pos[:, dim], limit)

    def calculate_distance(self):

        n = len(self.pos)
        i_indices, j_indices = np.triu_indices(n, k=1)

        pos1 = self.pos[i_indices]
        pos2 = self.pos[j_indices]
        directions = pos1 - pos2

        directions[:, 0] -= np.round(directions[:, 0] / WIDTH) * WIDTH
        directions[:, 1] -= np.round(directions[:, 1] / HEIGHT) * HEIGHT

        distance_sqs = np.einsum('ij,ij->i', directions, directions)

        mask = distance_sqs <= MAX_DISTANCE**2

        i_indices = i_indices[mask]
        j_indices = j_indices[mask]
        directions = directions[mask]
        distance_sqs = distance_sqs[mask]
        distance = np.sqrt(distance_sqs)

        unit_vectors = directions / distance[:, None]
        unit_vectors[distance == 0] = 0

        g_1_values = PARTICLE_INTERACTIONS[self.system_type[i_indices], self.system_type[j_indices]]
        g_2_values = PARTICLE_INTERACTIONS[self.system_type[j_indices], self.system_type[i_indices]]
        normalised_distances = distance / MAX_DISTANCE

        force_mags_1 = self.calculate_forces(normalised_distances, g_1_values)
        force_mags_2 = self.calculate_forces(normalised_distances, g_2_values)

        force_1 = force_mags_1[:, None] * unit_vectors * MAX_DISTANCE * FORCE_FACTOR
        force_2 = force_mags_2[:, None] * unit_vectors * MAX_DISTANCE * FORCE_FACTOR

        self.acc[:] = 0
        np.add.at(self.acc, i_indices, -force_1)
        np.add.at(self.acc, j_indices, +force_2)


    @njit
    def calculate_forces(self, normalised_distances, g_values):
        MAX_FORCE_DISTANCE = (MIN_DISTANCE + 1) / 2

        forces = np.zeros_like(normalised_distances)

        # Zone 1: distance <= MIN_DISTANCE
        mask1 = normalised_distances <= MIN_DISTANCE
        forces[mask1] = (normalised_distances[mask1] / MIN_DISTANCE) - 1

        # Zone 2: MIN_DISTANCE < distance <= MAX_FORCE_DISTANCE
        mask2 = (normalised_distances > MIN_DISTANCE) & (normalised_distances <= MAX_FORCE_DISTANCE)
        forces[mask2] = g_values[mask2] / (MAX_FORCE_DISTANCE - MIN_DISTANCE) * (normalised_distances[mask2] - MIN_DISTANCE)

        # Zone 3: MAX_FORCE_DISTANCE < distance <= 1
        mask3 = (normalised_distances > MAX_FORCE_DISTANCE) & (normalised_distances <= 1)
        forces[mask3] = g_values[mask3] / (1 - MAX_FORCE_DISTANCE) * (1 - normalised_distances[mask3])

        # Zone 4: distance > 1 — forces remain 0
        return forces

    def draw_particles(self, screen):
        for i in range(len(self.pos)):
            colour = colour_map[self.system_type[i]]
            pygame.draw.circle(screen, colour, self.pos[i], RADIUS)

particle_manager = ParticleSystems()

particle_manager.add_system(1000, 0)

# # --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


running = True
while running:
    screen.fill((0, 0, 0))
    # --- Handle events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Physics update ---

    particle_manager.update_particles()
    particle_manager.apply_boundary_conditions()
    particle_manager.calculate_distance()
    particle_manager.draw_particles(screen)
    
    pygame.display.flip()

    # --- Cap frame rate ---
    clock.tick(60)
    print(f"FPS: {clock.get_fps():.2f}")

pygame.quit()
sys.exit()
