import pygame
import sys
from pygame.math import Vector2 as vector
from settings import *
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_position
from menu import Menu
from pygame.image import load
from support import import_folder


class Editor:
    def __init__(self, land_tiles):
        # Main setup
        self.display_surface = pygame.display.get_surface()
        self.canvas_data = {}

        # Imports
        self.land_tiles = land_tiles
        self.import_assets()

        # Navigation
        self.origin = vector()
        self.pan_active = False
        self.pan_offset = vector()

        # Support lines
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.support_line_surf.set_colorkey("green")
        self.support_line_surf.set_alpha(30)

        # Selection
        self.selection_index = 2
        self.last_selected_cell = None

        # Menu
        self.menu = Menu()

    def get_current_cell(self):
        distance_to_origin = vector(mouse_position()) - self.origin
        col = int(distance_to_origin.x / TILE_SIZE) if distance_to_origin.x > 0 else int(
            distance_to_origin.x / TILE_SIZE) - 1
        row = int(distance_to_origin.y / TILE_SIZE) if distance_to_origin.y > 0 else int(
            distance_to_origin.y / TILE_SIZE) - 1
        return col, row

    def check_neighbors(self, cell_pos):
        # Create a local cluster
        cluster_size = 3
        local_cluster = [
            (cell_pos[0] + col - int(cluster_size / 2), cell_pos[1] + row - int(cluster_size / 2))
            for col in range(cluster_size)
            for row in range(cluster_size)
        ]

        # Check neighbors
        for cell in local_cluster:
            if cell in self.canvas_data:
                self.canvas_data[cell].terrain_neighbors = []
                self.canvas_data[cell].water_on_top = False
                for name, side in NEIGHBOR_DIRECTIONS.items():
                    neighbor_cell = (cell[0] + side[0], cell[1] + side[1])

                    # Water top neighbor
                    if neighbor_cell in self.canvas_data and \
                            self.canvas_data[neighbor_cell].has_water and \
                            self.canvas_data[cell].has_water and name == "A":
                        self.canvas_data[cell].water_on_top = True

                    # Terrain neighbors
                    if neighbor_cell in self.canvas_data and self.canvas_data[neighbor_cell].has_terrain:
                        self.canvas_data[cell].terrain_neighbors.append(name)

    def import_assets(self):
        self.water_bottom = load(
            r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\water\water_bottom.png")

        # Animations
        self.animations = {3: {"frame index": 0, "frames": ["surfaces"], "length": 3}}
        for key, value in EDITOR_DATA.items():
            if value["graphics"]:
                graphics = import_folder(value["graphics"])
                self.animations[key] = {
                    "frame index": 0,
                    "frames": graphics,
                    "length": len(graphics)
                }

    def animation_update(self, dt):
        for value in self.animations.values():
            value["frame index"] += ANIMATION_SPEED * dt
            if value["frame index"] >= value["length"]:
                value["frame index"] = 0

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.pan_input(event)
            self.selection_hotkeys(event)
            self.menu_click(event)
            self.canvas_add()

            # Check for right mouse button click to delete tile
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[2]:
                self.delete_tile()

            # Check for F key press to delete tile
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.delete_tile()

    def pan_input(self, event):
        # Middle mouse button pressed / released
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
            self.pan_active = True
            self.pan_offset = vector(mouse_position()) - self.origin

        if not mouse_buttons()[1]:
            self.pan_active = False

        # Mouse wheel
        if event.type == pygame.MOUSEWHEEL:
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.origin.y -= event.y * 50
            else:
                self.origin.x -= event.y * 50

        # Panning update
        if self.pan_active:
            self.origin = vector(mouse_position()) - self.pan_offset

    def selection_hotkeys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.selection_index += 1
            if event.key == pygame.K_LEFT:
                self.selection_index -= 1
        self.selection_index = max(2, min(self.selection_index, 18))

    def delete_tile(self):
        current_cell = self.get_current_cell()

        if current_cell in self.canvas_data:
            del self.canvas_data[current_cell]

    def menu_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.menu.rect.collidepoint(mouse_position()):
            self.selection_index = self.menu.click(mouse_position(), mouse_buttons())

    def canvas_add(self):
        if mouse_buttons()[0] and not self.menu.rect.collidepoint(mouse_position()):
            current_cell = self.get_current_cell()

            if current_cell != self.last_selected_cell:
                if current_cell in self.canvas_data:
                    self.canvas_data[current_cell].add_id(self.selection_index)
                else:
                    self.canvas_data[current_cell] = CanvasTile(self.selection_index)

                self.check_neighbors(current_cell)
                self.last_selected_cell = current_cell

    def draw_tile_lines(self):
        cols = WINDOW_WIDTH // TILE_SIZE
        rows = WINDOW_HEIGHT // TILE_SIZE

        offset_offset = vector(
            x=self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE,
            y=self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE
        )

        self.support_line_surf.fill("green")

        for col in range(cols + 1):
            x = offset_offset.x + col * TILE_SIZE
            pygame.draw.line(self.support_line_surf, LINE_COLOR, (x, 0), (x, WINDOW_HEIGHT))

        for row in range(rows + 1):
            y = offset_offset.y + row * TILE_SIZE
            pygame.draw.line(self.support_line_surf, LINE_COLOR, (0, y), (WINDOW_WIDTH, y))

        self.display_surface.blit(self.support_line_surf, (0, 0))

    def draw_level(self):
        for cell_pos, tile in self.canvas_data.items():
            pos = self.origin + vector(cell_pos) * TILE_SIZE

            # Water
            if tile.has_water:
                if tile.water_on_top:
                    self.display_surface.blit(self.water_bottom, pos)
                else:
                    frames = self.animations[3]["frames"]
                    index = int(self.animations[3]["frame index"])
                    surf = frames[index]
                    self.display_surface.blit(surf, pos)

            if tile.has_terrain:
                terrain_string = "".join(tile.terrain_neighbors)
                terrain_style = terrain_string if terrain_string in self.land_tiles else "X"
                self.display_surface.blit(self.land_tiles[terrain_style], pos)

            # Coins
            if tile.coin:
                frames = self.animations[tile.coin]["frames"]
                index = int(self.animations[tile.coin]["frame index"])
                surf = frames[index]
                rect = surf.get_rect(center=(pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE // 2))
                self.display_surface.blit(surf, rect)

            # Enemies
            if tile.enemy:
                frames = self.animations[tile.enemy]["frames"]
                index = int(self.animations[tile.enemy]["frame index"])
                surf = frames[index]
                rect = surf.get_rect(center=(pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE // 2))
                self.display_surface.blit(surf, rect)

    def run(self, dt): # TODO: Dan skončil zde
        self.event_loop() # reaguje na události

        # Updating
        self.animation_update(dt)  # voda a  mince se zde animují

        # Drawing
        self.display_surface.fill("grey")  # kreslí pozadí
        self.draw_level() # kreslí dlaždice levelu(mapy)
        self.draw_tile_lines()
        pygame.draw.circle(self.display_surface, "red", self.origin, 10) # kreslí tečku na středu mapy
        self.menu.display(self.selection_index) # kreslí menu


class CanvasTile:
    def __init__(self, tile_id):
        # Terrain
        self.has_terrain = False
        self.terrain_neighbors = []

        # Water
        self.has_water = False
        self.water_on_top = False

        # Coin
        self.coin = None

        # Enemy
        self.enemy = None

        # Objects
        self.objects = []

        self.add_id(tile_id)

    def add_id(self, tile_id):
        options = {key: value["style"] for key, value in EDITOR_DATA.items()}
        if options[tile_id] == "terrain":
            self.has_terrain = True
        elif options[tile_id] == "water":
            self.has_water = True
        elif options[tile_id] == "coin":
            self.coin = tile_id
        elif options[tile_id] == "enemy":
            self.enemy = tile_id
