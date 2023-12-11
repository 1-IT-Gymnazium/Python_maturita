from settings import TILE_SIZE


class Tile:
    def __init__(self, x, y, height=TILE_SIZE, width=TILE_SIZE):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
