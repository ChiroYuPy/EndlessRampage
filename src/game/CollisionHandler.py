import pygame
from pygame import Vector2


class Collision:
    def __init__(self, game):
        self.game = game

    def handler(self):
        for enemy in self.game.enemies:
            for projectile in self.game.projectiles:
                if self.check_collision(projectile, enemy):
                    enemy.hp -= self.game.player.projectile_damage
                    if enemy.hp <= 0:
                        self.game.xp_bar.update_xp(enemy.xp_value)
                        enemy.alive = False
                    projectile.alive = False

            if self.check_collision(self.game.core, enemy):
                self.game.core.hp -= enemy.hp
                enemy.alive = False
            if self.check_collision(self.game.player, enemy):
                self.game.player.hp -= enemy.hp
                enemy.alive = False

        for xp_object in self.game.xp_objects:
            if self.check_collision(self.game.player, xp_object):
                xp_object.move(self.game.player.velocity.x, self.game.player.velocity.y)
                self.game.player.velocity += Vector2(-self.game.player.velocity.x * 2, -self.game.player.velocity.y * 2)
                xp_object.hp -= 1
                self.game.player.hp -= 1
                if xp_object.hp <= 0:
                    self.game.xp_bar.update_xp(xp_object.xp_value)
                    xp_object.alive = False

            for projectile in self.game.projectiles:
                if self.check_collision(projectile, xp_object):
                    xp_object.move(xp_object.velocity.x, xp_object.velocity.y)
                    projectile_velocity = projectile.direction * projectile.speed
                    xp_object.velocity = Vector2(projectile_velocity.x, projectile_velocity.y)
                    xp_object.hp -= 1
                    projectile.alive = False
                    if xp_object.hp <= 0:
                        self.game.xp_bar.update_xp(xp_object.xp_value)
                        xp_object.alive = False

    def check_collision(self, entity1, entity2):
        rect1 = pygame.Rect(entity1.pos.x - entity1.size / 2, entity1.pos.y - entity1.size / 2, entity1.size,
                            entity1.size)
        rect2 = pygame.Rect(entity2.pos.x - entity2.size / 2, entity2.pos.y - entity2.size / 2, entity2.size,
                            entity2.size)
        return rect1.colliderect(rect2)
