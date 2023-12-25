import pygame


class Counter:
    def __init__(self, game, pos, size, border_color=(255, 255, 255), gauge_color=(127, 127, 127),
                 background_color=(40, 40, 40),
                 max_value=1, min_value=0, border=0, width=0, value=None, text_size=16, command=None, text=""):
        self.game = game
        self.pos = (pos[0] - size[0] / 2, pos[1] - size[1] / 2)
        self.size = size
        self.border = border
        self.width = width
        self.border_color = border_color
        self.gauge_color = gauge_color
        self.background_color = background_color
        self.text_size = text_size
        self.text = text

        self.button_rect = pygame.Rect(self.pos[0] + 2 + self.size[0], self.pos[1], self.size[1], self.size[1])
        self.button = pygame.Rect(self.button_rect)

        self.min_value = min_value
        self.max_value = max_value
        self.value = max_value if value is None else value

        self.clicked = False
        self.command = command

        self.font = pygame.font.Font('src/assets/fonts/Bubble.ttf', text_size)
        self.text_rendered = self.font.render(self.text, True, (255, 255, 255))
        text_width, text_height = self.font.size(self.text)
        self.text_pos = (
        (self.pos[0] + self.size[0] / 2 - text_width / 2), (self.pos[1] + self.size[1] / 2 - text_height / 2))

        self.target_text = self.font.render("+", True, (240, 240, 240))
        self.target_text_rect = self.target_text.get_rect(
            center=(self.button.x + self.button.width / 2, self.button.y + self.button.height / 2 - 2))

    def draw(self, screen):
        rect_params = (self.pos[0] + self.width, self.pos[1] + self.width, self.size[0] - self.width * 2,
                       self.size[1] - self.width * 2)

        pygame.draw.rect(screen, self.background_color, rect_params, border_radius=round(self.border / 2))
        pygame.draw.rect(screen, self.gauge_color, (
        rect_params[0], rect_params[1], rect_params[2] * (max(0, min(self.value, self.max_value)) / self.max_value),
        rect_params[3]), border_radius=round(self.border / 2))
        pygame.draw.rect(screen, self.border_color, (self.pos[0], self.pos[1], self.size[0], self.size[1]),
                         border_radius=self.border, width=self.width)

        button_color = self.gauge_color if self.value < self.max_value else self.background_color
        pygame.draw.rect(screen, button_color, self.button_rect, border_radius=self.border)
        pygame.draw.rect(screen, self.border_color, self.button_rect, border_radius=self.border, width=self.width)
        self.is_clicked()

        screen.blit(self.text_rendered, self.text_pos)
        screen.blit(self.target_text, self.target_text_rect)

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.button.collidepoint(mouse_pos)

    def is_clicked(self):
        if self.is_hovered():
            mouse_button = pygame.mouse.get_pressed()[0]
            if mouse_button and not self.clicked:
                self.clicked = True
            elif not mouse_button and self.clicked:
                self.clicked = False
                if self.command and self.value < self.max_value and self.game.settings.skill_points > 0:
                    self.value += 1
                    self.game.settings.skill_points -= 1
                    self.command()
        else:
            self.clicked = False
