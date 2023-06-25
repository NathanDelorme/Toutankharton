import pygame
from enum import Enum

pygame.init()


class MenuOption(Enum):
    NEW_GAME = 1
    CONTINUE = 2
    QUIT = 3
    UNPAUSE = 5


class GameInfo:
    version = "0.0.1"
    frame_rate = 60

class Resources:
    tileset = {
        "default": (pygame.image.load("assets/tilesets/default_tileset.png"),
                    ["opened_door_north", "closed_door_north", "wall_north", "corner_wall_north_west",
                     "rock", "bloc", "bloc_north", "bloc_north_south",
                     "bloc_south_east", "bloc_north_south_east", "bloc_all", "floor", "hole"],
                    16)
    }
    fonts = {
        "default": pygame.font.Font("assets/gui/font/Silkscreen-Regular.ttf", 16),
    }
    gui = {
        "crosshair": pygame.image.load("assets/gui/crosshair/crosshair.png"),
        "filled_heart_frame": pygame.image.load("assets/gui/hud/filled_heart_frame.png"),
        "empty_heart_frame": pygame.image.load("assets/gui/hud/empty_heart_frame.png"),
        "coin": pygame.image.load("assets/gui/hud/coin.png"),
        "attack_damage": pygame.image.load("assets/gui/hud/attack_damage.png"),
        "attack_speed": pygame.image.load("assets/gui/hud/attack_speed.png"),
    }

    characters = {
        "player": pygame.image.load("assets/characters/player/player.png"),
        "green_slime": pygame.image.load("assets/characters/slimes/green_slime.png"),
        "orange_slime": pygame.image.load("assets/characters/slimes/orange_slime.png"),
        "red_slime": pygame.image.load("assets/characters/slimes/red_slime.png"),
        "king_slime": pygame.image.load("assets/characters/slimes/king_slime.png")
    }

    projectiles = {
        "paper_bullet": pygame.image.load("assets/projectiles/paper_bullet.png")
    }

    items = {
        "heal": pygame.image.load("assets/items/heal.png"),
        "max_heal": pygame.image.load("assets/items/max_heal.png"),
        "coin": pygame.image.load("assets/items/coin.png"),
        "attack_damage_upgrade": pygame.image.load("assets/items/damage_upgrade.png"),
        "attack_speed_upgrade": pygame.image.load("assets/items/attack_speed_upgrade.png"),
        "life_upgrade": pygame.image.load("assets/items/life_upgrade.png"),
    }

    items_animations = {

    }

    loaded = False

    @staticmethod
    def load():
        if Resources.loaded:
            return
        sprite_sheet = pygame.image.load("assets/items/coin.png")
        images = []
        for i in range(0, sprite_sheet.get_height(), 4):
            for j in range(0, sprite_sheet.get_width(), 4):
                images.append(sprite_sheet.subsurface(j, i, 4, 4))
        Resources.items_animations["coin"] = (images, 200)
        Resources.loaded = True


class DisplayerCalculator:
    adjust_center = (0, 0)
    factor = 1

    @staticmethod
    def computeFactor(screen_size, map_size=(13, 13), tile_size=16):
        if screen_size[0] < screen_size[1]:
            DisplayerCalculator.factor = screen_size[0] // (map_size[0] * tile_size)
        else:
            DisplayerCalculator.factor = screen_size[1] // (map_size[1] * tile_size)

        center_x = (screen_size[0] // 2) - (map_size[0] * tile_size * DisplayerCalculator.factor // 2)
        center_y = (screen_size[1] // 2) - (map_size[1] * tile_size * DisplayerCalculator.factor // 2)
        DisplayerCalculator.adjust_center = (center_x, center_y)


class MetaVector2(type):
    def __repr__(cls):
        return "__repr__ on the metaclass"
    def __str__(cls):
        return "__str__ on the metaclass"

class Vector2(metaclass=MetaVector2):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        return False


class List2D:
    def __init__(self, size, default_value=0):
        self.size = size
        self.table = [[default_value for x in range(self.size.x)] for y in range(self.size.y)]

    def load_from_list(self, list2D):
        self.table = list2D
        self.size = Vector2(len(list2D), len(list2D[0]))
        return self

    def get_cell(self, pos):
        return self.table[pos.y][pos.x]

    def set_cell(self, pos, value):
        self.table[pos.y][pos.x] = value

    def __str__(self):
        res = ""
        for y in range(self.size.y):
            for x in range(self.size.x):
                pos = Vector2(x, y)
                res += str(self.get_cell(pos)).center(3)
            res += "\n"
        return res
