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
from ..ui.gauge import Gauge
from ..ui.counter import Counter
from ..game.CollisionHandler import Collision


class Game:
    def __init__(self):
        self.delta_time = 0.0

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

        self.player_xp_bar = Gauge((self.window_width / 2, self.window_height - 20), (360, 30),
                                   max_value=self.settings.max_xp,
                                   border_color=(50, 50, 50),
                                   gauge_color="#15cac5",
                                   back_gauge_color="#7accc9",
                                   border=8,
                                   width=4,
                                   text=True,
                                   text_color="#aee1df",
                                   adapt_value_speed=0.5,
                                   default_value=0)
        self.game_uis.append(self.player_xp_bar)

        self.core_hp_bar = Gauge((self.window_width - 110, self.window_height / 2 + 46), (216, 30),
                                 max_value=self.core.max_hp,
                                 border_color=(50, 50, 50),
                                 gauge_color="#d6702e",
                                 back_gauge_color="#d29e7c",
                                 border=8,
                                 width=4,
                                 text=True,
                                 text_color="#eabfa2",
                                 adapt_value_speed=0.3,
                                 default_value=self.core.max_hp)
        self.game_uis.append(self.core_hp_bar)

        self.player_hp_bar = Gauge((self.window_width - 110, self.window_height / 2 + 83), (216, 30),
                                   max_value=self.player.max_hp,
                                   border_color=(50, 50, 50),
                                   gauge_color="#9d1717",
                                   back_gauge_color="#ca6868",
                                   border=8,
                                   width=4,
                                   text=True,
                                   text_color="#ea9696",
                                   adapt_value_speed=0.3,
                                   default_value=self.player.max_hp)
        self.game_uis.append(self.player_hp_bar)

        self.player_stamina_bar = Gauge((self.window_width - 110, self.window_height / 2 + 120), (216, 30),
                                        max_value=self.player.max_stamina,
                                        border_color=(50, 50, 50),
                                        gauge_color=(88, 23, 246),
                                        back_gauge_color="#7d70ca",
                                        border=8,
                                        width=4,
                                        text=True,
                                        text_color="#a498e8",
                                        adapt_value_speed=0.3,
                                        default_value=self.player.max_stamina)
        self.game_uis.append(self.player_stamina_bar)

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
            "player_body_damage_level": {
                "name": "Player body damage",
                "level": 0,
                "color": "#6cf0ec"
            },
            "player_projectile_speed_level": {
                "name": "Player projectile speed",
                "level": 0,
                "color": "#f0d96c"
            },
            "player_reload_level": {
                "name": "Player reload",
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

        self.pause_menu_uis.append(Button((self.window_width * 0.1, self.window_height / 2 - 300, 200, 60),
                                          hover_color=(115, 115, 115),
                                          text="Simple Tank",
                                          font_size=24,
                                          border=16,
                                          command=lambda: self.player.change_tank("simple")))
        self.pause_menu_uis.append(Button((self.window_width * 0.1, self.window_height / 2 - 220, 200, 60),
                                          hover_color=(115, 115, 115),
                                          text="Double Tank",
                                          font_size=24,
                                          border=16,
                                          command=lambda: self.player.change_tank("double")))
        self.pause_menu_uis.append(Button((self.window_width * 0.1, self.window_height / 2 - 140, 200, 60),
                                          hover_color=(115, 115, 115),
                                          text="Triplet Tank",
                                          font_size=24,
                                          border=16,
                                          command=lambda: self.player.change_tank("triplet")))
        self.pause_menu_uis.append(Button((self.window_width * 0.1, self.window_height / 2 - 60, 200, 60),
                                          hover_color=(115, 115, 115),
                                          text="Octo Tank",
                                          font_size=24,
                                          border=16,
                                          command=lambda: self.player.change_tank("octo")))
        self.pause_menu_uis.append(Button((self.window_width * 0.1, self.window_height / 2 + 20, 200, 60),
                                          hover_color=(115, 115, 115),
                                          text="Spread Shot Tank",
                                          font_size=24,
                                          border=16,
                                          command=lambda: self.player.change_tank("spread shot")))

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
            self.player.fire(self.projectiles)
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
        current_tick = pygame.time.get_ticks()
        self.delta_time = (current_tick - self.tick) / 1000
        self.tick = current_tick

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
        self.player_xp_bar.value = self.settings.xp

        self.player.update(self.get_pos_on_map(pygame.mouse.get_pos()))
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