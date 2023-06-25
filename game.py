import pygame

import characters
import items
import utils
import pickle
from characters import Player
import map


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.screen = pygame.display.set_mode((720, 480))
        utils.DisplayerCalculator.computeFactor(self.screen.get_size())
        self.tileset = map.Tileset()
        self.clock = pygame.time.Clock()
        self.level = 1
        self.current_room = None
        self.dungeon = None

        self.delta_time = 1 / utils.GameInfo.frame_rate
        self.running = False
        self.player = Player(self, 0, 0)

    def start_dungeon(self):
        if self.dungeon is None:
            self.generate_dungeon(self)
            self.current_room = self.dungeon.start_room
            self.player.rect.center = self.screen.get_rect().center
            print(self.dungeon)
            return map.Tilemap(self)
        return map.Tilemap(self)
    def generate_dungeon(self, game):
        self.dungeon = map.Dungeon(game, utils.Vector2(self.level + 1, self.level + 1))
        self.current_room = self.dungeon.start_room

    def draw(self):
        for enemy in self.current_room.enemies:
            enemy.draw(self.screen)
        for item in self.current_room.items:
            item.draw(self.screen)
        self.player.draw(self.screen)

    def handle_events(self):
        self.player.actions()
        for enemy in self.current_room.enemies:
            enemy.actions()
        for item in self.current_room.items:
            item.use(self.player)

    def save_game(self):
        with open("save/savegame.dat", "wb") as file:
            self.player.save()
            for y in range(self.dungeon.size.y):
                for x in range(self.dungeon.size.x):
                    room = self.dungeon.get_cell(utils.Vector2(x, y))
                    for enemy in room.enemies:
                        enemy.save()
                    for item in room.items:
                        item.save()
            self.tileset = None
            self.screen = None
            self.clock = None
            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_game():
        with open("save/savegame.dat", "rb") as file:
            game = pickle.load(file)
            game.running = False
            game.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            #self.screen = pygame.display.set_mode((720, 480))
            utils.DisplayerCalculator.computeFactor(game.screen.get_size())
            game.tileset = map.Tileset()
            game.clock = pygame.time.Clock()
            game.player.load()
            for y in range(game.dungeon.size.y):
                for x in range(game.dungeon.size.x):
                    room = game.dungeon.get_cell(utils.Vector2(x, y))
                    for enemy in room.enemies:
                        enemy.load()
                    for item in room.items:
                        item.load()
            return game
