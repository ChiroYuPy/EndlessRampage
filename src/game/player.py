# src/game/player.py
import math

import pygame
from pygame import Vector2

from ..config.constants import (MAP_W, MAP_H, PLAYER_SIZE, PLAYER_COLOR, PLAYER_SPEED, PLAYER_PROJECTILE_RELOAD,
                                PLAYER_PROJECTILE_SPEED, PLAYER_MAX_HP, PLAYER_MAX_STAMINA, PLAYER_PROJECTILE_DAMAGE,
                                PLAYER_BODY_DAMAGE)
from ..game.entity import TangibleEntity
from ..game.projectile import Projectile


class Turret:
    def __init__(self, player, width, height, offset_x=0, offset_y=0):
        self.launch_pos = 0
        self.last_shot_time = 0

        self.player = player
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.angle = 0

    def draw(self, screen, pos, direction):
        if direction:
            x, y = pos
            turret_points = self.calculate_turret_points(x, y, direction)
            pygame.draw.polygon(screen, (71, 71, 71), turret_points)
            pygame.draw.polygon(screen, (57, 57, 57), turret_points, width=3)

    def calculate_turret_points(self, x, y, direction):
        turret_x, turret_y = x, y

        turret_angle = math.atan2(direction[1], direction[0])
        rotated_points = []

        for point in [
            (self.width/2 + self.offset_y, self.height / 2 + self.offset_x),
            (self.width/2 + self.offset_y, - self.height / 2 + self.offset_x),
            (- self.width/2 + self.offset_y, - self.height / 2 + self.offset_x),
            (- self.width/2 + self.offset_y, self.height / 2 + self.offset_x)
        ]:
            rotated_x = math.cos(turret_angle) * point[0] - math.sin(turret_angle) * point[1] + turret_x
            rotated_y = math.sin(turret_angle) * point[0] + math.cos(turret_angle) * point[1] + turret_y
            rotated_points.append((rotated_x, rotated_y))


        center_x = math.cos(turret_angle) * (self.offset_y + self.height/2) - math.sin(turret_angle) * self.offset_x + turret_x
        center_y = math.sin(turret_angle) * (self.offset_y + self.height/2) + math.cos(turret_angle) * self.offset_x + turret_y
        self.launch_pos = Vector2(center_x, center_y)

        return rotated_points

    def update_rotation(self, pos):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_x, player_y = pos

        turret_x, turret_y = player_x + self.offset_x, player_y + self.offset_y
        self.angle = math.atan2(mouse_x - turret_y, mouse_x - turret_x)

    def fire(self, projectiles):
        if self.player.direction is not None and self.player.current_time - self.last_shot_time >= 1000 / self.player.reload:
            projectiles.append(Projectile(self.launch_pos, self.player.direction, self.player.projectile_speed))

            step_back = -self.player.direction
            self.player.move(*step_back)

            self.last_shot_time = self.player.current_time


class Player(TangibleEntity):
    def __init__(self, pos):
        super().__init__(pos, PLAYER_SIZE, "#1925b6", speed=PLAYER_SPEED, inertia=0.94, shape="circle", width=False)

        self.direction = None
        self.current_time = 0
        self.last_stamina_regen = 0
        self.last_shot_time = 0
        self.last_speed_boost_time = 0
        self.speed_boost = False

        self.border_color = "#141fab"

        self.player_stamina_regen = 1000
        self.speed_boost_delay = 2000

        self.reload = PLAYER_PROJECTILE_RELOAD
        self.projectile_speed = PLAYER_PROJECTILE_SPEED
        self.body_damage = PLAYER_BODY_DAMAGE
        self.projectile_damage = PLAYER_PROJECTILE_DAMAGE
        self.speed = PLAYER_SPEED
        self.max_hp = PLAYER_MAX_HP
        self.max_stamina = PLAYER_MAX_STAMINA

        self.hp = self.max_hp
        self.stamina = self.max_stamina

        self.turret1 = Turret(self, 48, 22, offset_x=13, offset_y=24)
        self.turret2 = Turret(self, 48, 22, offset_x=-13, offset_y=24)

    def clamp_position(self):
        self.pos.x = max(self.size / 2, min(self.pos.x, MAP_W - self.size / 2))
        self.pos.y = max(self.size / 2, min(self.pos.y, MAP_H - self.size / 2))

    def fire(self, projectiles):
        self.turret1.fire(projectiles)
        self.turret2.fire(projectiles)

    def update(self, mouse_pos):
        super().update()
        self.direction = self.get_target_direction(mouse_pos)

        self.current_time = pygame.time.get_ticks()

        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_d] - keys[pygame.K_q]
        dy = keys[pygame.K_s] - keys[pygame.K_z]

        if self.speed_boost and self.stamina > 0:
            self.speed_boost = 2
            self.stamina -= math.sqrt(self.velocity.x ** 2 + self.velocity.y ** 2) / 50
            self.last_speed_boost_time = self.current_time
        else:
            self.speed_boost = 1

        if (self.current_time - self.last_speed_boost_time >= self.speed_boost_delay
                and self.stamina < self.max_stamina):
            self.stamina += 0.01

        self.move(dx, dy)
        self.turret1.update_rotation(self.pos)
        self.turret2.update_rotation(self.pos)
        self.clamp_position()

    def draw(self, screen):
        self.turret1.draw(screen, self.pos, self.direction)
        self.turret2.draw(screen, self.pos, self.direction)
        super().draw(screen)
        pygame.draw.circle(screen, self.border_color, (self.pos.x, self.pos.y), self.size/2, width=3)
