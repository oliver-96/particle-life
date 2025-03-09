import pygame as pg
import numpy as np
import random

from particles import Particle, particle_rules

# Initialize pygame
pg.init()

# Screen settings
WIDTH, HEIGHT = 400, 400
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Particle Life")


for _ in range (30):
    Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT), 'type_1')

for _ in range (50):
    Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT), 'type_2')

for _ in range (50):
    Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT), 'type_3')



# Main loop
running = True
clock = pg.time.Clock()
while running:

    screen.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    particle_rules(Particle)

    for particle in Particle.particle_list:
        particle.update()
        particle.boundary(WIDTH, HEIGHT)
        particle.draw(screen)
    
    print(f"FPS: {clock.get_fps():.2f}")
    pg.display.flip()
    clock.tick(60)  # 60 FPS

pg.quit()
