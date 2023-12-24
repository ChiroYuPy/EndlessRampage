import pygame


class Gauge:
    def __init__(self, pos, size, border_color=(255, 255, 255), gauge_color=(127, 127, 127),
                 background_color=(40, 40, 40),
                 max_value=1, min_value=0, border=0, width=0, text=False, text_color=(255, 255, 255), text_size=16):
        self.pos = (pos[0] - size[0] / 2, pos[1] - size[1] / 2)
        self.size = size
        self.border = border
        self.width = width
        self.border_color = border_color
        self.gauge_color = gauge_color
        self.background_color = background_color

        self.min_value = min_value
        self.max_value = max_value
        self.value = self.max_value

        self.text = text
        self.text_color = text_color
        self.text_font = pygame.font.Font('src/assets/fonts/Bubble.ttf', text_size)
        text_width, text_height = self.text_font.size(f'{round(self.value)}/{self.max_value}')
        self.text_pos = ((self.pos[0] + self.size[0] / 2 - text_width / 2), (self.pos[1] + self.size[1] / 2 - text_height / 2))

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color,
                         (self.pos[0] + self.width, self.pos[1] + self.width, self.size[0] - self.width * 2,
                          self.size[1] - self.width * 2),
                         border_radius=round(self.border / 2))
        pygame.draw.rect(screen, self.gauge_color,
                         (self.pos[0] + self.width, self.pos[1] + self.width,
                          (self.size[0] - self.width * 2) * (max(0, min(self.value, self.max_value)) / self.max_value),
                          self.size[1] - self.width * 2),
                         border_radius=round(self.border / 2))
        pygame.draw.rect(screen, self.border_color,
                         (self.pos[0], self.pos[1], self.size[0], self.size[1]),
                         border_radius=self.border,
                         width=self.width)
        if self.text:
            text_rendered = self.text_font.render(f'{round(self.value)}/{self.max_value}', True, self.text_color)
            screen.blit(text_rendered, self.text_pos)
