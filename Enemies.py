from pygame.image import load
from r_settings import EDITOR_DATA


class Ball:
    def __init__(self, x, y, velocity_x, velocity_y=0, height=10, width=10):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.height = height
        self.width = width


class Cannon:
    right_cannon = load(EDITOR_DATA[8]["graphics"])
    left_cannon = load(EDITOR_DATA[9]["graphics"])

    def __init__(self, x, y, facing="right"):
        self.x = x
        self.y = y
        self.facing = facing

    def draw(self):
        pass
