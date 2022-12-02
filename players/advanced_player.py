from enums import Cell
from players.player import Player
import random

class Advanced_player(Player):
    def __init__(self):
        super().__init__()

    def shoot(self):
        weights = [[0 for _ in range(10)] for _ in range(10)]
        for x in range(10):
            for y in range(10):
                if self.field.radar[y][x] == Cell.empty:
                    weights[y][x] = self.get_weight(x, y)
        max_weight = max(max(weights))
        max_weight_coords = [(x, y) for y in range(10) for x in range(10) if weights[y][x] == max_weight]
        return random.choice(max_weight_coords)

    def get_weight(self, x, y):
        weight = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_x, new_y = x + i, y + j
                if self.field.is_valid(new_x, new_y) and self.field.radar[new_y][new_x] == Cell.empty:
                    weight += 1
        for direction in self.field.directions:
            new_x, new_y = x + direction[0], y + direction[1]
            if self.field.is_valid(new_x, new_y) and self.field.radar[new_y][new_x] == Cell.damaged:
                weight += 10
        return weight
