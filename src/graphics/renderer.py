# src/graphics/renderer.py
import ctypes
import sys

import pygame
from pygame import Vector2
from ..ui.cursor import Cursor
from ..config.constants import CAPTION, BACKGROUND_COLOR, MAP_COLOR, MAP_W, MAP_H, ENEMIES_SPAWN_DISTANCE, FPS, \
    GAME_VERSION


class Renderer:
    def __init__(self, game):
        self.game = game

        self.screen_width = game.window_width
        self.screen_height = game.window_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.NOFRAME, pygame.SRCALPHA)
        pygame.display.set_caption(CAPTION)
        pygame.mouse.set_visible(False)
        self.font12 = pygame.font.Font("src/assets/fonts/Bubble.ttf", 12)
        self.font24 = pygame.font.Font("src/assets/fonts/Bubble.ttf", 24)

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
                         (*self.get_map_pos(Vector2(-self.screen_width / 2 - 1, -self.screen_height / 2 - 1)),
                          self.screen_width + 1, self.screen_height + 1))
        pygame.draw.circle(self.map, (50, 50, 50), (MAP_W / 2, MAP_H / 2), radius=ENEMIES_SPAWN_DISTANCE, width=5)

        self.total_entities_drawn = 0

        for enemy in self.game.enemies:
            enemy.draw(self.map)
            self.total_entities_drawn += 1

            if self.game.debug_mode:
                enemy_rect = pygame.Rect(enemy.pos.x - enemy.size / 2, enemy.pos.y - enemy.size / 2, enemy.size,
                                         enemy.size)
                pygame.draw.rect(self.map, (255, 255, 255), enemy_rect, 1)

        for xp_object in self.game.xp_objects:
            xp_object.draw(self.map)
            self.total_entities_drawn += 1

            if self.game.debug_mode:
                xp_object_rect = pygame.Rect(xp_object.pos.x - xp_object.size / 2, xp_object.pos.y - xp_object.size / 2,
                                             xp_object.size, xp_object.size)
                pygame.draw.rect(self.map, (255, 255, 255), xp_object_rect, 1)

        self.total_entities_drawn += 2

        self.game.core.draw(self.map)

        for projectile in self.game.projectiles:
            projectile.draw(self.map)
            self.total_entities_drawn += 1

            if self.game.debug_mode:
                projectile_rect = pygame.Rect(projectile.pos.x - projectile.size / 2,
                                              projectile.pos.y - projectile.size / 2, projectile.size, projectile.size)
                pygame.draw.rect(self.map, (255, 255, 255), projectile_rect, 1)

        if not self.game.pause_menu_active:
            self.game.player.draw(self.map)

        if self.game.debug_mode:
            player_rect = pygame.Rect(self.game.player.pos.x - self.game.player.size / 2,
                                      self.game.player.pos.y - self.game.player.size / 2,
                                      self.game.player.size, self.game.player.size)
            core_rect = pygame.Rect(self.game.core.pos.x - self.game.core.size / 2,
                                    self.game.core.pos.y - self.game.core.size / 2,
                                    self.game.core.size, self.game.core.size)
            pygame.draw.rect(self.map, (255, 255, 255), player_rect, 1)
            pygame.draw.rect(self.map, (255, 255, 255), core_rect, 1)

        self.screen.blit(self.map, (
        -self.game.player.pos.x + self.screen_width / 2, -self.game.player.pos.y + self.screen_height / 2))

    def render_uis(self):

        for obj in self.game.game_uis:
            obj.draw(self.screen)

        text1 = self.font24.render('Lvl.', True, '#9ee523')
        text2 = self.font24.render(str(self.game.settings.level), True, '#4dc514')

        center_x = self.screen_width / 2 - text1.get_width() + text2.get_width() - 4

        text1_pos = (center_x, self.screen_height - 64)
        text2_pos = (center_x + text1.get_width(), self.screen_height - 64)

        self.screen.blit(text1, text1_pos)
        self.screen.blit(text2, text2_pos)

        if self.game.settings.skill_points != 0:
            text = self.font24.render(f"x{self.game.settings.skill_points}", True, (255, 255, 255))
            rotated_text = pygame.transform.rotate(text, 20)
            self.screen.blit(rotated_text, (self.screen_width * 0.205, self.screen_height * 0.605))

        if self.game.debug_mode:
            for i, stat_text in enumerate(self.update_stats()):
                stat_display = self.font12.render(stat_text, True, (199, 199, 199))
                self.screen.blit(stat_display, (4, 1 + i * 12))

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
            f'----------[ Info ]------------',
            f'{GAME_VERSION} | {int(self.game.clock.get_fps())}/{FPS} | {int(pygame.time.get_ticks() / 1000)}s | {int(pygame.time.get_ticks() / 1000 * FPS)} img',
            f'MWPos: {pygame.mouse.get_pos()}',
            f'MMPos: {self.get_map_pos(Vector2(*pygame.mouse.get_pos()))}',
            f'PPos: {(int(self.game.player.pos.x), int(self.game.player.pos.y))}',
            f'PVel: {round(self.game.player.velocity) * self.game.player.speed_boost}',
            f'Enemies: {len(self.game.enemies)}',
            f'Projectiles: {len(self.game.projectiles)}',
            f'XpObjects: {len(self.game.xp_objects)}',
            f'Objects: {self.total_entities_drawn}',
            f'Uis: {len(self.game.game_uis)}',
            f'',
            f'----------[ Game ]-----------',
            f'player Projectile Damage {self.game.player.projectile_damage}',
            f'player Projectile Reload {self.game.player.reload}',
            f'player Projectile Speed {self.game.player.projectile_speed}',
            f'player Body Damage {self.game.player.body_damage}',
            f'Core Max HP {self.game.core.max_hp}',
            f'player Max HP {self.game.player.max_hp}',
            f'player Max Stamina {self.game.player.max_stamina}',
            f'player Max Speed {self.game.player.speed}',
        ]
