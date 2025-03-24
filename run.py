import pygame as pg
import numpy as np
import random
import argparse
import time



from particles import Particle, particle_rules_grid

WIDTH, HEIGHT = 600, 600

def initialize_particles(testing):
    if testing:
        num_particles = 500
        for _ in range(num_particles):

            Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT), 'type_0')

            grid_size = int(np.sqrt(num_particles))  
            spacing_x = WIDTH // grid_size          
            spacing_y = HEIGHT // grid_size        
            
            for i in range(grid_size):
                for j in range(grid_size):
                    if len(Particle.particle_list) >= num_particles:
                        return  
                    
                    x = i * spacing_x + spacing_x // 2 
                    y = j * spacing_y + spacing_y // 2
                    
                    Particle(x, y, 'type_0')

    else:

        # for _ in range(20):
        #     Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT), 'type_1')

        for _ in range(400):
            Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT), 'type_2')

        for _ in range(200):
            Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT), 'type_4')


def run(testing=False):
    # Initialize pygame
    pg.init()

    # Screen settings
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Particle Life")

    initialize_particles(testing)

    # Main loop
    running = True
    clock = pg.time.Clock()
    while running:

        screen.fill((0, 0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        particle_rules_grid(Particle)

        for particle in Particle.particle_list:

            particle.update()
            particle.boundary(WIDTH, HEIGHT)

            particle.draw(screen)

        
        
        print(f"FPS: {clock.get_fps():.2f}")
        pg.display.flip()
        clock.tick(60)  # 60 FPS

    pg.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="FPS testing mode")
    args = parser.parse_args()
    run(testing=args.test)

