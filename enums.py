import enum
import pygame


@enum.unique
class Turn_result(enum.Enum):
    miss = 1
    hit = 2
    kill = 3
    incorrect = 4


class Color:
    white = pygame.Color(255, 255, 255)
    gray = pygame.Color(128, 128, 128)
    blue = pygame.Color(0, 0, 255)
    orange = pygame.Color(255, 128, 0)
    yellow = pygame.Color(255, 255, 0)
    red = pygame.Color(255, 0, 0)
    sea = pygame.Color(0, 144, 144)
    black = pygame.Color(0, 0, 0)

@enum.unique
class Cell(enum.Enum):
    empty = 0
    undamaged = 1
    damaged = 2
    destroyed = 3
    miss = 4
    space = 5


color = {
    Cell.empty: Color.white,
    Cell.undamaged: Color.blue,
    Cell.damaged: Color.yellow,
    Cell.destroyed: Color.red,
    Cell.miss: Color.black,
    Cell.space: Color.gray
}
