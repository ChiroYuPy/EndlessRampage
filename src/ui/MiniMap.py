import pygame
from ..config.constants import MAP_W, MAP_H, PLAYER_COLOR, CORE_COLOR, ENEMIES_COLOR, ENEMIES_SPAWN_DISTANCE


class MiniMap:
    def __init__(self, pos, size, game):
        self.game = game
        self.pos = pos
        self.size = size

    def draw(self, screen):
        map_x, map_y = self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2
        pygame.draw.rect(screen,
                         (51, 51, 51),
                         (map_x - 8, map_y - 8, self.size[1] + 16, self.size[0] + 16),
                         border_radius=8,
                         width=4)

        pygame.draw.circle(screen, (50, 50, 50), self.pos, radius=ENEMIES_SPAWN_DISTANCE/MAP_W*self.size[0], width=2)

        mini_map_player_x = self.game.player.pos.x / MAP_W * self.size[1] + map_x
        mini_map_player_y = self.game.player.pos.y / MAP_H * self.size[0] + map_y
        pygame.draw.circle(screen, PLAYER_COLOR, (mini_map_player_x, mini_map_player_y), 2)

        mini_map_core_x = self.game.core.pos.x / MAP_W * self.size[1] + map_x
        mini_map_core_y = self.game.core.pos.y / MAP_H * self.size[0] + map_y
        pygame.draw.circle(screen, CORE_COLOR, (mini_map_core_x, mini_map_core_y), 3)

        for enemy in self.game.enemies:
            mini_map_enemy_x = enemy.pos.x / MAP_W * self.size[1] + map_x
            mini_map_enemy_y = enemy.pos.y / MAP_H * self.size[0] + map_y
            pygame.draw.circle(screen, ENEMIES_COLOR, (mini_map_enemy_x, mini_map_enemy_y), 1)