import pygame


class ProgressBar:
    def __init__(self, entity):
        self.hp = 0
        self.entity = entity
        self.width = entity.size
        self.height = 8
        self.border_color = (255, 0, 0)
        self.fill_color = (0, 255, 0)

    def draw(self, window, pos):
        self.hp = max(0, min(self.entity.hp, self.entity.max_hp))
        pygame.draw.rect(window, self.border_color, (pos.x - self.entity.size/2, pos.y - self.entity.size*0.5 - 16, self.width, self.height), border_radius=8)
        pygame.draw.rect(window, self.fill_color, (pos.x - self.entity.size/2, pos.y - self.entity.size*0.5 - 16, (self.width * self.hp / self.entity.max_hp), self.height), border_radius=8)
