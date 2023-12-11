import pygame
from settings import *
from pygame.image import load

class Menu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.create_data()
        self.create_buttons()

    def create_data(self):
        self.menu_surfs = {}
        for key, value in EDITOR_DATA.items():
            if value["menu"]:
                menu_key = value["menu"]
                if menu_key not in self.menu_surfs:
                    self.menu_surfs[menu_key] = [(key, load(value["menu_surf"]))]
                else:
                    self.menu_surfs[menu_key].append((key, load(value["menu_surf"])))

    def create_buttons(self):
        size = 180
        margin = 6
        topleft = (WINDOW_WIDTH - size - margin, WINDOW_HEIGHT - size - margin)
        self.rect = pygame.Rect(topleft, (size, size))

        button_margin = 5
        generic_button_rect = pygame.Rect(self.rect.topleft, (self.rect.width / 2, self.rect.height / 2))
        self.tile_button_rect = generic_button_rect.copy().inflate(-button_margin, -button_margin)
        self.coin_button_rect = generic_button_rect.move(self.rect.height / 2, 0).inflate(-button_margin,
                                                                                          -button_margin)
        self.enemy_button_rect = generic_button_rect.move(self.rect.height / 2, self.rect.width / 2).inflate(
            -button_margin, -button_margin)
        self.palm_button_rect = generic_button_rect.move(0, self.rect.width / 2).inflate(-button_margin, -button_margin)

        self.buttons = pygame.sprite.Group()
        Button(self.tile_button_rect, self.buttons, self.menu_surfs["terrain"])
        Button(self.coin_button_rect, self.buttons, self.menu_surfs["coin"])
        Button(self.enemy_button_rect, self.buttons, self.menu_surfs["enemy"])
        Button(self.palm_button_rect, self.buttons, self.menu_surfs["palm fg"], self.menu_surfs["palm bg"])

    def click(self, mouse_position, mouse_button):
        for sprite in self.buttons:
            if sprite.rect.collidepoint(mouse_position):
                if mouse_button[1]:  # middle_mouse click
                    sprite.main_active = not sprite.main_active if sprite.items["alt"] else True
                if mouse_button[2]:  # right click
                    sprite.switch()
                return sprite.get_id()

    def highlight_indicator(self, index):
        button_rect_mapping = {
            "terrain": self.tile_button_rect,
            "coin": self.coin_button_rect,
            "enemy": self.enemy_button_rect,
            "palm fg": self.palm_button_rect,
            "palm bg": self.palm_button_rect
        }
        button_rect = button_rect_mapping.get(EDITOR_DATA[index]["menu"])
        if button_rect:
            pygame.draw.rect(self.display_surface, BUTTON_LINE_COLOR, button_rect.inflate(4, 4), 5, 4)

    def display(self, index):
        self.buttons.update()
        self.buttons.draw(self.display_surface)
        self.highlight_indicator(index)


class Button(pygame.sprite.Sprite):
    def __init__(self, rect, group, items, items_alt=None):
        super().__init__(group)
        self.image = pygame.Surface(rect.size)
        self.rect = rect
        self.items = {"main": items, "alt": items_alt}
        self.index = 0
        self.main_active = True

    def get_id(self):
        return self.items["main" if self.main_active else "alt"][self.index][0]

    def switch(self):
        self.index = (self.index + 1) % len(self.items["main" if self.main_active else "alt"])

    def update(self):
        self.image.fill(BUTTON_BG_COLOR)
        surf = self.items["main" if self.main_active else "alt"][self.index][1]
        rect = surf.get_rect(center=(self.rect.width / 2, self.rect.height / 2))
        self.image.blit(surf, rect)
