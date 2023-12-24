from ..game.entity import TangibleEntity


class XpObject(TangibleEntity):
    def __init__(self, pos, color, size, shape="polygon", edges=3):
        super().__init__(pos=pos, size=size, color=color, shape=shape, width=4, border=8, speed=1, inertia=0.95)
        self.max_hp = 3
        self.hp = self.max_hp

        self.xp_value = 2 ** (edges + 2)
        self.edges = edges
        self.dx = 0
        self.dy = 0

    def move(self, dx, dy):
        self.dx = dx
        self.dy = dy
        super().move(self.dx, self.dy)
        self.dx = 0
        self.dy = 0

    def update(self):
        super().update()
        self.move(self.dx, self.dy)
