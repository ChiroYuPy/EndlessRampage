# src/game/projectile.py
import pygame
import math

from ..game.entity import TangibleEntity
from ..config.constants import PROJECTILE_SIZE, PROJECTILE_COLOR


class Projectile(TangibleEntity):
    def __init__(self, pos, angle, speed, size=PROJECTILE_SIZE):
        super().__init__(pos=pos,
                         size=size,
                         color=PROJECTILE_COLOR,
                         shape="circle",
                         width=False)
        self.border_color = "#7e0f3c"
        self.angle = angle
        self.speed = speed
        self.spawn_time = pygame.time.get_ticks()
        self.direction = None

    def update(self):
        if self.angle is not None:
            self.direction = pygame.Vector2(math.cos(self.angle), math.sin(self.angle))
            self.velocity = self.direction * self.speed
        self.move(self.velocity.x, self.velocity.y)
        if self.spawn_time + 20000 * 1 / self.speed < pygame.time.get_ticks():
            self.alive = False

    def draw(self, screen):
        super().draw(screen)
        pygame.draw.circle(screen, self.border_color, (self.pos.x, self.pos.y), self.size / 2, width=3)
