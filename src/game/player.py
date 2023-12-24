# src/game/player.py
import math

import pygame
from ..config.constants import (MAP_W, MAP_H, PLAYER_SIZE, PLAYER_COLOR, PLAYER_SPEED, PLAYER_PROJECTILE_RELOAD,
                                PLAYER_PROJECTILE_SPEED, PLAYER_MAX_HP, PLAYER_MAX_STAMINA, PLAYER_PROJECTILE_DAMAGE)
from ..game.entity import TangibleEntity
from ..game.projectile import Projectile


class Player(TangibleEntity):
    def __init__(self, pos):
        super().__init__(pos, PLAYER_SIZE, PLAYER_COLOR, speed=PLAYER_SPEED, inertia=0.92)
        self.last_stamina_regen = 0
        self.player_stamina_regen = 1000
        self.current_time = 0
        self.player_speed_boost_delay = 2000
        self.player_reload = PLAYER_PROJECTILE_RELOAD
        self.projectile_speed = PLAYER_PROJECTILE_SPEED
        self.last_shot_time = 0
        self.last_speed_boost_time = 0
        self.projectile_damage = PLAYER_PROJECTILE_DAMAGE
        self.speed = PLAYER_SPEED
        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp
        self.max_stamina = PLAYER_MAX_STAMINA
        self.stamina = self.max_stamina
        self.speed_boost = False

    def clamp_position(self):
        self.pos.x = max(self.size / 2, min(self.pos.x, MAP_W - self.size / 2))
        self.pos.y = max(self.size / 2, min(self.pos.y, MAP_H - self.size / 2))

    def fire(self, projectiles, mouse_pos):
        direction = self.get_target_direction(mouse_pos)
        if direction is not None and self.current_time - self.last_shot_time >= 1000 / self.player_reload:
            projectiles.append(Projectile(self.pos, direction, self.projectile_speed))
            self.last_shot_time = self.current_time

    def update(self):
        self.current_time = pygame.time.get_ticks()

        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_d] - keys[pygame.K_q]
        dy = keys[pygame.K_s] - keys[pygame.K_z]

        if self.speed_boost and self.stamina > 0:
            self.speed_boost = 2
            self.stamina -= math.sqrt(self.velocity.x**2+self.velocity.y**2)/50
            self.last_speed_boost_time = self.current_time
        else:
            self.speed_boost = 1

        if (self.current_time - self.last_speed_boost_time >= self.player_speed_boost_delay
                and self.stamina < self.max_stamina):
            self.stamina += 0.01

        self.move(dx, dy)
        self.clamp_position()

    def draw(self, screen):
        super().draw(screen)
