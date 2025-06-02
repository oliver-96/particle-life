import pygame as pg
import pygame_gui

from ui.ui_constants import *
from particles.particle_schema import PARTICLE_INTERACTIONS, PARTICLE_TYPES

class ParticleInteractionUI:
    def __init__ (self, matrix_size, manager, screen):
        self.matrix_size = matrix_size
        self.interaction_buttons = {}
        self.manager = manager
        self.screen = screen
        self.slider = None
        self.label = None
        self.selected_i = None
        self.selected_j = None
        self.particle_colour_1 = None
        self.particle_colour_2 = None

    def draw_ui_elements(self, particle_type_list):
        self.draw_particle_key(particle_type_list)
        self.draw_heat_map(particle_type_list)

    def create_button_grid(self):
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                rect = pg.Rect(button_start_x + j * CELL_SIZE, button_start_y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                btn = pygame_gui.elements.UIButton(
                    relative_rect=rect,
                    text='',
                    manager=self.manager,
                )
                self.interaction_buttons[(i, j)] = btn

    def button_interaction(self, event):
        slider_y = START_Y + CELL_SIZE * self.matrix_size * 2 + slider_y_offset
        colour_square_y = slider_y + colour_square_y_offset

        for (i, j), btn in self.interaction_buttons.items():
            if event.ui_element == btn:
                self.selected_i, self.selected_j = i, j
                current_value = PARTICLE_INTERACTIONS[i, j]
                self.particle_colour_1 = PARTICLE_TYPES[i]['colour']
                self.particle_colour_2 = PARTICLE_TYPES[j]['colour']
                if self.slider:
                    self.slider.kill()
                    self.label.kill()

                self.slider = pygame_gui.elements.UIHorizontalSlider(
                    relative_rect=pg.Rect((START_X - CELL_SIZE, slider_y), SLIDER_DIMENSIONS),
                    start_value=current_value,
                    value_range=(-1.0, 1.0),
                    manager=self.manager
                )
                
                self.label = pygame_gui.elements.UILabel(
                    relative_rect=pg.Rect((START_X + label_y_offset, slider_y + label_y_offset), LABEL_DIMENSIONS),
                    text=f'{current_value:.2f}',
                    manager=self.manager
                )

        if self.particle_colour_1:
            pg.draw.rect(self.screen, self.particle_colour_1, pg.Rect(START_X, colour_square_y, CELL_SIZE, CELL_SIZE))
            pg.draw.rect(self.screen, self.particle_colour_2, pg.Rect(START_X + CELL_SIZE * 1.2, colour_square_y, CELL_SIZE, CELL_SIZE))

    def silder_interaction(self, event, particle_type_list):

        if self.selected_i not in particle_type_list or self.selected_j not in particle_type_list:
            return
        
        PARTICLE_INTERACTIONS[self.selected_i, self.selected_j] = event.value
        self.label.set_text(f'{event.value:.2f}')
        new_color = self.value_to_colour(event.value)
        rect = pg.Rect(START_X + self.selected_j * CELL_SIZE, START_Y + self.selected_i * CELL_SIZE + map_y_offset, CELL_SIZE, CELL_SIZE)
        pg.draw.rect(self.screen, new_color, rect)
    
            
    def draw_particle_key(self, particle_type_list):

        # Draw row type colors - heat map
        self.draw_square_grid(self.matrix_size, 1, START_X - CELL_SIZE, START_Y + map_y_offset + map_spacing, particle_type_list, 'particle_matrix')

        # Draw column type colors - heat map
        self.draw_square_grid(1, self.matrix_size, START_X + map_spacing, START_Y + map_y_offset - CELL_SIZE, particle_type_list, 'particle_matrix')

    def draw_heat_map(self, particle_type_list):
        self.draw_square_grid(self.matrix_size, self.matrix_size, START_X + map_spacing, START_Y + map_y_offset + map_spacing, particle_type_list, 'heatmap')

    def draw_square_grid(self, row_number, column_number, START_X, START_Y, particle_type_list, colour_map):
        for i in range(row_number):
            for j in range(column_number):
                rect = pg.Rect(START_X + j * CELL_SIZE, START_Y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE)

                if colour_map == 'heatmap':
                    if i not in particle_type_list or j not in particle_type_list:
                        colour = (100, 100, 100)
                    else:
                        colour = self.value_to_colour(PARTICLE_INTERACTIONS[i, j])

                if colour_map == 'particle_matrix':
                    if row_number == 1:
                        k = j
                    else:
                        k = i

                    colour = PARTICLE_TYPES[k]['colour']

                pg.draw.rect(self.screen, colour, rect)

    @staticmethod
    def value_to_colour(value):
        if value < 0:
            red = int(255 * -value)
            return (red, 0, 0)
        else:
            green = int(255 * value)
            return (0, green, 0)