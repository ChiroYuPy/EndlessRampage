from ..config.constants import (PLAYER_SPEED, PLAYER_MAX_STAMINA, PLAYER_MAX_HP, CORE_MAX_HP, PLAYER_PROJECTILE_SPEED,
                                PLAYER_PROJECTILE_RELOAD, PLAYER_PROJECTILE_DAMAGE)


class Settings:
    MAX_SKILL_LEVEL = 10

    def __init__(self, game):
        self.game = game

        self.screen_width = 1280
        self.screen_height = 720

        self.game.player.speed = PLAYER_SPEED
        self.game.player.max_stamina = PLAYER_MAX_STAMINA
        self.game.player.max_hp = PLAYER_MAX_HP
        self.game.core.max_hp = CORE_MAX_HP
        self.game.player.projectile_speed = PLAYER_PROJECTILE_SPEED
        self.game.player.projectile_damage = PLAYER_PROJECTILE_DAMAGE
        self.game.player.projectile_reload = PLAYER_PROJECTILE_RELOAD

        self.game.player_speed_level = 0
        self.game.player_stamina_level = 0
        self.game.player_max_hp_level = 0
        self.game.core_max_hp_level = 0
        self.game.player_projectile_speed_level = 0
        self.game.player_projectile_damage_level = 0
        self.game.player_projectile_reload_level = 0

    def round_skill(self, base_value, factor, level):
        return round(base_value * factor ** level, 3)

    def update_skill(self, skill):
        if self.game.xp_bar.skill_points > 0:
            match skill["name"]:
                case "Player max speed":
                    if self.game.player_speed_level < self.MAX_SKILL_LEVEL:
                        self.game.player_speed_level += 1
                    self.game.player.speed = self.round_skill(PLAYER_SPEED, 1.1, self.game.player_speed_level)

                case "Player max stamina":
                    if self.game.player_stamina_level < self.MAX_SKILL_LEVEL:
                        self.game.player_stamina_level += 1
                    self.game.player.max_stamina = self.round_skill(PLAYER_MAX_STAMINA, 1.175, self.game.player_stamina_level)
                    self.game.player_stamina_bar.max_value = self.round_skill(PLAYER_MAX_STAMINA, 1.175, self.game.player_stamina_level)

                case "Player max hp":
                    if self.game.player_max_hp_level < self.MAX_SKILL_LEVEL:
                        self.game.player_max_hp_level += 1
                    self.game.player.max_hp = self.round_skill(PLAYER_MAX_HP, 1.175, self.game.player_max_hp_level)
                    self.game.player_hp_bar.max_value = self.round_skill(PLAYER_MAX_HP, 1.175, self.game.player_max_hp_level)

                case "Core max hp":
                    if self.game.core_max_hp_level < self.MAX_SKILL_LEVEL:
                        self.game.core_max_hp_level += 1
                    self.game.core.max_hp = self.round_skill(CORE_MAX_HP, 1.1, self.game.core_max_hp_level)
                    self.game.core_hp_bar.max_value = self.round_skill(CORE_MAX_HP, 1.175, self.game.core_max_hp_level)

                case "Player projectile speed":
                    if self.game.player_projectile_speed_level < self.MAX_SKILL_LEVEL:
                        self.game.player_projectile_speed_level += 1
                    self.game.player.projectile_speed = self.round_skill(PLAYER_PROJECTILE_SPEED, 1.1, self.game.player_projectile_speed_level)

                case "Player projectile reload":
                    if self.game.player_projectile_reload_level < self.MAX_SKILL_LEVEL:
                        self.game.player_projectile_reload_level += 1
                    self.game.player.projectile_reload = self.round_skill(PLAYER_PROJECTILE_RELOAD, 1.5, self.game.player_projectile_reload_level)

                case "Player projectile damage":
                    if self.game.player_projectile_damage_level < self.MAX_SKILL_LEVEL:
                        self.game.player_projectile_damage_level += 1
                    self.game.player.projectile_damage = self.round_skill(PLAYER_PROJECTILE_DAMAGE, 1.1, self.game.player_projectile_damage_level)
