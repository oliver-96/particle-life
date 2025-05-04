import numpy as np
import pygame as pg
import random
from collections import defaultdict

from particles.particle_schema import PARTICLE_TYPES
from sim_config.setup_schema import SIM_WIDTH, SIM_HEIGHT, DRAG, MAX_DISTANCE, RADIUS

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
        self.radius = RADIUS
        self.type = PARTICLE_TYPES[ptype]['type']

        Particle.particle_list.append(self)

    @classmethod
    def create_particles(cls, particle_count, ptype):
        for _ in range(particle_count):
            x = random.randint(0, SIM_WIDTH)
            y = random.randint(0, SIM_HEIGHT)
            cls(x, y, ptype)

    @classmethod
    def create_particles_testing(cls, particle_count):
        grid_size = int(np.sqrt(particle_count))  
        spacing_x = SIM_WIDTH // grid_size          
        spacing_y = SIM_HEIGHT // grid_size        
            
        for i in range(grid_size):
            for j in range(grid_size):
                x = i * spacing_x + spacing_x // 2 
                y = j * spacing_y + spacing_y // 2 
                cls(x, y, 'type_0')

    def update(self):
        drag_force = self.vel**2 * DRAG * np.sign(self.vel) * -1
        self.acc += drag_force

        self.vel += (self.acc )
        self.pos += self.vel
        self.acc *= 0

    def boundary(self, width, height):

        if self.pos[0] < 0:
            self.pos[0] = width

        if self.pos[0] > width:
            self.pos[0] = 0
        
        if self.pos[1] < 0:
            self.pos[1] = height
        
        if self.pos[1] > height:
            self.pos[1] = 0
        
    def get_grid_pos(self):
        return (int(self.pos[0] // GRID_SIZE), int(self.pos[1] // GRID_SIZE))
    
    def draw(self, screen):
        pg.draw.circle(screen, self.colour, self.pos, self.radius)