import pygame

from players.player import Player


class Human_player(Player):
    def __init__(self):
        super().__init__()

    def shoot(self):
        while True:
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if (550 <= x < 800) and (0 <= y < 250):
                    return (x - 550) // 25, y // 25
            else:
                continue
