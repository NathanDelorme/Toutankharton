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
                res += str(self.get_cell(pos))
            res += "\n"
        return res
