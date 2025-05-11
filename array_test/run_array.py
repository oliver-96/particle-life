import pygame
import sys

from particle_array import ParticleSystems
from schema import WIDTH, HEIGHT

particle_manager = ParticleSystems()
particle_manager.add_system(1400, 0)
# particle_manager.add_system(300, 1)


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
    particle_manager.check_interactions()
    particle_manager.update_particles()
    particle_manager.apply_boundary_conditions()
    particle_manager.draw_particles(screen)
    
    pygame.display.flip()

    # --- Cap frame rate ---
    clock.tick(60)
    print(f"FPS: {clock.get_fps():.2f}")

pygame.quit()
sys.exit()
