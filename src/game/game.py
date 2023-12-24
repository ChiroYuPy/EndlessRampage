# src/game/game.py
import pygame
from ..graphics.renderer import Renderer
from ..game.player import Player
from ..game.core import Core
from ..ui.button import Button
from ..ui.MiniMap import MiniMap
from ..config.constants import *
from ..game.spawner import *
from ..config.settings import Settings
from ..game.XpBar import XpBar
from ..ui.gauge import Gauge
from ..ui.counter import Counter
from ..game.CollisionHandler import Collision


class Game:
    def __init__(self):
        self.fullscreen = False
        self.is_running = True
        self.tick = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()
        self.window_width = WINDOW_SIZE[0]
        self.window_height = WINDOW_SIZE[1]
        self.renderer = Renderer(self)
        self.collision = Collision(self)

        self.debug_mode = False
        self.pause_menu_active = False

        self.enemies = []
        self.projectiles = []
        self.xp_objects = []
        self.power_ups = []

        self.game_uis = []
        self.pause_menu_uis = []

        self.player = Player(Vector2(MAP_W // 2, MAP_H // 2))
        self.core = Core(Vector2(MAP_W // 2, MAP_H // 2))
        self.spawner = Spawner()
        self.generator = Generator()

        self.settings = Settings(self)

        self.game_uis.append(Button((self.window_width - 40, 0, 40, 40),
                                    hover_color=(228, 15, 15), text="×",
                                    font_size=40,
                                    offset_y=-3,
                                    command=lambda: self.stop()))
        self.game_uis.append(Button((self.window_width - 80, 0, 40, 40),
                                    hover_color=(115, 115, 115),
                                    text="::",
                                    font_size=36,
                                    offset_y=-2,
                                    command=lambda: self.toggle_fullscreen()))
        self.game_uis.append(Button((self.window_width - 120, 0, 40, 40),
                                    hover_color=(115, 115, 115),
                                    text="-",
                                    font_size=48,
                                    offset_y=-2))

        self.core_hp_bar = Gauge((self.window_width - 110, self.window_height / 2 + 46), (216, 30),
                                 max_value=self.core.max_hp,
                                 border_color=(50, 50, 50),
                                 gauge_color="#d6702e",
                                 border=8,
                                 width=4,
                                 text=True,
                                 text_color="#eabfa2")
        self.game_uis.append(self.core_hp_bar)

        self.player_stamina_bar = Gauge((self.window_width - 110, self.window_height / 2 + 83), (216, 30),
                                        max_value=self.player.max_stamina,
                                        border_color=(50, 50, 50),
                                        gauge_color=(88, 23, 246),
                                        border=8,
                                        width=4,
                                        text=True,
                                        text_color="#a498e8")
        self.game_uis.append(self.player_stamina_bar)

        self.player_hp_bar = Gauge((self.window_width - 110, self.window_height / 2 + 120), (216, 30),
                                   max_value=self.player.max_hp,
                                   border_color=(50, 50, 50),
                                   gauge_color="#9d1717",
                                   border=8,
                                   width=4,
                                   text=True,
                                   text_color="#ea9696")
        self.game_uis.append(self.player_hp_bar)

        y_spacing = 32

        skills = {
            "player_speed_level": {
                "name": "Player max speed",
                "level": 0,
                "color": "#eeb690"
            },
            "player_stamina_level": {
                "name": "Player max stamina",
                "level": 0,
                "color": "#ec6cf0"
            },
            "player_hp_level": {
                "name": "Player max hp",
                "level": 0,
                "color": "#9a6cf0"
            },
            "core_hp_level": {
                "name": "Core max hp",
                "level": 0,
                "color": "#6c96f0"
            },
            "player_projectile_speed_level": {
                "name": "Player projectile speed",
                "level": 0,
                "color": "#f0d96c"
            },
            "player_projectile_reload_level": {
                "name": "Player projectile reload",
                "level": 0,
                "color": "#f06c6c"
            },
            "player_projectile_damage_level": {
                "name": "Player projectile damage",
                "level": 0,
                "color": "#98f06c"
            }
        }

        for skill in skills:
            temp_counter_name = f"counter_of_{skill}"
            counter_y = (117, self.window_height - 20 + list(skills.keys()).index(skill) * (-y_spacing))
            locals()[temp_counter_name] = Counter(self, counter_y,
                                                  (230, 30),
                                                  border_color=(50, 50, 50),
                                                  gauge_color=skills[skill]["color"],
                                                  border=8,
                                                  width=4,
                                                  value=0,
                                                  max_value=10,
                                                  text=skills[skill]["name"],
                                                  command=lambda n=skills[skill]: self.settings.update_skill(n))
            self.game_uis.append(locals()[temp_counter_name])

        self.pause_menu_uis.append(Button((self.window_width * 0.1, self.window_height / 2 - 105, 200, 60),
                                          hover_color=(115, 115, 115),
                                          text="Resume",
                                          font_size=24))
        self.pause_menu_uis.append(Button((self.window_width * 0.1, self.window_height / 2 - 30, 200, 60),
                                          hover_color=(115, 115, 115),
                                          text="Quit",
                                          font_size=24,
                                          command=lambda: self.stop()))
        self.pause_menu_uis.append(Button((self.window_width * 0.1, self.window_height / 2 + 45, 200, 60),
                                          hover_color=(115, 115, 115),
                                          text="Restart",
                                          font_size=24))

        self.xp_bar = XpBar((self.window_width / 2, self.window_height * 0.05))
        self.game_uis.append(self.xp_bar)

        self.mini_map = MiniMap((self.window_width - 110, self.window_height - 110), (200, 200), self)
        self.game_uis.append(self.mini_map)

        self.player_last_regen_time = 0
        self.core_last_regen_time = 0

    def run(self):
        while self.is_running:
            self.handle_events()
            if not self.pause_menu_active:
                self.update()
            self.renderer.render()
            self.clock.tick(FPS)

    def get_pos_on_map(self, target):
        x, y = target
        return Vector2(x, y) + self.player.pos + Vector2(-self.settings.screen_width / 2,
                                                         -self.settings.screen_height / 2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.settings.screen_width, self.settings.screen_height = 1920, 1080
                    self.renderer.window_size(self.settings.screen_width, self.settings.screen_height)
                elif event.key == pygame.K_F10:
                    self.settings.screen_width, self.settings.screen_height = 1280, 720
                    self.renderer.window_size(self.settings.screen_width, self.settings.screen_height)
                elif event.key == pygame.K_F9:
                    self.settings.screen_width, self.settings.screen_height = 640, 360
                    self.renderer.window_size(self.settings.screen_width, self.settings.screen_height)
                elif event.key == pygame.K_F3 and not self.pause_menu_active:
                    self.debug_mode = not self.debug_mode
                    pygame.mouse.set_visible(self.debug_mode)
                elif event.key == pygame.K_ESCAPE:
                    self.pause_menu_active = not self.pause_menu_active
                    if self.pause_menu_active:
                        self.debug_mode = False
                    pygame.mouse.set_visible(self.pause_menu_active)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_e]:
            self.player.fire(self.projectiles, self.get_pos_on_map(pygame.mouse.get_pos()))
        if keys[pygame.K_LSHIFT]:
            self.player.speed_boost = True
        else:
            self.player.speed_boost = False

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.renderer.window_size(self.settings.screen_width, self.settings.screen_height)
            self.fullscreen = False
        else:
            self.renderer.window_size(1920, 1080)
            self.fullscreen = True

    def natural_regeneration(self):
        if self.player.hp < self.player.max_hp and self.tick - self.player_last_regen_time >= PLAYER_REGEN:
            self.player.hp += 1
            self.player_last_regen_time = self.tick
        if self.core.hp < self.core.max_hp and self.tick - self.core_last_regen_time >= CORE_REGEN:
            self.core.hp += 1
            self.core_last_regen_time = self.tick

    def update(self):
        self.tick = pygame.time.get_ticks()
        self.spawner.spawn(self.tick, self.enemies, self.core)
        self.generator.spawn(self.tick, self.xp_objects)

        for enemy in self.enemies:
            enemy.update()

        for projectile in self.projectiles:
            projectile.update()

        for xp_object in self.xp_objects:
            xp_object.update()

        self.natural_regeneration()

        self.player_hp_bar.value = self.player.hp
        self.player_stamina_bar.value = self.player.stamina
        self.core_hp_bar.value = self.core.hp

        self.player.update()
        self.core.update()

        self.collision.handler()
        self.kill_non_alive_entities()

    def kill_non_alive_entities(self):
        for entity in self.enemies:
            if not entity.alive:
                self.enemies.remove(entity)
        for projectile in self.projectiles:
            if not projectile.alive:
                self.projectiles.remove(projectile)
        for xp_object in self.xp_objects:
            if not xp_object.alive:
                self.xp_objects.remove(xp_object)


    def stop(self):
        self.is_running = False
