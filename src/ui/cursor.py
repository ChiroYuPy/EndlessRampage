import pygame


class Cursor:
    def __init__(self, game):
        self.game = game

        self.scale_factor = 1.2
        self.color = (255, 255, 255)
        self.transparence = 127

        self.original_image = pygame.image.load("src/assets/images/cursors/crosshair1.png")
        self.crosshair_image = pygame.transform.scale(self.original_image,
                                                      (int(self.original_image.get_width() * self.scale_factor),
                                                       int(self.original_image.get_height() * self.scale_factor)))
        self.crosshair_rect = self.crosshair_image.get_rect()

        self.replace_black_pixels()

    def replace_black_pixels(self):
        for x in range(self.crosshair_image.get_width()):
            for y in range(self.crosshair_image.get_height()):
                pixel_color = self.crosshair_image.get_at((x, y))
                if pixel_color == (0, 0, 0, 255):
                    self.crosshair_image.set_at((x, y), self.color + (self.transparence,))

    def draw(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.crosshair_rect.center = (mouse_x, mouse_y)
        screen.blit(self.crosshair_image, self.crosshair_rect)
