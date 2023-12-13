import pygame.draw
from pygame.image import load
from settings import TILE_SIZE, ANIMATION_SPEED
from support import import_folder


class Tile:
    image_path = None  # Cesta k obrázku pro konkrétní typ dlaždice

    def __init__(self):
        self.image = load(Tile.image_path) if Tile.image_path else None
        self.frame_index = 0
        self.frames = []  # Seznam snímků pro animaci


    def animate(self, dt):
        if self.frames:
            self.frame_index += ANIMATION_SPEED * dt
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]

    def draw(self, surface, position):
        if self.image:
            surface.blit(self.image, position)


class WaterTile(Tile):
    image_path = r"tiles_png\water\animations"

    def __init__(self):
        super().__init__()
        # Načtení snímků pro vodní dlaždici
        self.frames = import_folder(WaterTile.image_path)


class TerrainTile(Tile):
    image_path = r"tiles_png\land\X.png"

    def __init__(self):
        super().__init__()
        # Načtení obrázku pro terénní dlaždici
