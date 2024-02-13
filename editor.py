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

        # Objects
        self.canvas_objects = pygame.sprite.Group()
        self.object_drag_active = False

        # Player
        CanvasObject(
            pos=(200, WINDOW_HEIGHT / 2),
            frames=self.animations[0]["frames"],
            tile_id=0,
            origin=self.origin,
            group=self.canvas_objects)

    def get_current_cell(self, obj=None):
        distance_to_origin = vector(mouse_position()) - self.origin if not obj else vector(
            obj.distance_to_origin) - self.origin

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
            r"tiles_png\water\water_bottom.png")

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

    def create_grid(self):
        # add objects to the tiles
        for tile in self.canvas_data.values():
            tile.objects = []

        for obj in self.canvas_objects:
            current_cell = self.get_current_cell(obj)
            offset = vector(obj.distance_to_origin) - (vector(current_cell) * TILE_SIZE)

            # if tile exists already
            if current_cell in self.canvas_data:
                self.canvas_data[current_cell].add_id(obj.tile_id, offset)
            # if no tile exists yet
            else:
                self.canvas_data[current_cell] = CanvasTile(obj.tile_id, offset)

        # grid offset
        left = sorted(self.canvas_data.keys(), key=lambda tile: tile[0])[0][0]
        top = sorted(self.canvas_data.keys(), key=lambda tile: tile[1])[0][1]

        # create an empty grid
        layers = {
            "water": {},
            "bg palms": {},
            "terrain": {},
            "enemies": {},
            "coins": {},
            "fg objects": {},
        }

        # fill the grid
        for tile_pos, tile in self.canvas_data.items():
            row_adjusted = tile_pos[1] - top
            col_adjusted = tile_pos[0] - left
            x = col_adjusted * TILE_SIZE
            y = row_adjusted * TILE_SIZE

            if tile.has_water:
                layers["water"][(x,y)] = tile.get_water()

            if tile.has_terrain:
                layers["terrain"][(x,y)] = tile.get_terrain() if tile.get_terrain() in self.land_tiles else "X"

            if tile.coin:
                layers["coins"][(x + TILE_SIZE // 2, y + TILE_SIZE // 2 )] = tile.coin

            if tile.enemy:
                layers["enemies"][(x,y)] = tile.enemy

            if tile.objects:
                for obj, offset in tile.objects:
                    if obj in [key for key, value in EDITOR_DATA.items() if value["style"] == "palm_bg"]:
                        layers["bg palms"][(int(x + offset.x), int(y + offset.y))] = obj
                    else:
                        layers["fg objects"][(int(x + offset.x), int(y + offset.y))] = obj

        return layers

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                print(self.create_grid())

            self.pan_input(event)
            self.selection_hotkeys(event)
            self.menu_click(event)
            self.object_drag(event)
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

            for sprite in self.canvas_objects:
                sprite.pan_pos(self.origin)

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
        self.check_neighbors(current_cell)

    def object_drag(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
            for sprite in self.canvas_objects:
                if sprite.rect.collidepoint(event.pos):
                    sprite.start_drag()
                    self.object_drag_active = True

        if event.type == pygame.MOUSEBUTTONUP and self.object_drag_active:
            for sprite in self.canvas_objects:
                if sprite.selected:
                    sprite.drag_end(self.origin)
                    self.object_drag_active = False

    def menu_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.menu.rect.collidepoint(mouse_position()):
            self.selection_index = self.menu.click(mouse_position(), mouse_buttons())

    def canvas_add(self):
        if mouse_buttons()[0] and not self.menu.rect.collidepoint(mouse_position()) and not self.object_drag_active:
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

    def draw_sky_background(self):
        # Fill the entire screen with the sky color
        self.display_surface.fill(pygame.Color(SKY_COLOR))

        # Draw the horizon
        horizon_rect = pygame.Rect(0, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT // 2)
        pygame.draw.rect(self.display_surface, pygame.Color(HORIZON_COLOR), horizon_rect)

        # Draw the sea
        sea_rect = pygame.Rect(0, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT // 2)
        pygame.draw.rect(self.display_surface, pygame.Color(SEA_COLOR), sea_rect)

        # Draw a line to separate the sky and the sea
        line_rect = pygame.Rect(0, WINDOW_HEIGHT // 2, WINDOW_WIDTH, 2)
        pygame.draw.rect(self.display_surface, pygame.Color(LINE_COLOR), line_rect)

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

            if tile.palm_fg:
                frames = self.animations[tile.palm_fg]["frames"]
                index = int(self.animations[tile.palm_fg]["frame index"])
                surf = frames[index]
                self.display_surface.blit(surf, pos)

            if tile.crate:
                frames = self.animations[tile.crate]["frames"]
                index = int(self.animations[tile.crate]["frame index"])
                surf = frames[index]
                rect = surf.get_rect(center=(pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE // 2))
                self.display_surface.blit(surf, rect)
        self.canvas_objects.draw(self.display_surface)

    def run(self, dt):
        self.event_loop()

        # Updating
        self.animation_update(dt)
        self.canvas_objects.update(dt)

        # Drawing
        self.display_surface.fill("grey")
        self.draw_sky_background()
        self.draw_level()
        self.draw_tile_lines()
        pygame.draw.circle(self.display_surface, "red", self.origin, 10)
        self.menu.display(self.selection_index)


class CanvasTile:
    def __init__(self, tile_id, offset=vector()):
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

        self.palm_fg = None

        self.crate = None
        # Objects
        self.objects = []

        self.add_id(tile_id, offset=offset)

    def add_id(self, tile_id, offset=vector()):
        options = {key: value["style"] for key, value in EDITOR_DATA.items()}
        match options[tile_id]:
            case "terrain":
                self.has_terrain = True
            case "water":
                self.has_water = True
            case "coin":
                self.coin = tile_id
            case "enemy":
                self.enemy = tile_id
            case "palm_fg":
                self.palm_fg = tile_id
            case "crate":
                self.crate = tile_id
            case _:
                if (tile_id, offset) not in self.objects:
                    self.objects.append((tile_id, offset))

    def get_water(self):
        return "bottom" if self.water_on_top else "top"

    def get_terrain(self):
        return "".join(self.terrain_neighbors)


class CanvasObject(pygame.sprite.Sprite):
    def __init__(self, pos, frames, tile_id, origin, group):
        super().__init__(group)
        self.tile_id = tile_id

        # Animation
        self.frames = frames
        self.frame_index = 0

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # Movement
        self.distance_to_origin = vector(self.rect.topleft) - origin
        self.selected = False
        self.mouse_offset = vector()

    def start_drag(self):
        self.selected = True
        self.mouse_offset = vector(mouse_position()) - vector(self.rect.topleft)

    def drag(self):
        if self.selected:
            self.rect.topleft = mouse_position() - self.mouse_offset

    def drag_end(self, origin):
        self.selected = False
        self.distance_to_origin = vector(self.rect.topleft) - origin

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.frame_index = 0 if self.frame_index >= len(self.frames) else self.frame_index
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def pan_pos(self, origin):
        self.rect.topleft = origin + self.distance_to_origin

    def update(self, dt):
        self.animate(dt)
        self.drag()
