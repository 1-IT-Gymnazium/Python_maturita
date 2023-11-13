TILE_SIZE = 64
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
ANIMATION_SPEED = 8

EDITOR_DATA = {
    0: {"style": "player", "type": "object", "menu": None, "menu_surf": None, "preview": None, "graphics": None},
    1: {"style": "sky", "type": "object", "menu": None, "menu_surf": None, "preview": None, "graphics": None},

    2: {"style": "terrain", "type": "tile", "menu": "terrain",
        "menu_surf": r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\land\X.png",
        "preview": r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\land\X.png",
        "graphics": None},

    3: {"style": "water", "type": "tile", "menu": "terrain",
        "menu_surf": r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\water_bottom.png",
        "preview": r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\water_bottom.png",
        "graphics": r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\water_animation"},

    4: {"style": "coin", "type": "tile", "menu": "coin",
        "menu_surf": r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\SILVER_COIN.png",
        "preview": r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\SILVER_COIN.png",
        "graphics": r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\SILVER_COIN.png"},
    5: {"style": "coin", "type": "tile", "menu": "coin",
        "menu_surf": r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\GOLD_COIN.png",
        "preview": r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\GOLD_COIN.png",
        "graphics": r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\GOLD_COIN.png"},

    7: {'style': 'enemy', 'type': 'tile', 'menu': 'enemy',
        'menu_surf': r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\SPIKE_BLOCK.png",
        'preview': r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\SPIKE_BLOCK.png",
        'graphics': r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\SPIKE_BLOCK.png"},

    8: {'style': 'palm_fg', 'type': 'object', 'menu': 'palm fg',
        'menu_surf': r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\PALM.png",
        'preview': r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\PALM.png",
        'graphics': r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\PALM.png"},

    9: {'style': 'palm_bg', 'type': 'object', 'menu': 'palm bg',
        'menu_surf': r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\BG_PALM.png",
        'preview': r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\BG_PALM.png",
        'graphics': r"C:\Users\erikd\Pygame maturita\Python Maturitní projekt\tiles_png\BG_PALM.png"},

}

NEIGHBOR_DIRECTIONS = {
    'A': (0, -1),
    'B': (1, -1),
    'C': (1, 0),
    'D': (1, 1),
    'E': (0, 1),
    'F': (-1, 1),
    'G': (-1, 0),
    'H': (-1, -1)
}

LEVEL_LAYERS = {
    'clouds': 1,
    'ocean': 2,
    'bg': 3,
    'water': 4,
    'main': 5
}

# colors
SKY_COLOR = '#ddc6a1'
SEA_COLOR = '#92a9ce'
HORIZON_COLOR = '#f5f1de'
HORIZON_TOP_COLOR = '#d1aa9d'
LINE_COLOR = 'black'
BUTTON_BG_COLOR = "#33323d"
BUTTON_LINE_COLOR = "#f5f1de"
