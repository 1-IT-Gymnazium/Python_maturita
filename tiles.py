import pygame.draw

from settings import TILE_SIZE


class Tile:
    def __init__(self, x, y, height=TILE_SIZE, width=TILE_SIZE, surface=pygame.display.get_surface()):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.animations = []
        self.surface = surface

    def draw(self):
        rect = pygame.draw.rect(self.surface, "green", (self.x, self.y, self.width, self.height), 0)
        self.display_surface.blit(self.surface, rect)
