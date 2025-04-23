import pygame as pg
import pygame_gui
import numpy as np
import random
import argparse

from particles import Particle, particle_rules_grid
from setup_schema import SIM_WIDTH, SIM_HEIGHT, UI_WIDTH
from particle_schema import PARTICLE_INTERACTIONS, PARTICLE_TYPES

HEIGHT = SIM_HEIGHT
WIDTH = SIM_WIDTH + UI_WIDTH

def initialize_particles(testing):
    if testing:
        num_particles = 675

        grid_size = int(np.sqrt(num_particles))  
        spacing_x = SIM_WIDTH // grid_size          
        spacing_y = SIM_HEIGHT // grid_size        
            
        for i in range(grid_size):
            for j in range(grid_size):
                x = i * spacing_x + spacing_x // 2 
                y = j * spacing_y + spacing_y // 2
                
                Particle(x, y, 'type_0')
            
    else:

        # for _ in range(150):
        #     Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT), 'type_0')

        for _ in range(40):
            Particle(random.randint(0, SIM_WIDTH), random.randint(0, SIM_HEIGHT), 'type_1')

        for _ in range(300):
            Particle(random.randint(0, SIM_WIDTH), random.randint(0, SIM_HEIGHT), 'type_2')

        # for _ in range(50):
        #     Particle(random.randint(0, SIM_WIDTH), random.randint(0, SIM_HEIGHT), 'type_3')

        # for _ in range(50):
        #     Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT), 'type_4')


def value_to_color(value):
    # Map -1 to red, 0 to white, 1 to green
    if value < 0:
        red = int(255 * -value)
        return (red, 0, 0)
    else:
        green = int(255 * value)
        return (0, green, 0)




pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Particle Life")

manager = pygame_gui.UIManager((WIDTH, HEIGHT))

def run(testing=False):

    initialize_particles(testing)

    interaction_buttons = {}

    matrix_size = len(PARTICLE_INTERACTIONS)
    cell_size = 25
    start_x, start_y = SIM_WIDTH + 50, 50
    screen.fill((40, 40, 40), rect=pg.Rect(SIM_WIDTH, 0, UI_WIDTH, HEIGHT))

    heatmap_surface = pg.Surface((UI_WIDTH, HEIGHT), pg.SRCALPHA)

    # Draw static heatmap colors
    for i in range(matrix_size):
        for j in range(matrix_size):
            value = PARTICLE_INTERACTIONS[i, j]
            color = value_to_color(value)
            rect = pg.Rect(start_x + j * cell_size, start_y + i * cell_size + 200, cell_size, cell_size)
            pg.draw.rect(screen, color, rect)

    for i in range(matrix_size):
        for j in range(matrix_size):
            rect = pg.Rect(start_x + j * cell_size, start_y + i * cell_size, cell_size, cell_size)
            btn = pygame_gui.elements.UIButton(
                relative_rect=rect,
                text='',
                manager=manager,
            )
            interaction_buttons[(i, j)] = btn

    # Draw column type colors
    for i in range(matrix_size):
        color = PARTICLE_TYPES[f"type_{i}"]['colour']        
        rect = pg.Rect(start_x + i * cell_size, start_y - cell_size + 5, cell_size, cell_size)
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, (0, 0, 0), rect, 1)

    # Draw row type colors
    for i in range(matrix_size):
        color = PARTICLE_TYPES[f"type_{i}"]['colour']  
        rect = pg.Rect(start_x - cell_size - 5, start_y + i * cell_size, cell_size, cell_size)
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, (0, 0, 0), rect, 1)


    # Main loop
    running = True
    clock = pg.time.Clock()
    selected_i, selected_j = None, None
    slider = None
    label = None
    particle_colour_1 = None
    particle_colour_2 = None

    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                for (i, j), btn in interaction_buttons.items():
                    if event.ui_element == btn:
                        selected_i, selected_j = i, j
                        current_value = PARTICLE_INTERACTIONS[i, j]
                        particle_colour_1 = PARTICLE_TYPES[f"type_{i}"]['colour']
                        particle_colour_2 = PARTICLE_TYPES[f"type_{j}"]['colour']
                        if slider:
                            slider.kill()
                            label.kill()

                        slider = pygame_gui.elements.UIHorizontalSlider(
                            relative_rect=pg.Rect((start_x, start_y + matrix_size * cell_size + 20), (180, 25)),
                            start_value=current_value,
                            value_range=(-1.0, 1.0),
                            manager=manager
                        )
                        label = pygame_gui.elements.UILabel(
                            relative_rect=pg.Rect((start_x + 175, start_y + matrix_size * cell_size + 20), (80, 30)),
                            text=f'{current_value:.2f}',
                            manager=manager
                        )
                
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                print(selected_i, selected_j)
                PARTICLE_INTERACTIONS[selected_i, selected_j] = event.value
                label.set_text(f'{event.value:.2f}')


                # Update heatmap cell color
                new_color = value_to_color(event.value)
                rect = pg.Rect(start_x + selected_j * cell_size, start_y + selected_i * cell_size +200, cell_size, cell_size)
                pg.draw.rect(screen, new_color, rect)

            if particle_colour_1:
                pg.draw.rect(screen, particle_colour_1, pg.Rect(start_x, start_y + matrix_size * cell_size + 50, cell_size, cell_size))
                pg.draw.rect(screen, particle_colour_2, pg.Rect(start_x + 30, start_y + matrix_size * cell_size + 50, cell_size, cell_size))


        

        # Sim background
        screen.fill((0, 0, 0), rect=pg.Rect(0, 0, SIM_WIDTH, HEIGHT))

        # UI background
        screen.fill((40, 40, 40), rect=pg.Rect(SIM_WIDTH + 240, 0, UI_WIDTH, HEIGHT))

        particle_rules_grid(Particle)

        for particle in Particle.particle_list:

            particle.update()
            particle.boundary(SIM_WIDTH, SIM_HEIGHT)

            particle.draw(screen)

        manager.update(time_delta)
        manager.draw_ui(screen)
        
        print(f"FPS: {clock.get_fps():.2f}")
        pg.display.flip()
        clock.tick(60)  # 60 FPS

    pg.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="FPS testing mode")
    args = parser.parse_args()

    run(testing=args.test)

