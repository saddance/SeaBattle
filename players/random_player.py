from random import randint
from parameters import Parameters
from players.player import Player


class Random_player(Player):
    def __init__(self):
        super().__init__()

    def shoot(self, timer=None):
        x = randint(0, Parameters.field_size - 1)
        y = randint(0, Parameters.field_size - 1)
        return x, y
