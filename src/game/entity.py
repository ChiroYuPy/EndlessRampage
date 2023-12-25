# src/game/entity.py
import math

import pygame
from pygame.math import Vector2
from ..game.ProgressBar import ProgressBar


class Entity:
    def __init__(self, pos, size, color, shape="rectangle", edges=3, width=4, border=8, max_hp=1):
        self.shape = shape
        self.width = width
        self.border = border
        self.pos = Vector2(pos.x, pos.y)
        self.edges = edges
        self.rotation = math.degrees(0)
        self.size = size
        self.color = color

        self.hp_bar = ProgressBar(self)
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.hp_bar_shown = False
        self.alive = True

    def draw(self, screen):
        if self.shape == "circle":
            pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), radius=int(self.size // 2),
                               width=int(self.width))

        elif self.shape == "rectangle":
            rect = pygame.Rect(0, 0, self.size, self.size)
            rect.center = (int(self.pos.x), int(self.pos.y))
            pygame.draw.rect(screen, self.color, rect, width=int(self.width), border_radius=int(self.border))

        elif self.shape == "polygon":
            angle = 360 / self.edges
            points = []
            for i in range(self.edges):
                x = (self.size - self.size/self.edges) * math.cos(math.radians(angle * i))
                y = (self.size - self.size/self.edges) * math.sin(math.radians(angle * i))
                points.append((x, y))

            rotated_points = [(int(x * math.cos(math.radians(self.rotation)) - y * math.sin(
                math.radians(self.rotation))) + self.pos.x,
                               int(x * math.sin(math.radians(self.rotation)) + y * math.cos(
                                   math.radians(self.rotation))) + self.pos.y)
                              for x, y in points]

            pygame.draw.polygon(screen, self.color, rotated_points, self.width)

        if self.hp_bar_shown:
            self.hp_bar.draw(screen, self.pos)

    def update(self):
        pass

    def get_target_direction(self, target):
        if target is None:
            return None
        else:
            offset = target - self.pos
            return offset.normalize() if offset != Vector2(0, 0) else None


class TangibleEntity(Entity):
    def __init__(self, pos, size, color, shape="rectangle", width=4, border=8, speed=0, inertia=0, speed_boost=1):
        super().__init__(pos, size, color, shape, width=width, border=border)
        self.speed_boost = speed_boost
        self.speed = speed
        self.velocity = Vector2(0, 0)
        self.inertia = inertia

        self.is_already_collide = False

    def move(self, dx, dy):
        self.velocity *= self.inertia
        movement = Vector2(dx, dy)
        if movement.length() != 0:
            self.velocity += movement.normalize() * self.speed

        self.pos += self.velocity * self.speed_boost
