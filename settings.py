TILE_SIZE = 64
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 800
ANIMATION_SPEED = 5
FPS = 60

EDITOR_DATA = {
    0: {"style": "player", "type": "object", "menu": None, "menu_surf": None, "preview": None, "graphics": None},
    1: {"style": "sky", "type": "object", "menu": None, "menu_surf": None, "preview": None, "graphics": None},

    2: {"style": "terrain", "type": "tile", "menu": "terrain",
        "menu_surf": r"tiles_png\land\X.png",
        "preview": r"tiles_png\land\X.png",
        "graphics": None},

    3: {"style": "water", "type": "tile", "menu": "terrain",
        "menu_surf": r"tiles_png\water\water_bottom.png",
        "preview": r"tiles_png\water\water_bottom.png",
        "graphics": r"tiles_png\water\animations"},

    4: {"style": "coin", "type": "tile", "menu": "coin",
        "menu_surf": r"tiles_png\silver_coin\SILVER_COIN.png",
        "preview": r"tiles_png\silver_coin\SILVER_COIN.png",
        "graphics": r"tiles_png\silver_coin\animations"},
    5: {"style": "coin", "type": "tile", "menu": "coin",
        "menu_surf": r"tiles_png\gold_coin\GOLD_COIN.png",
        "preview": r"tiles_png\gold_coin\GOLD_COIN.png",
        "graphics": r"tiles_png\gold_coin\animations"},

    7: {'style': 'enemy', 'type': 'tile', 'menu': 'enemy',
        'menu_surf': r"tiles_png\spikes\SPIKE_BLOCK.png",
        'preview': r"tiles_png\spikes\SPIKE_BLOCK.png",
        'graphics': r"tiles_png\spikes"},
    8: {'style': 'enemy', 'type': 'tile', 'menu': 'enemy',
        'menu_surf': r"tiles_png\canon_left\CANON_LEFT.png",
        'preview': r"tiles_png\canon_left\CANON_LEFT.png",
        'graphics': r"tiles_png\canon_left"},
    9: {'style': 'enemy', 'type': 'tile', 'menu': 'enemy',
        'menu_surf': r"tiles_png\canon_right\CANON_RIGHT.png",
        'preview': r"tiles_png\canon_right\CANON_RIGHT.png",
        'graphics': r"tiles_png\canon_right"},

    10: {'style': 'palm_fg', 'type': 'object', 'menu': 'objects',
         'menu_surf': r"tiles_png\large_fg\large_1.png",
         'preview': r"tiles_png\large_fg\large_1.png",
         'graphics': r"tiles_png\large_fg\animations"},

    11: {'style': 'crate', 'type': 'object', 'menu': 'objects',
         'menu_surf': r"tiles_png\crate\crate.png",
         'preview': r"tiles_png\crate\crate.png",
         'graphics': r"tiles_png\crate"},

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
