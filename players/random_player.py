from random import randint

from game import Game
from players.player import Player


class Random_player(Player):
    def __init__(self):
        super().__init__()

    def shoot(self):
        x = randint(0, Game.field_size - 1)
        y = randint(0, Game.field_size - 1)
        return x, y
