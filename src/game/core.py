# src/game/core.py
from ..game.entity import Entity
from ..config.constants import CORE_SIZE, CORE_COLOR, CORE_MAX_HP
from ..graphics.ImageLoader import load_image


class Core(Entity):
    def __init__(self, pos):
        super().__init__(pos=pos,
                         size=CORE_SIZE,
                         color=CORE_COLOR,
                         max_hp=CORE_MAX_HP)

        self.image = load_image("core/core-0000.png", scale=8, color_key=(127, 0, 255))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        self.rect.center = (self.pos.x, self.pos.y)
        screen.blit(self.image, self.rect)
