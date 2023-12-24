# src/game/projectile.py
import pygame

from ..game.entity import Entity
from ..config.constants import PROJECTILE_SIZE, PROJECTILE_COLOR, PROJECTILE_LIFE_TIME


class Projectile(Entity):
    def __init__(self, pos, direction, speed):
        super().__init__(pos=pos,
                         size=PROJECTILE_SIZE,
                         color=PROJECTILE_COLOR,
                         shape="circle",
                         width=4)
        self.direction = direction
        self.speed = speed
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.pos += self.direction * self.speed
        if self.spawn_time + PROJECTILE_LIFE_TIME < pygame.time.get_ticks():
            self.alive = False
