import random
import time
from random import randint

from field import Field
from game import Game
from ship import Ship

class Player:

    def __init__(self):
        self.field = Field(Game.field_size)
        self.random_ships_setup()
        self.ships_count = len(Game.ship_sizes)
    
    def shoot(self):
        pass

    def setup_ships(self):
        pass

    def random_placement(self, size):
        while True:
            x = randint(0, Game.field_size - 1)
            y = randint(0, Game.field_size - 1)
            rotation = randint(0, 3)
            try_ship = Ship(size, x, y, rotation)
            if self.field.ship_fits(try_ship):
                return try_ship

    def random_ships_setup(self):
        for ship_size in Game.ship_sizes:
            self.field.add_ship(self.random_placement(ship_size))

    def make_shoot(self, x, y):
        return self.field.make_shoot(x, y)

    def write_result(self, x, y, result):
        self.field.write_result(x, y, result)



