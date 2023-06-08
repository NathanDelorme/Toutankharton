import random
from room import Room


class Maze:
    def __init__(self, width, height):
        self.maze = []
        self.width = width * 2 + 1
        self.height = height * 2 + 1
        self.rooms_x = [x for x in range(1, self.width - 1, 2)]
        self.rooms_y = [y for y in range(1, self.height - 1, 2)]
        self.generate_prim_algorithm()
        self.dead_ends = self.get_dead_ends()
        self.start = random.choice(self.dead_ends)
        self.breadth_first_search(self.start)
        self.end = self.get_end()
        print(self.display_solved_maze())

        self.rooms = dict()
        for x in self.rooms_x:
            for y in self.rooms_y:
                self.rooms[(x, y)] = Room((x, y), self)

        for room in self.rooms.values():
            room.load_adjacent_rooms()
            print(room)

    def get_end(self):
        max_distance = 0
        end = []
        for x in range(self.width):
            for y in range(self.height):
                if self.solved_maze[x][y] > max_distance:
                    max_distance = self.solved_maze[x][y]
                    end = [(x, y)]
                elif self.solved_maze[x][y] == max_distance:
                    end.append((x, y))
        return random.choice(end)

    def breadth_first_search(self, start):
        self.solved_maze = [[-1 for _ in range(self.height)] for _ in range(self.width)]
        for x in range(self.width):
            for y in range(self.height):
                if self.get_cell((x, y)) == 1:
                    self.solved_maze[x][y] = -2
        self.solved_maze[start[0]][start[1]] = 0
        queue = [start]
        while queue:
            cell = queue.pop(0)
            for neighbor in self.get_neighbors(cell):
                if self.solved_maze[neighbor[0]][neighbor[1]] != -2 and self.solved_maze[neighbor[0]][neighbor[1]] == -1:
                    queue.append(neighbor)
                    self.solved_maze[neighbor[0]][neighbor[1]] = self.solved_maze[cell[0]][cell[1]] + 1

    def get_dead_ends(self):
        dead_ends = []
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if self.maze[x][y] == 0:
                    count_neighbors_room = 0
                    neighbors = [self.maze[x - 1][y], self.maze[x + 1][y], self.maze[x][y - 1], self.maze[x][y + 1]]
                    for neighbor in neighbors:
                        if neighbor == 0:
                            count_neighbors_room += 1
                    if count_neighbors_room == 1:
                        dead_ends.append((x, y))
        return dead_ends

    def get_cell(self, cell):
        return self.maze[cell[0]][cell[1]]

    def set_cell(self, cell, value):
        if cell[0] == 0 or cell[0] == self.width - 1 or cell[1] == 0 or cell[1] == self.height - 1:
            raise Exception("Cannot set border cell")
        self.maze[cell[0]][cell[1]] = value

    def generate_prim_algorithm(self):
        self.maze = [[1 for _ in range(self.height)] for _ in range(self.width)]
        self.start = (random.choice(self.rooms_x), random.choice(self.rooms_y))
        self.set_cell(self.start, 0)

        in_maze = [self.start]
        borders = []
        borders += self.get_frontiers(self.start)

        while borders:
            cell1 = random.choice(borders)
            self.set_cell(cell1, 0)
            cell2 = None
            for new_cell in in_maze:
                if self.is_adjacent(cell1, new_cell):
                    cell2 = new_cell
                    break
            in_maze.append(cell1)
            for border in self.get_frontiers(cell1):
                if border not in in_maze and border not in borders:
                    borders.append(border)
            wall = self.get_wall(cell1, cell2)
            self.set_cell(wall, 0)
            borders.remove(cell1)

    @staticmethod
    def is_adjacent(cell1, cell2):
        return (cell1[0] == cell2[0] and abs(cell1[1] - cell2[1]) == 2) or (cell1[1] == cell2[1] and abs(cell1[0] - cell2[0]) == 2)

    def get_wall(self, cell1, cell2):
        if not self.is_adjacent(cell1, cell2):
            raise Exception("Cells are not adjacent")
        x = ((cell1[0] + cell2[0]) // 2) + ((cell1[1] + cell2[1]) % 2)
        y = ((cell1[1] + cell2[1]) // 2) + ((cell1[1] + cell2[1]) % 2)
        return (x, y)

    def get_frontiers(self, cell):
        frontier = []
        if cell[0] > 1:
            frontier.append((cell[0] - 2, cell[1]))
        if cell[0] < self.width - 2:
            frontier.append((cell[0] + 2, cell[1]))
        if cell[1] > 1:
            frontier.append((cell[0], cell[1] - 2))
        if cell[1] < self.height - 2:
            frontier.append((cell[0], cell[1] + 2))
        return frontier

    def get_neighbors(self, cell):
        neighbors = []
        if cell[0] > 0:
            neighbors.append((cell[0] - 1, cell[1]))
        if cell[0] < self.width - 1:
            neighbors.append((cell[0] + 1, cell[1]))
        if cell[1] > 0:
            neighbors.append((cell[0], cell[1] - 1))
        if cell[1] < self.height - 1:
            neighbors.append((cell[0], cell[1] + 1))
        return neighbors

    def display_solved_maze(self):
        res = ""
        for r in range(self.height):
            for c in range(self.width):
                cell = self.solved_maze[c][r]
                if (c, r) == self.start:
                    res += "SS".center(4," ")
                elif (c, r) == self.end:
                    res += "EE".center(4," ")
                elif cell == -2:
                    res += "████"
                else:
                    res += str(cell).center(4," ")
            res += "\n"
        return res

    def __str__(self):
        res = ""
        for r in range(self.height):
            for c in range(self.width):
                cell = self.maze[c][r]
                if (c, r) == self.start:
                    res += "SS"
                if (c, r) == self.end:
                    res += "EE"
                elif cell == 1:
                    res += "██"
                elif cell == 0:
                    res += "  "
            res += "\n"
        return res

for i in range(1):
    m = Maze(3, 3)
