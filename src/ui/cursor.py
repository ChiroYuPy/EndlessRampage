import pygame

class Cursor:
    def __init__(self, game):
        self.game = game
        self.size = 20
        self.outer_color = (127, 197, 169)
        self.middle_color = (198, 197, 169)
        self.inner_color = (255, 0, 0)
        self.line_color = (127, 197, 169)

    def draw(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.draw_outer_circle(screen, mouse_x, mouse_y)
        self.draw_middle_circle(screen, mouse_x, mouse_y)
        self.draw_inner_circle(screen, mouse_x, mouse_y)
        self.draw_crosshair(screen, mouse_x, mouse_y)

    def draw_outer_circle(self, screen, x, y):
        pygame.draw.circle(screen, self.middle_color, (x, y), int(self.size), width=1)

    def draw_middle_circle(self, screen, x, y):
        pygame.draw.circle(screen, self.outer_color, (x, y), int(self.size/8), width=1)

    def draw_inner_circle(self, screen, x, y):
        pygame.draw.circle(screen, self.inner_color, (x, y), int(self.size/1.8), width=1)

    def draw_crosshair(self, screen, x, y):
        pygame.draw.line(screen, self.line_color, (x + 6, y), (x + 24, y), 1)
        pygame.draw.line(screen, self.line_color, (x - 6, y), (x - 24, y), 1)
        pygame.draw.line(screen, self.line_color, (x, y + 6), (x, y + 24), 1)
        pygame.draw.line(screen, self.line_color, (x, y - 6), (x, y - 24), 1)
