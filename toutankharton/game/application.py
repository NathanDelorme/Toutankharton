from toutankharton.game.map import dungeon, utils


class Game:
    def __init__(self, level=1):
        self.level = level
        self.dungeon = dungeon.Dungeon(utils.Vector2(self.level * 2 + 1, self.level * 2 + 1))
