# src/game/player.py
import json
import math

import pygame
from pygame import Vector2

from ..config.constants import (MAP_W, MAP_H, PLAYER_SIZE, PLAYER_COLOR, PLAYER_SPEED, PLAYER_PROJECTILE_RELOAD,
                                PLAYER_PROJECTILE_SPEED, PLAYER_MAX_HP, PLAYER_MAX_STAMINA, PLAYER_PROJECTILE_DAMAGE,
                                PLAYER_BODY_DAMAGE)
from ..game.entity import TangibleEntity
from ..game.projectile import Projectile


class Turret:
    def __init__(self, player, width, height, projectile_speed, projectile_reload, tangent_offset=0, distance=0,
                 angle_offset=0):
        self.player = player

        self.launch_pos = self.player.pos
        self.last_shot_time = 0

        self.projectile_speed = projectile_speed
        self.projectile_reload = projectile_reload

        self.width = width
        self.height = height

        self.offset_x = tangent_offset
        self.offset_y = distance

        self.angle_offset = math.radians(int(angle_offset))
        self.projectile_size = height

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
            (self.width / 2 + self.offset_y, self.height / 2 + self.offset_x),
            (self.width / 2 + self.offset_y, - self.height / 2 + self.offset_x),
            (- self.width / 2 + self.offset_y, - self.height / 2 + self.offset_x),
            (- self.width / 2 + self.offset_y, self.height / 2 + self.offset_x)
        ]:
            rotated_x = math.cos(turret_angle + self.angle_offset) * point[0] - math.sin(
                turret_angle + self.angle_offset) * point[1] + turret_x
            rotated_y = math.sin(turret_angle + self.angle_offset) * point[0] + math.cos(
                turret_angle + self.angle_offset) * point[1] + turret_y
            rotated_points.append((rotated_x, rotated_y))

        center_x = math.cos(turret_angle + self.angle_offset) * (self.offset_y + self.height) - math.sin(
            turret_angle + self.angle_offset) * self.offset_x + turret_x
        center_y = math.sin(turret_angle + self.angle_offset) * (self.offset_y + self.height) + math.cos(
            turret_angle + self.angle_offset) * self.offset_x + turret_y
        self.launch_pos = Vector2(center_x, center_y)

        return rotated_points

    def fire(self, projectiles):
        if self.player.angle + self.angle_offset is not None and self.player.current_time - self.last_shot_time >= 1000 / (
                self.player.reload * self.projectile_reload):
            projectiles.append(Projectile(self.launch_pos, self.player.angle + self.angle_offset,
                                          self.player.projectile_speed * self.projectile_speed,
                                          size=self.projectile_size))
            self.last_shot_time = self.player.current_time


class Player(TangibleEntity):
    def __init__(self, pos):
        super().__init__(pos, PLAYER_SIZE, "#1925b6", speed=PLAYER_SPEED, inertia=0.94, shape="circle", width=False)

        self.angle = 0
        self.direction = Vector2(0, 0)
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

        with open("src/config/tanks.json", 'r') as json_file:
            turret_sets = json.load(json_file)

        self.turret_sets = {}
        for turret_set in turret_sets['turret_sets']:
            set_name = turret_set['set_name']
            turrets = [Turret(self, **params) for params in turret_set['turrets'].values()]
            self.turret_sets[set_name] = turrets

        self.turrets = self.turret_sets.get('double')

    def clamp_position(self):
        self.pos.x = max(self.size / 2, min(self.pos.x, MAP_W - self.size / 2))
        self.pos.y = max(self.size / 2, min(self.pos.y, MAP_H - self.size / 2))

    def fire(self, projectiles):
        for turret in self.turrets:
            turret.fire(projectiles)

    def update(self, mouse_pos):
        super().update()

        self.direction = self.get_target_direction(mouse_pos)
        dx, dy = self.direction
        self.angle = math.atan2(dy, dx)

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
            self.stamina += 0.01 * self.max_stamina / PLAYER_MAX_STAMINA

        self.move(dx, dy)
        self.clamp_position()

    def draw(self, screen):
        for turret in self.turrets:
            turret.draw(screen, self.pos, self.direction)
        super().draw(screen)
        pygame.draw.circle(screen, self.border_color, (self.pos.x, self.pos.y), self.size / 2, width=3)
