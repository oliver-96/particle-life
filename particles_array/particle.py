import pygame
import numpy as np
from collections import defaultdict

from sim_config.setup_schema import SIM_WIDTH, SIM_HEIGHT, DRAG, MAX_DISTANCE, RADIUS, DT, FORCE_FACTOR
from particles_array.particle_schema import PARTICLE_INTERACTIONS, PARTICLE_TYPES
from particles_array.particle_force_calc import calculate_forces

GRID_SIZE = MAX_DISTANCE * 1.25
NEIGHTBOUR_OFFSET = [(1,-1), (1,0), (1,1),(0,1)]

max_width_cell = int(SIM_WIDTH // GRID_SIZE) - 1
max_height_cell = int(SIM_HEIGHT // GRID_SIZE) - 1


class ParticleSystems:

    grid = defaultdict(list)

    def __init__(self):
        self.pos = np.empty((0, 2), dtype=np.float32)
        self.vel = np.empty((0, 2), dtype=np.float32)
        self.acc = np.empty((0, 2), dtype=np.float32)
        self.system_type = np.empty(0, dtype=int)
        self.pair_indicies = ()

    def add_system(self, number_of_particles, system_type, testing=False):
        if testing:
            x_list, y_list = self.get_testing_positions(number_of_particles)
            pos_array = np.column_stack((x_list, y_list))
            number_of_particles = len(x_list)
        else:
            pos_array = np.random.rand(number_of_particles, 2) * [SIM_WIDTH, SIM_HEIGHT]

        vel_array = np.zeros((number_of_particles, 2))
        acc_array = np.zeros((number_of_particles, 2))
        system_type_array = np.full(number_of_particles, system_type)

        self.pos = np.vstack([self.pos, pos_array])
        self.vel = np.vstack([self.vel, vel_array])
        self.acc = np.vstack([self.acc, acc_array])
        self.system_type = np.concatenate([self.system_type, system_type_array])

        self.pair_indicies = np.triu_indices(len(self.pos), k=1)


    def get_testing_positions(self, number_of_particles):
        grid_size = int(np.sqrt(number_of_particles))  
        spacing_x = SIM_WIDTH // grid_size          
        spacing_y = SIM_HEIGHT // grid_size        
            
        x_list = []
        y_list = []
        for i in range(grid_size):
            for j in range(grid_size):
                x = i * spacing_x + spacing_x // 2 
                y = j * spacing_y + spacing_y // 2 

                x_list.append(x)
                y_list.append(y)

        return x_list, y_list

    def update_particles(self):
        drag_force = self.vel**2 * DRAG * np.sign(self.vel) * -1

        self.acc += drag_force
        self.vel += self.acc * DT
        self.pos += self.vel * DT

        self.acc[:] = 0

    def apply_boundary_conditions(self):
        for dim, limit in enumerate([SIM_WIDTH, SIM_HEIGHT]):
            self.pos[:, dim] = np.mod(self.pos[:, dim], limit)

    def get_grid_position(self):
        ParticleSystems.grid.clear()
        grid_position = np.floor(self.pos / GRID_SIZE).astype(int)

        for i in range(len(self.pos)):
            ParticleSystems.grid[tuple(grid_position[i])].append(i)
        
    def check_interactions(self):
        self.get_grid_position()

        i_indices = []
        j_indices = []


        for (gx, gy), cell_particles in ParticleSystems.grid.items():
            for i in cell_particles:
                for j in cell_particles:
                    if i < j:
                        i_indices.append(i)
                        j_indices.append(j)

            for dx, dy in NEIGHTBOUR_OFFSET:

                neighbour_x = gx + dx
                neighbour_y = gy + dy

                if neighbour_x > max_width_cell:
                    neighbour_x = 0
                if neighbour_y > max_height_cell:
                    neighbour_y = 0
                if neighbour_y < 0:
                    neighbour_y = max_height_cell

                neighbour_cell = (neighbour_x, neighbour_y)
                
                if neighbour_cell not in ParticleSystems.grid:
                    continue
                neighbour_particles = ParticleSystems.grid[neighbour_cell]

                i_length = len(neighbour_particles)
                for i in cell_particles:
                    [i] * i_length
                    i_indices.extend([i] * i_length)
                    j_indices.extend(neighbour_particles)
        
        if not i_indices:
            return

        i_indices = np.array(i_indices)
        j_indices = np.array(j_indices)

        self.calculate_distance(i_indices, j_indices)
    

    def calculate_distance(self, i_indices, j_indices):

        pos1 = self.pos[i_indices]
        pos2 = self.pos[j_indices]
        directions = pos1 - pos2

        directions[:, 0] -= np.round(directions[:, 0] / SIM_WIDTH) * SIM_WIDTH
        directions[:, 1] -= np.round(directions[:, 1] / SIM_HEIGHT) * SIM_HEIGHT

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

        force_mags_1 = calculate_forces(normalised_distances, g_1_values)
        force_mags_2 = calculate_forces(normalised_distances, g_2_values)

        force_1 = force_mags_1[:, None] * unit_vectors * MAX_DISTANCE * FORCE_FACTOR
        force_2 = force_mags_2[:, None] * unit_vectors * MAX_DISTANCE * FORCE_FACTOR

        np.add.at(self.acc, i_indices, -force_1)
        np.add.at(self.acc, j_indices, +force_2)
 

    def draw_particles(self, screen):
        for i in range(len(self.pos)):
            colour = PARTICLE_TYPES[self.system_type[i]]['colour']
            pygame.draw.circle(screen, colour, self.pos[i], RADIUS)
