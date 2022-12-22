from enums import Color
import pygame
from button import Button
USEREVENT = pygame.locals.USEREVENT
class Timer:
    time_a = 300  # 5 minutes
    time_b = 300
    a_on = False
    b_on = False
    screen = None
    clock = None

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

    def set_time(self, time):
        self.time_a = time
        self.time_b = time

    def turn_a(self):
        if not self.b_on:
            # Set for 1 second (1000 milliseconds)
            pygame.time.set_timer(USEREVENT, 1000)
            self.a_on = True
        else:
            # The other one should turn on immediately
            pygame.time.set_timer(USEREVENT + 1, 0)
            pygame.time.set_timer(USEREVENT, 1000)
            self.a_on = True
            self.b_on = False

    def turn_b(self):
        if not self.a_on:
            # Set for 1 second (1000 milliseconds)
            pygame.time.set_timer(USEREVENT + 1, 1000)
            self.b_on = True
        else:
            # The other one should turn on immediately
            pygame.time.set_timer(USEREVENT, 0)
            pygame.time.set_timer(USEREVENT + 1, 1000)
            self.b_on = True
            self.a_on = False

    def display(self):
        time_a_str = "%d:%02d" % (int(self.time_a / 60), int(self.time_a % 60))
        time_b_str = "%d:%02d" % (int(self.time_b / 60), int(self.time_b % 60))

        button_a = Button(pygame.Rect(200, 310, 100, 100), time_a_str, pygame.font.Font(None, 36), Color.orange, Color.black)
        button_b = Button(pygame.Rect(400, 310, 100, 100), time_b_str, pygame.font.Font(None, 36), Color.orange, Color.black)
        #button_a = Button(100, 100, self.screen, Color.orange, Color.black)
        #button_b = Button(100, 100, self.screen, Color.orange, Color.black)
        button_a.draw(self.screen)
        button_b.draw(self.screen)
        pygame.display.update()
