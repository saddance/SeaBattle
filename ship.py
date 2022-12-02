from enums import Cell
class Ship:

    def __init__(self, size, x, y, rotation):
        self.coords = []
        for i in range(size):
            if rotation == 0:
                self.coords.append((x + i, y))
            elif rotation == 1:
                self.coords.append((x, y + i))
            elif rotation == 2:
                self.coords.append((x - i, y))
            elif rotation == 3:
                self.coords.append((x, y - i))
