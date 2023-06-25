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
        self.level = 15
        self.current_room = None
        self.dungeon = None

        self.delta_time = 1 / utils.GameInfo.frame_rate
        self.running = False
        self.player = Player(self, 0, 0)
        #self.enemies = [characters.GreenSlime(self, 550, 550)]
        self.items = [items.Heal(self, 100, 100), items.MaxHeal(self, 150, 150), items.Coin(self, 200, 200),
                      items.LifeUpgrade(self, 350, 350), items.DamageUpgrade(self, 400, 400), items.AttackSpeedUpgrade(self, 450, 450),
                      items.AttackSpeedUpgrade(self, 450, 500), items.AttackSpeedUpgrade(self, 450, 550),
                      items.AttackSpeedUpgrade(self, 450, 600), items.AttackSpeedUpgrade(self, 450, 650),
                      items.AttackSpeedUpgrade(self, 500, 500), items.AttackSpeedUpgrade(self, 500, 550),
                      items.AttackSpeedUpgrade(self, 500, 600), items.AttackSpeedUpgrade(self, 500, 650),
                      items.AttackSpeedUpgrade(self, 750, 500), items.AttackSpeedUpgrade(self, 750, 550),
                      items.AttackSpeedUpgrade(self, 750, 600), items.AttackSpeedUpgrade(self, 750, 650),
                      items.AttackSpeedUpgrade(self, 700, 500), items.AttackSpeedUpgrade(self, 700, 550),
                      items.AttackSpeedUpgrade(self, 700, 600), items.AttackSpeedUpgrade(self, 500, 650),
                      items.AttackSpeedUpgrade(self, 700, 600), items.AttackSpeedUpgrade(self, 500, 650),
                      items.AttackSpeedUpgrade(self, 700, 600), items.AttackSpeedUpgrade(self, 500, 650),
                      items.AttackSpeedUpgrade(self, 700, 600), items.AttackSpeedUpgrade(self, 500, 650),
                      items.Coin(self, 300, 300), items.Coin(self, 300, 300), items.Coin(self, 300, 300),
                      items.Coin(self, 300, 300), items.Coin(self, 300, 300), items.Coin(self, 300, 300),
                      items.Coin(self, 300, 300), items.Coin(self, 300, 300), items.Coin(self, 300, 300),
                      items.Coin(self, 300, 300), items.Coin(self, 300, 300), items.Coin(self, 300, 300),
                      items.Coin(self, 300, 300), items.Coin(self, 300, 300), items.Coin(self, 300, 300),
                      items.Coin(self, 300, 300)]

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
        for item in self.items:
            item.draw(self.screen)
        for enemy in self.current_room.enemies:
            enemy.draw(self.screen)
        self.player.draw(self.screen)

    def handle_events(self):
        self.player.actions()
        for enemy in self.current_room.enemies:
            enemy.actions()
        for item in self.items:
            item.use(self.player)

    def save_game(self):
        with open("save/savegame.dat", "wb") as file:
            self.player.save()
            for enemy in self.current_room.enemies:
                enemy.save()
            for items in self.items:
                items.save()
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
            for item in game.items:
                item.load()
            for enemy in game.enemies:
                enemy.load()
            return game
