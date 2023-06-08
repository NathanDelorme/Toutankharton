import random

class Maze:
    def __init__(self, width, height):
        self.width = width * 2 + 1
        self.height = height * 2 + 1
        self.start = (1, 1)

    def get_cell(self, cell):
        if(cell[0] == 0 or cell[0] == self.width-1 or cell[1] == 0 or cell[1] == self.height-1):
            raise Exception("Cannot get border cell")
        return self.maze[cell[0]][cell[1]]

    def set_cell(self, cell, value):
        if(cell[0] == 0 or cell[0] == self.width-1 or cell[1] == 0 or cell[1] == self.height-1):
            raise Exception("Cannot set border cell")
        self.maze[cell[0]][cell[1]] = value

    def generate_prim_algorithm(self):
        self.maze = [[1 for _ in range(self.height)] for _ in range(self.width)]
        cells_width = [i for i in range(1, self.width-1, 2)]
        cells_height = [i for i in range(1, self.height-1, 2)]
        self.start = (random.choice(cells_width), random.choice(cells_height))
        #self.start = (random.randint(1, self.width-2), random.randint(1, self.height-2))
        self.set_cell(self.start, 0)
        borders = []

    def get_frontier(self, cell):
        frontier = []
        if cell[0] > 1:
            frontier.append((cell[0]-2, cell[1]))
        if cell[0] < self.width-2:
            frontier.append((cell[0]+2, cell[1]))
        if cell[1] > 1:
            frontier.append((cell[0], cell[1]-2))
        if cell[1] < self.height-2:
            frontier.append((cell[0], cell[1]+2))
        return frontier

    def __str__(self):
        res = ""
        for r in range(self.height):
            for c in range(self.width):
                cell = self.maze[c][r]
                #if (c, r) == self.start:
                    #res += "DD"
                if cell == 1:
                    res += "██"
                elif cell == 0:
                    res += "  "
            res += "\n"
        return res

m = Maze(3, 3)
m.generate_prim_algorithm()
print(m)