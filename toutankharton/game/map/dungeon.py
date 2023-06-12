from toutankharton.game.map.utils import Vector2, List2D
import random


class Dungeon(List2D):
    def __init__(self, size, room_size=Vector2(13, 13)):
        super().__init__(size, None)
        for y in range(self.size.y):
            for x in range(self.size.x):
                pos = Vector2(x, y)
                room = Room(room_size, pos)
                self.set_cell(pos, room)

        self.generate_doors_with_prim_algorithm()

        self.dead_ends = []
        self.set_dead_ends()

        self.start_room = random.choice(self.dead_ends)

        self.solved_maze = List2D(self.size, default_value=-1)
        self.breadth_first_search()
        self.end_room = None
        self.set_end_room()

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
        100: "MM",
        200: "II"
    }

    def __init__(self, room_size=Vector2(13, 13), room_pos=Vector2(0, 0)):
        super().__init__(room_size, default_value=0)
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
        self.monsters = []
        self.items = []

        self.generate_walls()
        self.generate_monsters()
        self.generate_items()

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
                    if pattern.get_cell(pattern_pos) != -1:
                        self.set_cell(pos, pattern.get_cell(pattern_pos))

    def generate_monsters(self):
        monster_count = random.randint(self.size.x * self.size.y // (self.size.x + self.size.y),
                                       self.size.x * self.size.y // (self.size.x + self.size.y // 4))
        for i in range(monster_count):
            available_cells = self.get_all_cells_of_value(0)
            if not available_cells:
                return
            random_cell = random.choice(available_cells)
            self.monsters.append(random_cell)

    def generate_items(self):
        item_count = random.randint(self.size.x * self.size.y // (self.size.x + self.size.y * 4),
                                    self.size.x * self.size.y // (self.size.x + self.size.y * 2))
        for i in range(item_count):
            available_cells = self.get_all_cells_of_value(0)
            if not available_cells:
                return
            random_cell = random.choice(available_cells)
            self.items.append(random_cell)

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
        res += self.monsters.__str__() + "\n"
        res += self.items.__str__() + "\n"
        return res
