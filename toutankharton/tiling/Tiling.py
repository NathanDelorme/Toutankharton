import pygame

from toutankharton.utils import Vector2

default_tileset = "resources/images/tilesets/default_tileset.png"
default_tiles_name = ["opened_door_north", "closed_door_north", "wall_north", "corner_wall_north_west",
                      "rock", "bloc", "bloc_north", "bloc_north_south",
                      "bloc_south_east", "bloc_north_south_east", "bloc_all", "floor"]
default_tile_size = 16


class Tilemap:
    def __init__(self, game):
        self.game = game

        if self.game.screen_size.x < self.game.screen_size.y:
            temp = self.game.screen_size.x // (self.game.current_room.size.x * self.game.tileset.tile_size)
        else:
            temp = self.game.screen_size.y // (self.game.current_room.size.y * self.game.tileset.tile_size)
        self.display_tile_size = self.game.tileset.tile_size * (temp - temp % 2)

        center_x = (self.game.screen_size.x // 2) - (self.game.current_room.size.x * self.display_tile_size // 2)
        center_y = (self.game.screen_size.y // 2) - (self.game.current_room.size.y * self.display_tile_size // 2)

        self.center_adjust = Vector2(center_x, center_y)

    def draw(self):
        for y in range(self.game.current_room.size.y):
            for x in range(self.game.current_room.size.x):
                pos = Vector2(x, y)
                cell_value = self.game.current_room.get_cell(pos)
                self.game.screen.blit(pygame.transform.scale(self.get_tile_from_value(pos),
                                                             (self.display_tile_size, self.display_tile_size)), (
                                      self.center_adjust.x + x * self.display_tile_size,
                                      self.center_adjust.y + y * self.display_tile_size))

    def get_tile_from_value(self, pos):
        value = self.game.current_room.get_cell(pos)
        if value == 0:
            return self.game.tileset.get_tile("floor")
        elif value == 3:
            return self.game.tileset.get_tile("floor")
        elif value == 1:
            if pos.x == 0 and pos.y == 0:
                return self.game.tileset.get_tile("corner_wall_north_west")
            elif pos.x == 0 and pos.y == self.game.current_room.size.y - 1:
                return pygame.transform.rotate(self.game.tileset.get_tile("corner_wall_north_west"), 90)
            elif pos.x == self.game.current_room.size.x - 1 and pos.y == 0:
                return pygame.transform.rotate(self.game.tileset.get_tile("corner_wall_north_west"), 270)
            elif pos.x == self.game.current_room.size.x - 1 and pos.y == self.game.current_room.size.y - 1:
                return pygame.transform.rotate(self.game.tileset.get_tile("corner_wall_north_west"), 180)
            elif pos.x == 0:
                return pygame.transform.rotate(self.game.tileset.get_tile("wall_north"), 90)
            elif pos.x == self.game.current_room.size.x - 1:
                return pygame.transform.rotate(self.game.tileset.get_tile("wall_north"), 270)
            elif pos.y == self.game.current_room.size.y - 1:
                return pygame.transform.rotate(self.game.tileset.get_tile("wall_north"), 180)
            return self.game.tileset.get_tile("wall_north")
        elif value == 2:
            if pos.x == 0:
                return pygame.transform.rotate(self.game.tileset.get_tile("opened_door_north"), 90)
            elif pos.x == self.game.current_room.size.x - 1:
                return pygame.transform.rotate(self.game.tileset.get_tile("opened_door_north"), 270)
            if pos.y == self.game.current_room.size.y - 1:
                return pygame.transform.rotate(self.game.tileset.get_tile("opened_door_north"), 180)
            return self.game.tileset.get_tile("opened_door_north")
        else:
            error = pygame.Surface([self.game.tileset.tile_size, self.game.tileset.tile_size])
            error.fill((255, 100, 98))
            return error


class Tileset:
    def __init__(self, path=default_tileset, tiles_name=None, tile_size=16):
        if tiles_name is None:
            tiles_name = default_tiles_name
        self.tile_size = tile_size
        self.tileset = pygame.image.load(path).convert_alpha()
        self.tiles_name = tiles_name
        self.tiles = dict()
        self.load_tiles()

    def load_tiles(self):
        tiles_count = 0
        for y in range(0, self.tileset.get_height(), self.tile_size):
            for x in range(0, self.tileset.get_width(), self.tile_size):
                tiles_count += 1
                self.tiles[self.tiles_name[tiles_count - 1]] = self.tileset.subsurface(x, y, self.tile_size,
                                                                                       self.tile_size)

        if tiles_count != len(self.tiles_name):
            raise Exception("Error while loading tiles from tileset, check the tiles_name list")

    def get_tile(self, name):
        if name not in self.tiles:
            raise Exception("Tile not found in tileset")
        return self.tiles[name]
