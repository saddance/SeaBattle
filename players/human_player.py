import pygame

import button
from enums import color, Color
from parameters import Parameters
from players.player import Player
from ship import Ship

USEREVENT = pygame.locals.USEREVENT


def draw_field(field, x, y, screen):
    # field = 250 * 250
    cell_size = 250 // Parameters.field_size
    for i in range(Parameters.field_size):
        for j in range(Parameters.field_size):
            pygame.draw.rect(screen, color[field[j][i]],
                             (x + cell_size * i, y + cell_size * j, cell_size, cell_size))
            pygame.draw.rect(screen, Color.red,
                             (x + cell_size * i, y + cell_size * j, cell_size, cell_size), 1)
    # pygame.display.flip()


def get_cell_in_cycle():
    while True:
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            cell_size = 250 // Parameters.field_size
            if (0 <= x < 250) and (0 <= y < 250):
                return x // cell_size, y // cell_size


def get_rotation(sx, sy, ex, ey):
    if sx == ex and sy == ey:
        return 0
    if sy == ey and sx < ex:
        return 0
    elif sx == ex and sy < ey:
        return 1
    elif sy == ey and sx > ex:
        return 2
    elif sx == ex and sy > ey:
        return 3


class Human_player(Player):
    def __init__(self):
        super().__init__()

    def shoot(self, timer=None):
        while True:
            if timer is not None:
                timer.display()
            event = pygame.event.wait()
            if event.type == USEREVENT:
                if timer.time_a > 0:
                    timer.time_a -= 1
                else:
                    pygame.time.set_timer(USEREVENT, 0)
            elif event.type == (USEREVENT + 1):
                if timer.time_b > 0:
                    timer.time_b -= 1
                else:
                    pygame.time.set_timer(USEREVENT, 0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                cell_size = 250 // Parameters.field_size
                if (550 <= x < 800) and (0 <= y < 250):
                    return (x - 550) // cell_size, y // cell_size

    def normal_placement(self, size):
        first_cell = get_cell_in_cycle()
        second_cell = get_cell_in_cycle()
        start_x, start_y = first_cell
        end_x, end_y = second_cell
        cur_size = abs(start_x - end_x) + abs(start_y - end_y) + 1
        if cur_size != size:
            return False
        if start_x == end_x or start_y == end_y:
            rotation = get_rotation(start_x, start_y, end_x, end_y)
            ship = Ship(size, start_x, start_y, rotation)
            if self.field.ship_fits(ship):
                self.field.add_ship(ship)
                return True
            else:
                return False
        else:
            return False

    def place_ships(self, screen):
        for size in Parameters.ship_sizes:
            while True:
                screen.fill(Color.orange)
                draw_field(self.field.map, 0, 0, screen)
                # wait 10 seconds
                # pygame.time.wait(10000)
                text = f'Place ship of size {size}'
                button.print_text(screen, text, 300, 0)
                if self.normal_placement(size):
                    break
                else:
                    continue
