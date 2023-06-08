class Room:
    def __init__(self, pos, maze):
        self.south = None
        self.west = None
        self.east = None
        self.north = None
        self.pos = pos
        self.maze = maze

    def load_adjacent_rooms(self):
        if self.maze.get_cell((self.pos[0], self.pos[1] - 1)) == 0:
            self.north = self.maze.rooms.get((self.pos[0], self.pos[1] - 2))
        if self.maze.get_cell((self.pos[0] + 1, self.pos[1])) == 0:
            self.east = self.maze.rooms.get((self.pos[0] + 2, self.pos[1]))
        if self.maze.get_cell((self.pos[0] - 1, self.pos[1])) == 0:
            self.west = self.maze.rooms.get((self.pos[0] - 2, self.pos[1]))
        if self.maze.get_cell((self.pos[0], self.pos[1] + 1)) == 0:
            self.south = self.maze.rooms.get((self.pos[0], self.pos[1] + 2))

    def __str__(self):
        return f"Room {self.pos}:\nNorth: {str(self.north is not None)}\nEast: {str(self.east is not None)}\nWest: {str(self.west is not None)}\nSouth: {str(self.south is not None)}\n"