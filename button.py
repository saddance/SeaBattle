import pygame


class CoolButton:
    def __init__(self, length: int, width: int, screen,
                 active_color=pygame.Color(190, 190, 170),
                 inactive_color=pygame.Color(190, 190, 210),
                 ):
        self.length = length
        self.width = width
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.was_click = False
        self.screen = screen

    def draw_button(self, x: float, y: float,
                    text: str = '', text_size: int = 0,
                    centering: list = (0, 0)):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (x < mouse_pos[0] < x + self.length) \
                and (y < mouse_pos[1] < y + self.width):
            pygame.draw.rect(self.screen, self.active_color,
                             (x, y, self.length, self.width))
            print_text(self.screen,text,
                       x + centering[0],
                       y + centering[1],
                       text_size)
            if click[0]:
                self.was_click = True
                return False
            else:
                if self.was_click:
                    self.was_click = False
                    return True
                return False

        else:
            pygame.draw.rect(self.screen, self.inactive_color,
                             (x, y, self.length, self.width))
            print_text(self.screen,
                       text,
                       x + centering[0],
                       y + centering[1],
                       text_size,
                       )

        return False



class Button:
    def __init__(self, rect, text, font, color, text_color):
        self.rect = rect
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text = self.font.render(self.text, True, self.text_color)
        screen.blit(text, (self.rect.x + self.rect.width / 2 - text.get_width() / 2,
                           self.rect.y + self.rect.height / 2 - text.get_height() / 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def wait_for_click(self):
        while True:
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_clicked(event.pos):
                    return
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def print_text(screen, message, x, y,
               size_font=30,
               font_color=(0, 0, 0),
               font_type=None):
    font_size = size_font
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))
