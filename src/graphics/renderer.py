# src/graphics/renderer.py
import ctypes
import sys

import pygame
from pygame import Vector2
from ..ui.cursor import Cursor
from ..config.constants import CAPTION, BACKGROUND_COLOR, MAP_COLOR, MAP_W, MAP_H, ENEMIES_SPAWN_DISTANCE, FPS, GAME_VERSION


class Renderer:
    def __init__(self, game):
        self.game = game

        self.screen_width = game.window_width
        self.screen_height = game.window_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.NOFRAME, pygame.SRCALPHA)
        pygame.display.set_caption(CAPTION)
        pygame.mouse.set_visible(False)
        self.font = pygame.font.Font("src/assets/fonts/Bubble.ttf", 20)

        self.cursor = Cursor(self)

        self.map = pygame.surface.Surface((MAP_W, MAP_H))
        self.total_entities_drawn = 0

    def window_size(self, width, height):
        self.screen_width = width
        self.screen_height = height
        self.screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
        self.center_window()

    def center_window(self):
        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h

        x = (screen_width - self.screen_width) // 2
        y = (screen_height - self.screen_height) // 2

        if sys.platform.startswith('win'):
            ctypes.windll.user32.SetWindowPos(pygame.display.get_wm_info()['window'], -1, x, y, 0, 0, 0x0001)

    def get_map_pos(self, vector, decimals=None):
        x = round(vector.x + self.game.player.pos.x, decimals) if decimals is not None else round(
            vector.x + self.game.player.pos.x)
        y = round(vector.y + self.game.player.pos.y, decimals) if decimals is not None else round(
            vector.y + self.game.player.pos.y)
        return x, y

    def render(self):
        self.render_objects()
        self.render_uis()

        pygame.display.flip()

    def render_objects(self):

        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.map, MAP_COLOR,
                         (*self.get_map_pos(Vector2(-self.screen_width / 2 - 1, -self.screen_height / 2 - 1)), self.screen_width + 1, self.screen_height + 1))
        pygame.draw.circle(self.map, (50, 50, 50), (MAP_W / 2, MAP_H / 2), radius=ENEMIES_SPAWN_DISTANCE, width=5)

        self.total_entities_drawn = 0

        for enemy in self.game.enemies:
            enemy.draw(self.map)
            self.total_entities_drawn += 1

        for projectile in self.game.projectiles:
            projectile.draw(self.map)
            self.total_entities_drawn += 1

        for xp_object in self.game.xp_objects:
            xp_object.draw(self.map)
            self.total_entities_drawn += 1

        self.total_entities_drawn += 2

        self.game.core.draw(self.map)
        self.game.player.draw(self.map)

        self.screen.blit(self.map, (-self.game.player.pos.x + self.screen_width / 2, -self.game.player.pos.y + self.screen_height / 2))

    def render_uis(self):

        for obj in self.game.game_uis:
            obj.draw(self.screen)

        if self.game.xp_bar.skill_points != 0:
            text = self.font.render(f"x{self.game.xp_bar.skill_points}", True, (255, 255, 255))
            rotated_text = pygame.transform.rotate(text, 20)
            self.screen.blit(rotated_text, (self.screen_width*0.205, self.screen_height*0.65))

        if self.game.debug_mode:
            for i, stat_text in enumerate(self.update_stats()):
                stat_display = self.font.render(stat_text, True, (199, 199, 199))
                self.screen.blit(stat_display, (5, 5 + i * 20))

        if not self.game.debug_mode and not self.game.pause_menu_active and pygame.mouse.get_focused():
            self.cursor.draw(self.screen)

        if self.game.pause_menu_active:
            self.draw_pause_menu()

    def draw_pause_menu(self):
        filter = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        filter.fill((0, 0, 0, 80))
        self.screen.blit(filter, (0, 0))

        for obj in self.game.pause_menu_uis:
            obj.draw(self.screen)

    def update_stats(self):
        return [
            f'Game version: {GAME_VERSION}',
            f'Mouse Window Pos: {pygame.mouse.get_pos()}',
            f'Mouse Map Pos: {self.get_map_pos(Vector2(*pygame.mouse.get_pos()))}',
            f'Player Pos: {(int(self.game.player.pos.x), int(self.game.player.pos.y))}',
            f'Player HP: {self.game.player.hp}',
            f'Player Velocity: {round(self.game.player.velocity)*self.game.player.speed_boost}',
            f'FPS: {int(self.game.clock.get_fps())}/{FPS}',
            f'Game Enemies: {len(self.game.enemies)}',
            f'Game Projectiles: {len(self.game.projectiles)}',
            f'Game XpObjects: {len(self.game.xp_objects)}',
            f'Game Objects: {self.total_entities_drawn}',
            f'Game Uis: {len(self.game.game_uis)}',
            f'Game UpTime: {int(pygame.time.get_ticks() / 1000)}s',
            f'Images Draws: {int(pygame.time.get_ticks() / 1000 * FPS)}',
        ]
