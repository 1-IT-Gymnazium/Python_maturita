import pygame
from os import walk


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
