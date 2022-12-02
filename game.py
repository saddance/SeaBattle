import sys
import pygame
import pygame_menu
from menu import Menu, Button
from enums import Turn_result, Color, color


class Game:
    ship_sizes = [1, 1, 1, 5, 2, 2, 2, 3, 3, 4]
    field_size = 10
    screen = None
    background = None

    def __init__(self):
        self.players = []
        self.current_player = None
        self.next_player = None

    def play(self):
        self.prepare_game()
        self.screen.fill(Color.orange)
        # self.set_up_drawer()
        while True:
            pygame.event.pump()
            if self.current_player == self.players[0]:
                self.draw_fields()
            turn_result = self.turn()
            if turn_result == Turn_result.kill:
                self.draw_fields()
            if turn_result == Turn_result.miss:
                self.switch_players()
            if self.next_player.ships_count == 0:
                self.exit()

    def set_up_drawer(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(Color.orange)
        self.screen.blit(self.background, (0, 0))

    def prepare_game(self):
        self.current_player = self.players[0]
        self.next_player = self.players[1]

    def draw_field(self, field, x, y):
        cell_size = 25
        for i in range(10):
            for j in range(10):
                pygame.draw.rect(self.screen, color[field[j][i]],
                                 (x + cell_size * i, y + cell_size * j, cell_size, cell_size))
                pygame.draw.rect(self.screen, Color.red,
                                 (x + cell_size * i, y + cell_size * j, cell_size, cell_size), 1)

    def draw_fields(self):
        cur_field = self.current_player.field.map
        next_field = self.current_player.field.radar
        self.draw_field(cur_field, 0, 0)
        self.draw_field(next_field, 550, 0)
        pygame.display.flip()

    def switch_players(self):
        self.current_player, self.next_player = self.next_player, self.current_player

    def add_player(self, player):
        self.players.append(player)

    def show_menu(self):
        self.set_up_drawer()
        '''menu = Menu(self.screen,
                    Button(300, 0, 200, 50, 'Start', self.play),
                    Button(300, 100, 200, 50, 'Choose Opponent', self.choose_opponent()),
                    Button(300, 200, 200, 50, 'Parametrize field', self.parametrize_field()),
                    Button(300, 300, 200, 50, 'Exit', self.exit))'''
        menu = pygame_menu.Menu('Welcome', 800, 600,
                                theme=pygame_menu.themes.THEME_BLUE)
        menu.add.button('Play', self.play)
        menu.add.button('Parametrize field', self.parametrize_field)
        menu.add.selector('Opponent :', [('Stupid bot', 1), ('Medium bot', 2), ('Human', 3)],
                          onchange=self.choose_opponent)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        print('ok')
        menu.mainloop(self.screen)



    def choose_opponent(self, obj, index, selected):
        pass
        # rand_button = Button(300, 0, 200, 50, 'Random', )
        # human_button = Button(300, 100, 200, 50, 'Human', )

    def parametrize_field(self):
        pass

    def exit(self):
        pygame.quit()
        sys.exit()

    def turn(self):
        x, y = self.current_player.shoot()
        turn_result = self.next_player.make_shoot(x, y)
        if turn_result == Turn_result.kill:
            self.next_player.ships_count -= 1
        self.current_player.write_result(x, y, turn_result)
        return turn_result
