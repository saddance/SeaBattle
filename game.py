import sys
import pygame
import pickle

import pygame_menu

import players.human_player
from enums import Turn_result, Color, color
from parameters import Parameters
from timer import Timer
from button import Button


class Game:
    screen: pygame.Surface
    buttons = []
    functions = []



    def __init__(self, screen):
        self.screen = screen
        self.players = []
        self.current_player = None
        self.next_player = None
        self.first_turn = True
        self.status = 'preparation'
        self.timer = Timer(screen)
        continue_button = Button(pygame.Rect(325, 400, 125, 50), 'Continue', pygame.font.Font(None, 36), Color.orange,
                                 Color.black)
        save_button = Button(pygame.Rect(325, 500, 125, 50), 'Save', pygame.font.Font(None, 36), Color.orange,
                             Color.black)
        self.buttons = [continue_button, save_button]
        self.functions = [self.do_nothing, self.save_game]

    def place_ships(self):
        for player in self.players:
            if isinstance(player, players.human_player.Human_player) and Parameters.placement == 'normal':
                player.place_ships(self.screen)
            else:
                player.random_ships_setup()

    def play(self):
        if self.status == 'preparation':
            self.prepare_game()
        while True:
            if isinstance(self.current_player, players.human_player.Human_player):
                self.draw_screen()
            if isinstance(self.current_player, players.human_player.Human_player):
                if isinstance(self.next_player, players.human_player.Human_player):
                    self.process_buttons(self.buttons, self.functions)
                else:
                    self.process_buttons(self.buttons[1:], self.functions[1:])
            turn_result = self.turn()
            if isinstance(self.current_player, players.human_player.Human_player):
                self.draw_screen()

            if turn_result == Turn_result.miss:
                self.switch_players()
            if self.next_player.ships_count == 0:
                self.status = 'finish'
                break
        self.final_stage()

    def final_stage(self):
        self.screen.fill(Color.orange)
        self.draw_field(self.next_player.field.radar, 0, 0)
        self.draw_field(self.current_player.field.radar, 550, 0)

        number = 1 if self.first_turn else 2
        self.print_text(f"Player {number} win", 350, 250)
        button = Button(pygame.Rect(325, 400, 125, 50), 'Back', pygame.font.Font(None, 36),
                        Color.orange, Color.black)
        button.draw(self.screen)
        pygame.display.flip()
        button.wait_for_click()
        return

    def draw_buttons(self, buttons):
        for button in buttons:
            button.draw(self.screen)
        pygame.display.flip()

    def process_buttons(self, buttons, functions):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(buttons)):
                    if buttons[i].rect.collidepoint(event.pos):
                        functions[i]()

    def do_nothing(self):
        return

    def prepare_game(self):
        switcher1 = {
            'Stupid bot': players.random_player.Random_player(),
            'Medium bot': players.advanced_player.Advanced_player(),
            'Human': players.human_player.Human_player()
        }
        switcher2 = {
            'Stupid bot': players.random_player.Random_player(),
            'Medium bot': players.advanced_player.Advanced_player(),
            'Human': players.human_player.Human_player()
        }
        self.add_player(switcher1[Parameters.first_player])
        self.add_player(switcher2[Parameters.second_player])
        self.current_player = self.players[0]
        self.next_player = self.players[1]
        self.timer.set_time(int(Parameters.time_limit))
        self.screen.fill(Color.orange)
        self.place_ships()
        self.status = 'play'

    def draw_field(self, field, x, y):
        # field = 250 * 250
        cell_size = 250 // Parameters.field_size
        for i in range(Parameters.field_size):
            for j in range(Parameters.field_size):
                pygame.draw.rect(self.screen, color[field[j][i]],
                                 (x + cell_size * i, y + cell_size * j, cell_size, cell_size))
                pygame.draw.rect(self.screen, Color.red,
                                 (x + cell_size * i, y + cell_size * j, cell_size, cell_size), 1)

    def draw_screen(self):
        cur_field = self.current_player.field.map
        next_field = self.current_player.field.radar
        self.screen.fill(Color.orange)
        self.draw_field(cur_field, 0, 0)
        self.draw_field(next_field, 550, 0)
        # write number of player on the screen
        number = 1 if self.first_turn else 2
        self.print_text(f"Player {number} turn", 350, 250)
        # add save button here
        pygame.display.flip()

    def print_text(self, txt, x, y):
        font = pygame.font.Font(None, 36)
        text = font.render(txt, True, Color.black)
        self.screen.blit(text, (x, y))

    def switch_players(self):
        self.current_player, self.next_player = self.next_player, self.current_player
        self.first_turn = not self.first_turn

    def add_player(self, player):
        self.players.append(player)

    @staticmethod
    def exit():
        pygame.quit()
        sys.exit()

    def turn(self):
        if self.first_turn:
            self.timer.turn_a()
        else:
            self.timer.turn_b()
        x, y = self.current_player.shoot(timer=self.timer)
        turn_result = self.next_player.make_shoot(x, y)
        if turn_result == Turn_result.kill:
            self.next_player.ships_count -= 1
        self.current_player.write_result(x, y, turn_result)
        return turn_result

    def save_game(self):
        # save game via pickle
        with open('save.pickle', 'wb') as f:
            pickle.dump(self, f)
