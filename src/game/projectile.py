# src/game/projectile.py
import pygame

from ..game.entity import TangibleEntity
from ..config.constants import PROJECTILE_SIZE, PROJECTILE_COLOR, PROJECTILE_LIFE_TIME


class Projectile(TangibleEntity):
    def __init__(self, pos, direction, speed):
        super().__init__(pos=pos,
                         size=PROJECTILE_SIZE,
                         color=PROJECTILE_COLOR,
                         shape="circle",
                         width=False)
        self.border_color = "#7e0f3c"
        self.direction = direction
        self.speed = speed
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        direction = self.direction
        if direction is not None:
            self.velocity = direction * self.speed
        self.move(self.velocity.x, self.velocity.y)

        if self.spawn_time + PROJECTILE_LIFE_TIME < pygame.time.get_ticks():
            self.alive = False
    
    def draw(self, screen):
        super().draw(screen)
        pygame.draw.circle(screen, self.border_color, (self.pos.x, self.pos.y), self.size / 2, width=3)
        