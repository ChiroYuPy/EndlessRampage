import pygame
from ..graphics.ImageLoader import load_image


class Cursor:
    def __init__(self, renderer):
        self.renderer = renderer

        self.image = load_image("cursors/crosshair1.png", scale=2, color_key=(40, 120, 80))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.center = (mouse_x, mouse_y)
        screen.blit(self.image, self.rect)
