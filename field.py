from collections import defaultdict
from enums import Cell, Turn_result
from queue import Queue


class Field:

    def __init__(self, size):
        self.size = size
        self.map = [[Cell.empty for _ in range(size)] for _ in range(size)]
        self.radar = [[Cell.empty for _ in range(size)] for _ in range(size)]
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def make_shoot(self, x, y) -> Turn_result:
        if not self.is_valid(x, y):
            return Turn_result.incorrect
        cell = self.map[y][x]
        if cell == Cell.empty or cell == Cell.space:
            self.map[y][x] = Cell.miss
            return Turn_result.miss
        if cell == Cell.destroyed or cell == Cell.miss or cell == Cell.damaged:
            return Turn_result.incorrect
        if cell == Cell.undamaged:
            self.map[y][x] = Cell.damaged
            return self.check_damage(x, y)

    def get_ship(self, x, y):
        queue = Queue()
        used = defaultdict(bool)
        queue.put((x, y))
        used[(x, y)] = True
        result = []
        while not queue.empty():
            qx, qy = queue.get()
            result.append((qx, qy))
            for i, j in self.directions:
                new_x, new_y = qx + i, qy + j
                if self.is_valid(new_x, new_y) and not used[(new_x, new_y)]:
                    if self.map[new_y][new_x] == Cell.damaged \
                            or self.map[new_y][new_x] == Cell.destroyed\
                            or self.map[new_y][new_x] == Cell.undamaged:
                        queue.put((new_x, new_y))
                        result.append((new_x, new_y))
                        used[(new_x, new_y)] = True
        return result

    def check_damage(self, x, y):
        ship = self.get_ship(x, y)
        for x, y in ship:
            if self.map[y][x] == Cell.undamaged:
                return Turn_result.hit
        for x, y in ship:
            self.map[y][x] = Cell.destroyed
        return Turn_result.kill

    def mark_neighbours(self, ship: list[tuple[int, int]]):
        for x, y in ship:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    new_x, new_y = x + i, y + j
                    if self.is_valid(new_x, new_y) and self.radar[new_y][new_x] == Cell.empty:
                        self.radar[new_y][new_x] = Cell.space

    def write_result(self, x, y, turn_result):
        if turn_result == Turn_result.kill:
            ship = self.get_ship(x, y)
            self.mark_neighbours(ship)
            for x, y in ship:
                self.radar[y][x] = Cell.destroyed
        if turn_result == Turn_result.miss:
            self.radar[y][x] = Cell.miss
        if turn_result == Turn_result.incorrect:
            pass
        if turn_result == Turn_result.hit:
            self.radar[y][x] = Cell.damaged

    def is_valid(self, x, y) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size

    def ship_fits(self, ship):
        for x, y in ship.coords:
            if not self.is_valid(x, y):
                return False
            if self.map[y][x] != Cell.empty:
                return False
        return True

    def add_ship(self, ship):
        for x, y in ship.coords:
            self.map[y][x] = Cell.undamaged
            for i in range(-1, 2):
                for j in range(-1, 2):
                    new_x, new_y = x + i, y + j
                    if self.is_valid(new_x, new_y) and self.map[new_y][new_x] == Cell.empty\
                            and (new_x, new_y) not in ship.coords:
                        self.map[new_y][new_x] = Cell.space

    def __str__(self):
        result = ''
        for i in range(self.size):
            for cell in self.map[i]:
                result += str(cell.value)
            result += ' '
            for cell in self.map[i]:
                result += str(cell.value)
            result += '\n'
        return result

    def __repr__(self):
        return self.__str__()
