import pygame

from ..game.entity import TangibleEntity

class Enemy(TangibleEntity):
    def __init__(self, pos, enemy_id):
        enemy_params = get_enemy_params_by_id(enemy_id)
        super().__init__(pos, enemy_params["size"], enemy_params["color"], speed=enemy_params["speed"], inertia=0.92)

        self.type = enemy_params["name"]
        self.max_hp = enemy_params["max_hp"]
        self.xp_value = enemy_params["xp_value"]
        self.hp = self.max_hp
        self.hp_bar_shown = True
        self.target = None

    def update(self):
        direction = self.get_target_direction(self.target.pos)
        if direction is not None:
            self.velocity = direction * self.speed
        self.move(self.velocity.x, self.velocity.y)

    def draw(self, screen):
        super().draw(screen)
        # self.render_name(screen)

    def render_name(self, screen):
        font = pygame.font.Font(None, 12)
        text = font.render(self.type, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.pos.x, self.pos.y-self.size-10))
        screen.blit(text, text_rect)

def get_enemy_params_by_id(enemy_id):
    types = [
        {
            "name": "Basic Enemy",
            "speed": 1,
            "size": 24,
            "color": "#f25820",
            "max_hp": 10,
            "xp_value": 20
        },
        {
            "name": "Fast Enemy",
            "speed": 2,
            "size": 28,
            "color": "#dd1010",
            "max_hp": 5,
            "xp_value": 35
        },
        {
            "name": "Big Enemy",
            "speed": 0.3,
            "size": 40,
            "color": "#8d1212",
            "max_hp": 30,
            "xp_value": 100
        },
        {
            "name": "Armored Enemy",
            "speed": 0.5,
            "size": 32,
            "color": "#969696",
            "max_hp": 20,
            "xp_value": 80
        }
    ]

    if 1 <= enemy_id <= len(types):
        return types[enemy_id - 1]
    else:
        return types[0]
