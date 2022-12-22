import pickle

import pygame
import pygame_menu
import game
import players

from enums import Color
from parameters import Parameters


class Menu:
    screen: pygame.Surface
    game = None

    def set_up_drawer(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((800, 600))
        background = pygame.Surface(self.screen.get_size())
        background.fill(Color.orange)
        self.screen.blit(background, (0, 0))

    def show_menu(self):
        menu = pygame_menu.Menu('Welcome', 800, 600,
                                theme=pygame_menu.themes.THEME_BLUE)
        menu.add.button('Play', self.play)
        menu.add.button('Load', self.load)
        menu.add.button('Parametrize field', self.parametrize_menu())
        menu.add.selector('Opponent :', [('Stupid bot', 1), ('Medium bot', 2), ('Human', 3)],
                          onchange=self.choose_opponent)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.screen)

    def load(self):
        try:
            with open('save.pickle', 'rb') as file:
                self.game = pickle.load(file)
        except FileNotFoundError:
            return

    def play(self):
        if self.game is None:
            self.game = game.Game(self.screen)
        self.game.play()

    @staticmethod
    def choose_field_size(value, id):
        Parameters.field_size = int(value[0][0])
        print(Parameters.field_size)

    @staticmethod
    def choose_ship_sizes(value, id):
        Parameters.ship_sizes = [int(x) for x in value[0][0].split(' ')]

    @staticmethod
    def choose_opponent(value, id):
        selected, index = value
        Parameters.second_player = selected[0]
        if selected[0] == 'Human':
            Parameters.opponent_is_human = True

    @staticmethod
    def choose_placement(value, id):
        text = value[0][0]
        if text == 'Yes':
            Parameters.placement = 'random'
        else:
            Parameters.placement = 'normal'

    @staticmethod
    def choose_time(value):
        Parameters.time_limit = value

    def parametrize_menu(self):
        menu = pygame_menu.Menu('Parametrize', 800, 600,
                                theme=pygame_menu.themes.THEME_BLUE)
        menu.add.selector('Field size :', [('10', 1), ('5', 2), ('15', 3)],
                          onchange=self.choose_field_size)
        menu.add.selector('Ship sizes :',
                          [('1 1 1 1 2 2 2 3 3 4', 1), ('1 1 1 2 2', 2), ('1 1 1 1 1 1 2 2 2 2 2 3 3 3 4 4 5', 3)],
                          onchange=self.choose_ship_sizes)
        menu.add.selector('Random placement :', [('Yes', 1), ('No', 2)], onchange=self.choose_placement)
        menu.add.text_input('Time in seconds:', default='300', onchange=self.choose_time)
        menu.add.button('Back', pygame_menu.events.BACK)
        return menu
