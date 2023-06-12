import pygame
import sys, os
from toutankharton.game.map import dungeon, utils
import pickle

from toutankharton.game.map.utils import Vector2


class Game:
    def __init__(self, level=1):
        if level < 1:
            raise Exception("Level must be greater than 0")
        self.level = level
        self.dungeon = None

        self.screen_size = None
        self.screen = None

    @staticmethod
    def start(game):
        pygame.init()
        game.screen_size = Vector2(pygame.display.Info().current_w, pygame.display.Info().current_h - 60)
        game.screen = pygame.display.set_mode((game.screen_size.x, game.screen_size.y))
        if game.dungeon is None:
            game.dungeon = dungeon.Dungeon(Vector2(game.level+1, game.level+1))
        print(game.dungeon)

        while True:
            pygame.display.flip()
            game.screen.fill("black")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.save_state()
                    pygame.quit()
                    sys.exit()

    def save_state(self):
        with open("savegame.dat", "wb") as file:
            self.screen = None
            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_state():
        if not os.path.isfile("savegame.dat"):
            return Game()
        with open("savegame.dat", "rb") as file:
            return pickle.load(file)

    def generate_dungeon(self):
        self.dungeon = dungeon.Dungeon(utils.Vector2(self.level+1, self.level+1))

    def __str__(self):
        return "Game level: {}".format(self.level)