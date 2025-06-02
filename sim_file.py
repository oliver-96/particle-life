import pygame as pg
import pygame_gui
import numpy as np
import time


from sim_config.setup_schema import SIM_WIDTH, SIM_HEIGHT, UI_WIDTH, RADIUS, FPS, DRAG, FORCE_FACTOR
from particles.particle_schema import PARTICLE_INTERACTIONS
from utils.initialiser import initialise_particles

HEIGHT = SIM_HEIGHT
WIDTH = SIM_WIDTH + UI_WIDTH
FORCE_STEP = 1
DRAG_STEP = 0.005

class SimState:
    def __init__(self):
        self.key_pressed = None
        self.drag = DRAG
        self.force_factor = FORCE_FACTOR

def setup_environment():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    return screen, manager

def handle_events(state):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_f:
                state.key_pressed = "F"
            if event.key == pg.K_d:
                state.key_pressed = "D"
            
            if event.key == pg.K_UP:
                if state.key_pressed == "F":
                    state.force_factor += FORCE_STEP
            
                if state.key_pressed == "D":
                    state.drag += DRAG_STEP
            
            if event.key == pg.K_DOWN:
                if state.key_pressed == "F":
                    state.force_factor = max(0, state.force_factor - FORCE_STEP)

                if state.key_pressed == "D":
                    state.drag = max(0, state.drag - DRAG_STEP)

            if event.key == pg.K_SPACE:
                PARTICLE_INTERACTIONS[:] = np.random.uniform(-1, 1, PARTICLE_INTERACTIONS.shape)

    return True

def run_sim(testing=False):
    screen, manager = setup_environment()
    particle_manager = initialise_particles(testing)
    state = SimState()

    running = True
    clock = pg.time.Clock()

    font = pg.font.SysFont(None, 20) 

    while running:

        start_time = time.time()

        running = handle_events(state)

        screen.fill((0, 0, 0), rect=pg.Rect(0, 0, SIM_WIDTH+RADIUS, HEIGHT))

        particle_manager.drag = state.drag
        particle_manager.force_factor = state.force_factor

        interacation_start_time = time.time()
        particle_manager.check_interactions()
        interacation_start_time = time.time()

        particle_manager.update_particles()
        particle_manager.apply_boundary_conditions()
        particle_manager.draw_particles(screen)

        
        print(f"FPS: {clock.get_fps():.2f}")
        pg.display.flip()
        clock.tick(FPS) 

        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.4f} seconds")
        print(f"Interaction time: {interacation_start_time - start_time:.4f} seconds")

    pg.quit()