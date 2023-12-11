import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT
from editor import Editor
from pygame.image import load
from support import import_folder_dict


class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.import_assets()

        self.editor = Editor(self.land_tiles)

        # Cursor
        cursor_surf = load(
            r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\mouse_cursor.png").convert_alpha() #TODO: predelat na relativni
        cursor = pygame.cursors.Cursor((0, 0), cursor_surf)
        pygame.mouse.set_cursor(cursor)

    def import_assets(self):
        self.land_tiles = import_folder_dict(
            r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\land"
        )

    def run(self):
        while True:
            dt = self.clock.tick() / 1000

            self.editor.run(dt)
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.run()
