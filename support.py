import pygame
from os import walk
from r_settings import WINDOW_WIDTH, WINDOW_HEIGHT


def import_folder(path):
    surface_list = []

    for folder_name, sub_folders, img_files in walk(path):
        for img_name in img_files:
            full_path = path + "/" + img_name
            img_surface = pygame.image.load(full_path)
            surface_list.append(img_surface)
    return surface_list


def import_folder_dict(path):
    surface_dict = {}

    for folder_name, sub_folders, img_files in walk(path):
        for img_name in img_files:
            full_path = path + "/" + img_name
            img_surface = pygame.image.load(full_path)
            surface_dict[img_name.split(".")[0]] = img_surface

    return surface_dict


class AssetImporter:
    def __init__(self, path):
        self.path = path

    def import_folder(self):
        surface_list = []

        for folder_name, sub_folders, img_files in walk(self.path):
            for img_name in img_files:
                full_path = self.path + "/" + img_name
                img_surface = pygame.image.load(full_path)
                surface_list.append(img_surface)

        return surface_list

    def import_folder_dict(self):
        surface_dict = {}

        for folder_name, sub_folders, img_files in walk(self.path):
            for img_name in img_files:
                full_path = self.path + "/" + img_name
                img_surface = pygame.image.load(full_path)
                surface_dict[img_name.split(".")[0]] = img_surface

        return surface_dict
