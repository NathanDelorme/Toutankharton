import random
from enum import Enum

import characters
import items
import utils
from utils import List2D, Vector2
import pygame


class Tilemap:
    easter_egg = 0

    def __init__(self, game):
        self.game = game

        self.display_tile_size = 16 * utils.DisplayerCalculator.factor
        center_x = (self.game.screen.get_width() // 2) - (self.game.current_room.size.x * self.display_tile_size // 2)
        center_y = (self.game.screen.get_height() // 2) - (self.game.current_room.size.y * self.display_tile_size // 2)
        self.center_adjust = Vector2(center_x, center_y)
        game.walls_rect = []
        game.doors_rect = []

        for y in range(self.game.current_room.size.y):
            for x in range(self.game.current_room.size.x):
                pos = Vector2(x, y)
                cell_value = self.game.current_room.get_cell(pos)
                if cell_value == 1:
                    image = pygame.transform.scale(self.game.tileset.get_tile("rock"),
                                                   (self.display_tile_size, self.display_tile_size)), (
                    self.center_adjust.x + x * self.display_tile_size,
                    self.center_adjust.y + y * self.display_tile_size)
                    game.walls_rect.append(pygame.Rect(image[1], (self.display_tile_size, self.display_tile_size)))
                if cell_value == 2:
                    image = pygame.transform.scale(self.game.tileset.get_tile("rock"),
                                                   (self.display_tile_size, self.display_tile_size)), (
                    self.center_adjust.x + x * self.display_tile_size,
                    self.center_adjust.y + y * self.display_tile_size)
                    game.doors_rect.append(
                        (pygame.Rect(image[1], (self.display_tile_size, self.display_tile_size)), pos))
                if cell_value == 4:
                    image = pygame.transform.scale(self.game.tileset.get_tile("rock"),
                                                   (self.display_tile_size, self.display_tile_size)), (
                    self.center_adjust.x + x * self.display_tile_size,
                    self.center_adjust.y + y * self.display_tile_size)
                    game.doors_rect.append(
                        (pygame.Rect(image[1], (self.display_tile_size, self.display_tile_size)), pos))

    def draw(self):
        for y in range(self.game.current_room.size.y):
            for x in range(self.game.current_room.size.x):
                pos = Vector2(x, y)
                cell_value = self.game.current_room.get_cell(pos)
                self.game.screen.blit(pygame.transform.scale(
                    pygame.transform.rotate(self.get_tile_from_value(pos), random.randint(0, 360) * self.easter_egg),
                    (self.display_tile_size, self.display_tile_size)), (
                                          self.center_adjust.x + x * self.display_tile_size,
                                          self.center_adjust.y + y * self.display_tile_size))

    def get_tile_from_value(self, pos):
        value = self.game.current_room.get_cell(pos)
        if value == 0:
            return self.game.tileset.get_tile("floor")
        elif value == 3:
            return self.game.tileset.get_tile("floor")
        elif value == 4:
            return self.game.tileset.get_tile("hole")
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
            elif pos.y == 0:
                return self.game.tileset.get_tile("wall_north")
            else:
                count_neighbour = 0
                if self.game.current_room.get_cell(Vector2(pos.x, pos.y - 1)) == 1:
                    count_neighbour += 1
                if self.game.current_room.get_cell(Vector2(pos.x, pos.y + 1)) == 1:
                    count_neighbour += 1
                if self.game.current_room.get_cell(Vector2(pos.x - 1, pos.y)) == 1:
                    count_neighbour += 1
                if self.game.current_room.get_cell(Vector2(pos.x + 1, pos.y)) == 1:
                    count_neighbour += 1

                if count_neighbour == 0:
                    return self.game.tileset.get_tile("rock")
                elif count_neighbour == 1:
                    if self.game.current_room.get_cell(Vector2(pos.x, pos.y - 1)) == 1:
                        return pygame.transform.rotate(self.game.tileset.get_tile("bloc_north"), 180)
                    elif self.game.current_room.get_cell(Vector2(pos.x - 1, pos.y)) == 1:
                        return pygame.transform.rotate(self.game.tileset.get_tile("bloc_north"), 270)
                    elif self.game.current_room.get_cell(Vector2(pos.x + 1, pos.y)) == 1:
                        return pygame.transform.rotate(self.game.tileset.get_tile("bloc_north"), 90)
                    return self.game.tileset.get_tile("bloc_north")
                elif count_neighbour == 2:
                    if self.game.current_room.get_cell(
                            Vector2(pos.x, pos.y - 1)) == 1 and self.game.current_room.get_cell(
                            Vector2(pos.x, pos.y + 1)) == 1:
                        return self.game.tileset.get_tile("bloc_north_south")
                    elif self.game.current_room.get_cell(
                            Vector2(pos.x - 1, pos.y)) == 1 and self.game.current_room.get_cell(
                            Vector2(pos.x + 1, pos.y)) == 1:
                        return pygame.transform.rotate(self.game.tileset.get_tile("bloc_north_south"), 90)
                    elif self.game.current_room.get_cell(
                            Vector2(pos.x, pos.y - 1)) == 1 and self.game.current_room.get_cell(
                            Vector2(pos.x - 1, pos.y)) == 1:
                        return pygame.transform.rotate(self.game.tileset.get_tile("bloc_south_east"), 180)
                    elif self.game.current_room.get_cell(
                            Vector2(pos.x, pos.y - 1)) == 1 and self.game.current_room.get_cell(
                            Vector2(pos.x + 1, pos.y)) == 1:
                        return pygame.transform.rotate(self.game.tileset.get_tile("bloc_south_east"), 90)
                    elif self.game.current_room.get_cell(
                            Vector2(pos.x, pos.y + 1)) == 1 and self.game.current_room.get_cell(
                            Vector2(pos.x - 1, pos.y)) == 1:
                        return pygame.transform.rotate(self.game.tileset.get_tile("bloc_south_east"), 270)
                    elif self.game.current_room.get_cell(
                            Vector2(pos.x, pos.y + 1)) == 1 and self.game.current_room.get_cell(
                            Vector2(pos.x + 1, pos.y)) == 1:
                        return self.game.tileset.get_tile("bloc_south_east")
                elif count_neighbour == 3:
                    return self.game.tileset.get_tile("corner_wall_north_west")
                elif count_neighbour == 4:
                    return self.game.tileset.get_tile("bloc_all")
            return self.game.tileset.get_tile("rock")
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
    def __init__(self, image=utils.Resources.tileset["default"][0], tiles_name=utils.Resources.tileset["default"][1],
                 tile_size=utils.Resources.tileset["default"][2]):
        self.tile_size = tile_size
        self.tileset = image.convert_alpha()
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


class Room_Type(Enum):
    ROOM = 1
    START_ROOM = 2
    END_ROOM = 3


class Dungeon(List2D):
    def __init__(self, game, size, room_size=Vector2(13, 13)):
        super().__init__(size, None)
        self.game = game
        for y in range(self.size.y):
            for x in range(self.size.x):
                pos = Vector2(x, y)
                room = Room(game, room_size, pos)
                self.set_cell(pos, room)

        self.generate_doors_with_prim_algorithm()

        self.dead_ends = []
        self.set_dead_ends()

        self.start_room = random.choice(self.dead_ends)

        self.solved_maze = List2D(self.size, default_value=-1)
        self.breadth_first_search()
        self.end_room = None
        self.set_end_room()

        for y in range(self.size.y):
            for x in range(self.size.x):
                pos = Vector2(x, y)
                if pos != self.start_room.pos and pos != self.end_room.pos:
                    self.get_cell(pos).generate_room(Room_Type.ROOM)
                elif pos == self.start_room.pos:
                    self.get_cell(pos).generate_room(Room_Type.START_ROOM)
                elif pos == self.end_room.pos:
                    self.get_cell(pos).generate_room(Room_Type.END_ROOM)

    def set_end_room(self):
        max_distance = 0
        end = []
        for dead_end in self.dead_ends:
            if self.solved_maze.get_cell(dead_end.pos) > max_distance:
                max_distance = self.solved_maze.get_cell(dead_end.pos)
                end = [dead_end]
            elif self.solved_maze.get_cell(dead_end.pos) == max_distance:
                end.append(dead_end)
        self.end_room = random.choice(end)

    def breadth_first_search(self):
        self.solved_maze.set_cell(self.start_room.pos, 0)

        queue = [self.start_room]
        while queue:
            cell = queue.pop(0)
            for frontier in cell.doors.values():
                if self.solved_maze.get_cell(frontier.pos) == -1:
                    queue.append(frontier)
                    self.solved_maze.set_cell(frontier.pos, self.solved_maze.get_cell(cell.pos) + 1)

    def set_dead_ends(self):
        dead_ends = []
        for y in range(self.size.y):
            for x in range(self.size.x):
                if len(self.get_cell(Vector2(x, y)).doors) == 1:
                    dead_ends.append(self.get_cell(Vector2(x, y)))
        self.dead_ends = dead_ends

    def generate_doors_with_prim_algorithm(self):
        random_x = random.randint(0, self.size.x - 1)
        random_y = random.randint(0, self.size.y - 1)
        start = self.get_cell(Vector2(random_x, random_y))

        visited = [start]
        frontiers = self.get_frontiers(start)
        while frontiers:
            room = random.choice(frontiers)
            room_frontiers = self.get_frontiers(room)
            selected_rooms = []

            for temp_room in room_frontiers:
                if temp_room in visited:
                    selected_rooms.append(temp_room)

            visited.append(room)
            for temp_room in room_frontiers:
                if temp_room not in visited and temp_room not in frontiers:
                    frontiers.append(temp_room)

            selected_room = random.choice(selected_rooms)
            cardinal_point = self.get_cardinal_point(room.pos, selected_room.pos)

            room.add_door(cardinal_point, selected_room)
            selected_room.add_door(self.get_opposite_cardinal_point(cardinal_point), room)

            frontiers.remove(room)

    @staticmethod
    def get_opposite_cardinal_point(cardinal_point):
        if cardinal_point == "N":
            return "S"
        elif cardinal_point == "S":
            return "N"
        elif cardinal_point == "E":
            return "W"
        elif cardinal_point == "W":
            return "E"

    @staticmethod
    def get_cardinal_point(pos1, pos2):
        if pos1.x == pos2.x:
            if pos1.y > pos2.y:
                return "N"
            else:
                return "S"
        else:
            if pos1.x > pos2.x:
                return "W"
            else:
                return "E"

    def get_frontiers(self, room):
        frontier = []
        if room.pos.x > 0:
            frontier.append(self.get_cell(Vector2(room.pos.x - 1, room.pos.y)))
        if room.pos.x < self.size.x - 1:
            frontier.append(self.get_cell(Vector2(room.pos.x + 1, room.pos.y)))
        if room.pos.y > 0:
            frontier.append(self.get_cell(Vector2(room.pos.x, room.pos.y - 1)))
        if room.pos.y < self.size.y - 1:
            frontier.append(self.get_cell(Vector2(room.pos.x, room.pos.y + 1)))
        return frontier

    def __str__(self):
        res = ""
        res += "start : " + str(self.start_room.pos) + "\n"
        res += "end : " + str(self.end_room.pos) + "\n"
        for y_room in range(self.size.y):
            for y in range(self.get_cell(Vector2(0, y_room)).size.y):
                for x_room in range(self.size.x):
                    room = self.get_cell(Vector2(x_room, y_room))
                    for x in range(room.size.y):
                        if room.get_cell(Vector2(x, y)) in room.values_to_display.keys():
                            res += str(room.values_to_display[room.get_cell(Vector2(x, y))]).center(2) + " "
                        else:
                            res += str("??").center(2) + " "
                res += "\n"
        res += "\n"
        res += "solved maze : \n"
        res += str(self.solved_maze)
        return res


class Room(List2D):
    wall_patterns = [
        List2D(Vector2(5, 5)).load_from_list(
            [
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 1, 0],
                [-1, -1, 0, 1, 0],
                [-1, -1, 0, 0, 0]
            ]),
        List2D(Vector2(5, 5)).load_from_list(
            [
                [-1, -1, 0, 0, 0],
                [-1, -1, 0, 1, 0],
                [0, 0, 0, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]
            ]),
        List2D(Vector2(5, 5)).load_from_list(
            [
                [0, 0, 0, -1, -1],
                [0, 1, 0, -1, -1],
                [0, 1, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]
            ]),
        List2D(Vector2(5, 5)).load_from_list(
            [
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 0, 0, 0],
                [0, 1, 0, -1, -1],
                [0, 0, 0, -1, -1]
            ]),
    ]
    values_to_display = {
        0: "  ",
        1: "██",
        2: "⌈⌉",
        3: "><",
        4: "[]",
        100: "MM",
        200: "II"
    }

    def __init__(self, game, room_size=Vector2(13, 13), room_pos=Vector2(0, 0)):
        super().__init__(room_size, default_value=0)
        self.game = game
        if self.size.x < 5 or self.size.y < 5:
            raise Exception("Room size must be at least 5x5")
        if self.size.x % 2 == 0 or self.size.y % 2 == 0:
            raise Exception("Room size must be odd")
        self.pos = room_pos
        for y in range(self.size.y):
            for x in range(self.size.x):
                if x == 0 or x == self.size.x - 1 or y == 0 or y == self.size.y - 1:
                    pos = Vector2(x, y)
                    self.set_cell(pos, 1)

        self.doors = dict()
        self.enemies = []
        self.items = []

    def generate_room(self, room_type):
        if room_type == Room_Type.ROOM:
            self.generate_walls()
            self.generate_monsters()
            self.generate_items()

        elif room_type == Room_Type.START_ROOM:
            self.generate_start_room()

        elif room_type == Room_Type.END_ROOM:
            self.generate_end_room()

        for key in self.doors.keys():
            self.add_door(key, self.doors[key])

    def generate_start_room(self):
        pass

    def generate_end_room(self):
        self.enemies.append(characters.KingSlime(self.game, self.game.screen.get_width() // 2, self.game.screen.get_height() // 2))
    def add_door(self, cardinal, adjacent_room):
        if cardinal == "N":
            self.doors["N"] = adjacent_room
            temp_middle = self.size.x // 2
            self.set_cell(Vector2(temp_middle, 0), 2)

            self.set_cell(Vector2(temp_middle - 1, 1), 3)
            self.set_cell(Vector2(temp_middle, 1), 3)
            self.set_cell(Vector2(temp_middle + 1, 1), 3)

            if self.get_cell(Vector2(temp_middle - 1, 2)) != 1:
                self.set_cell(Vector2(temp_middle - 1, 2), 3)
            if self.get_cell(Vector2(temp_middle - 1, 2)) != 1:
                self.set_cell(Vector2(temp_middle - 1, 2), 3)
            if self.get_cell(Vector2(temp_middle, 2)) != 1:
                self.set_cell(Vector2(temp_middle, 2), 3)
            if self.get_cell(Vector2(temp_middle + 1, 2)) != 1:
                self.set_cell(Vector2(temp_middle + 1, 2), 3)
        elif cardinal == "S":
            self.doors["S"] = adjacent_room
            temp_middle = self.size.x // 2
            self.set_cell(Vector2(temp_middle, self.size.y - 1), 2)

            self.set_cell(Vector2(temp_middle - 1, self.size.y - 2), 3)
            self.set_cell(Vector2(temp_middle, self.size.y - 2), 3)
            self.set_cell(Vector2(temp_middle + 1, self.size.y - 2), 3)

            if self.get_cell(Vector2(temp_middle - 1, self.size.y - 3)) != 1:
                self.set_cell(Vector2(temp_middle - 1, self.size.y - 3), 3)
            if self.get_cell(Vector2(temp_middle, self.size.y - 3)) != 1:
                self.set_cell(Vector2(temp_middle, self.size.y - 3), 3)
            if self.get_cell(Vector2(temp_middle + 1, self.size.y - 3)) != 1:
                self.set_cell(Vector2(temp_middle + 1, self.size.y - 3), 3)

        elif cardinal == "E":
            self.doors["E"] = adjacent_room
            temp_middle = self.size.y // 2
            self.set_cell(Vector2(self.size.x - 1, temp_middle), 2)

            self.set_cell(Vector2(self.size.x - 2, temp_middle - 1), 3)
            self.set_cell(Vector2(self.size.x - 2, temp_middle), 3)
            self.set_cell(Vector2(self.size.x - 2, temp_middle + 1), 3)

            if self.get_cell(Vector2(self.size.x - 3, temp_middle - 1)) != 1:
                self.set_cell(Vector2(self.size.x - 3, temp_middle - 1), 3)
            if self.get_cell(Vector2(self.size.x - 3, temp_middle)) != 1:
                self.set_cell(Vector2(self.size.x - 3, temp_middle), 3)
            if self.get_cell(Vector2(self.size.x - 3, temp_middle + 1)) != 1:
                self.set_cell(Vector2(self.size.x - 3, temp_middle + 1), 3)

        elif cardinal == "W":
            self.doors["W"] = adjacent_room
            temp_middle = self.size.y // 2
            self.set_cell(Vector2(0, temp_middle), 2)

            self.set_cell(Vector2(1, temp_middle - 1), 3)
            self.set_cell(Vector2(1, temp_middle), 3)
            self.set_cell(Vector2(1, temp_middle + 1), 3)

            if self.get_cell(Vector2(2, temp_middle - 1)) != 1:
                self.set_cell(Vector2(2, temp_middle - 1), 3)
            if self.get_cell(Vector2(2, temp_middle)) != 1:
                self.set_cell(Vector2(2, temp_middle), 3)
            if self.get_cell(Vector2(2, temp_middle + 1)) != 1:
                self.set_cell(Vector2(2, temp_middle + 1), 3)

    def generate_walls(self):
        for i in range(self.size.x + self.size.y):
            pattern = random.choice(self.wall_patterns)
            if 1 >= self.size.x - pattern.size.x - 1 or 1 >= self.size.y - pattern.size.y - 1:
                continue
            random_x = random.randint(1, self.size.x - pattern.size.x - 1)
            random_y = random.randint(1, self.size.y - pattern.size.y - 1)

            for y in range(pattern.size.y):
                for x in range(pattern.size.x):
                    pattern_pos = Vector2(x, y)
                    pos = Vector2(random_x + x, random_y + y)

                    if (self.get_cell(pos) == 3 and pattern.get_cell(pattern_pos) == 0) or pattern.get_cell(
                            pattern_pos) == -1:
                        continue

                    self.set_cell(pos, pattern.get_cell(pattern_pos))

    def generate_monsters(self):
        monster_count = random.randint(1, 4)
        monster_cells = []
        for i in range(monster_count):
            available_cells = self.get_all_cells_of_value(0)
            if not available_cells:
                return
            random_cell = random.choice(available_cells)
            monster_cells.append(random_cell)

        for cell in monster_cells:
            rnd = random.randint(0, 100)
            if rnd < 50:
                self.enemies.append(characters.GreenSlime(self.game,
                    utils.DisplayerCalculator.adjust_center[0] + utils.DisplayerCalculator.factor * 2 + cell.x * 16 * utils.DisplayerCalculator.factor,
                    utils.DisplayerCalculator.adjust_center[1] + utils.DisplayerCalculator.factor * 3 + cell.y * 16 * utils.DisplayerCalculator.factor))
            elif rnd < 85:
                self.enemies.append(characters.OrangeSlime(self.game, utils.DisplayerCalculator.adjust_center[
                    0] + utils.DisplayerCalculator.factor * 1 + cell.x * 16 * utils.DisplayerCalculator.factor,
                                                           utils.DisplayerCalculator.adjust_center[
                                                               1] + utils.DisplayerCalculator.factor * 2 + cell.y * 16 * utils.DisplayerCalculator.factor))
            else:
                self.enemies.append(characters.RedSlime(self.game, utils.DisplayerCalculator.adjust_center[
                    0] + utils.DisplayerCalculator.factor * 0.5 + cell.x * 16 * utils.DisplayerCalculator.factor,
                                                        utils.DisplayerCalculator.adjust_center[
                                                            1] + utils.DisplayerCalculator.factor * 1 + cell.y * 16 * utils.DisplayerCalculator.factor))

    def generate_items(self):
        item_count = random.randint(4, 8)
        items_cells = []
        for i in range(item_count):
            available_cells = self.get_all_cells_of_value(0)
            if not available_cells:
                return
            random_cell = random.choice(available_cells)
            if random_cell in items_cells:
                continue
            items_cells.append(random_cell)

        for cell in items_cells:
            rnd = random.randint(0, 100)
            if rnd < 85:
                for i in range(random.randint(1, 3)):
                    self.items.append(items.Coin(self.game, utils.DisplayerCalculator.adjust_center[
                        0] + utils.DisplayerCalculator.factor * 6 + cell.x * 16 * utils.DisplayerCalculator.factor,
                                                 utils.DisplayerCalculator.adjust_center[
                                                     1] + utils.DisplayerCalculator.factor * 6 + cell.y * 16 * utils.DisplayerCalculator.factor))
            elif rnd < 95:
                self.items.append(items.Heal(self.game, utils.DisplayerCalculator.adjust_center[
                    0] + utils.DisplayerCalculator.factor * 4 + cell.x * 16 * utils.DisplayerCalculator.factor,
                                             utils.DisplayerCalculator.adjust_center[
                                                 1] + utils.DisplayerCalculator.factor * 4 + cell.y * 16 * utils.DisplayerCalculator.factor))
            else:
                self.items.append(items.MaxHeal(self.game, utils.DisplayerCalculator.adjust_center[
                    0] + utils.DisplayerCalculator.factor * 4 + cell.x * 16 * utils.DisplayerCalculator.factor,
                                                utils.DisplayerCalculator.adjust_center[
                                                    1] + utils.DisplayerCalculator.factor * 4 + cell.y * 16 * utils.DisplayerCalculator.factor))

    def get_all_cells_of_value(self, value):
        res = []
        for y in range(self.size.y):
            for x in range(self.size.x):
                pos = Vector2(x, y)
                if self.get_cell(pos) == value:
                    res.append(pos)
        return res

    def __str__(self):
        res = ""
        for y in range(self.size.y):
            for x in range(self.size.x):
                pos = Vector2(x, y)
                c = 0
                if self.get_cell(pos) in self.values_to_display.keys():
                    c += 1
                    res += str(self.values_to_display[self.get_cell(pos)]).center(2) + " "
                else:
                    c += 1
                    res += str("??").center(2) + " "
                if c > 1:
                    raise Exception("More than one thing in a cell")
            res += "\n"
        res += self.enemies.__str__() + "\n"
        res += self.items.__str__() + "\n"
        return res
