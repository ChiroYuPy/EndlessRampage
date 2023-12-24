# src/game/core.py
from ..game.entity import Entity
from ..config.constants import CORE_SIZE, CORE_COLOR, CORE_MAX_HP


class Core(Entity):
    def __init__(self, pos):
        super().__init__(pos=pos,
                         size=CORE_SIZE,
                         color=CORE_COLOR,
                         max_hp=CORE_MAX_HP)