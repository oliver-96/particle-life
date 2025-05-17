import pygame as pg
import pygame_gui
import numpy as np

from ui.ui_utils import ParticleInteractionUI
from sim_config.setup_schema import SIM_WIDTH, SIM_HEIGHT, UI_WIDTH, RADIUS, FPS
from particles.particle_schema import PARTICLE_INTERACTIONS
from utils.initialiser import initialise_particles

HEIGHT = SIM_HEIGHT
WIDTH = SIM_WIDTH + UI_WIDTH

def setup_environment():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    return screen, manager

def handle_events(particle_ui, particle_type_list, manager):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False
        
        manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            particle_ui.button_interaction(event)
            
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            particle_ui.silder_interaction(event, particle_type_list)
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                PARTICLE_INTERACTIONS[:] = np.random.uniform(-1, 1, PARTICLE_INTERACTIONS.shape)
                particle_ui.draw_heat_map(particle_type_list)

    return True

def run_sim(testing=False):
    screen, manager = setup_environment()
    particle_manager = initialise_particles(testing)

    particle_type_list = np.unique(particle_manager.system_type).tolist()

    matrix_size = len(PARTICLE_INTERACTIONS)
    screen.fill((40, 40, 40), rect=pg.Rect(SIM_WIDTH, 0, UI_WIDTH, HEIGHT))

    particle_ui = ParticleInteractionUI(matrix_size, manager, screen)
    particle_ui.draw_ui_elements(particle_type_list)


    running = True
    clock = pg.time.Clock()

    while running:
        time_delta = clock.tick(FPS) / 1000
        running = handle_events(particle_ui, particle_type_list, manager)

        screen.fill((0, 0, 0), rect=pg.Rect(0, 0, SIM_WIDTH+RADIUS, HEIGHT))
        screen.fill((40, 40, 40), rect=pg.Rect(SIM_WIDTH * 1.13, HEIGHT / 2.1, UI_WIDTH, HEIGHT))

        particle_manager.check_interactions()
        particle_manager.update_particles()
        particle_manager.apply_boundary_conditions()
        particle_manager.draw_particles(screen)

        manager.update(time_delta)
        manager.draw_ui(screen)
        
        print(f"FPS: {clock.get_fps():.2f}")
        pg.display.flip()
        clock.tick(FPS) 
    pg.quit()