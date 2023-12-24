import math
import random

from pygame import Vector2
from ..game.enemy import Enemy
from ..game.XpObject import XpObject
from ..config.constants import ENEMIES_SPAWN_DISTANCE, MAP_W, MAP_H, OBJECT_SPAWN_RATE, ENEMIES_SPAWN_RATE, MAX_OBJECT_ON_MAP

options = [1, 2, 3, 4]
weights = [0.6, 0.25, 0.1, 0.05]


class Spawner:
    def __init__(self):
        self.last_spawn_time = 0

    def spawn(self, tick, data, target=None):
        current_time = tick
        if current_time - self.last_spawn_time >= 1000 / ENEMIES_SPAWN_RATE:
            angle = random.uniform(0, 2 * math.pi)
            vectorial_angle = Vector2(math.cos(angle), math.sin(angle))
            center = target.pos + vectorial_angle * ENEMIES_SPAWN_DISTANCE

            enemy = Enemy(center, random.choices(options, weights)[0])
            enemy.target = target
            data.append(enemy)
            self.last_spawn_time = current_time


class Generator:
    def __init__(self):
        self.edges = None
        self.size = None
        self.color = None
        self.last_spawn_time = 0

    def spawn(self, tick, data):
        if len(data) < MAX_OBJECT_ON_MAP:
            current_time = tick
            if current_time - self.last_spawn_time >= 1000 / OBJECT_SPAWN_RATE:

                # Randomly determine the number of edges for the object and set color and size accordingly.
                # Then, create an XpObject and add it to the data list.
                # The object is a polygon with a random number of edges (3 to 6).

                self.edges = random.randint(3, 6)
                if self.edges == 3:
                    self.color = (255, 0, 0)
                    self.size = 20
                elif self.edges == 4:
                    self.color = (255, 255, 0)
                    self.size = 24
                elif self.edges == 5:
                    self.color = (0, 0, 255)
                    self.size = 28
                elif self.edges == 6:
                    self.color = (0, 255, 0)
                    self.size = 32
                else:
                    self.color = (255, 255, 255)
                    self.size = 20

                pos = Vector2(random.randint(0, MAP_W), random.randint(0, MAP_H))
                object = XpObject(pos, self.color, self.size, shape="polygon", edges=self.edges)
                data.append(object)
                self.last_spawn_time = current_time
