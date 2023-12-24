import pygame
from pygame import Surface

pygame.font.init()


class Button:

    def __init__(self, rect, hover_color=(0, 0, 255), default_color=(73, 73, 73), text="", font_size=24, alpha=255,
                 border_radius=0, offset_y=0, command=None):
        self.clicked = False
        self.command = command
        self.rect = pygame.Rect(rect)
        self.hover_color = hover_color
        self.default_color = default_color
        self.text = text
        self.font_size = font_size
        self.alpha = alpha
        self.border_radius = border_radius
        self.offset_y = offset_y

        self.font = pygame.font.SysFont("Sans-serif", self.font_size)
        self.surface = Surface((self.rect.width, self.rect.height))

    def draw(self, screen):
        self.is_clicked()
        if self.is_hovered():
            color = self.hover_color
        else:
            color = self.default_color

        self.surface.fill((0, 0, 0))
        self.surface.set_alpha(self.alpha)
        pygame.draw.rect(self.surface, color, (0, 0, self.rect.width, self.rect.height),
                         border_radius=self.border_radius)
        screen.blit(self.surface, self.rect)

        self.draw_text(screen)

    def draw_text(self, screen):
        target_text = self.font.render(self.text, True, (255, 255, 255))
        target_text_rect = target_text.get_rect(
            center=(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2 + self.offset_y))
        screen.blit(target_text, target_text_rect)

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self):
        if self.is_hovered():
            mouse_button = pygame.mouse.get_pressed()[0]
            if mouse_button and not self.clicked:
                self.clicked = True
            elif not mouse_button and self.clicked:
                self.clicked = False
                if self.command:
                    self.command()
        else:
            self.clicked = False
