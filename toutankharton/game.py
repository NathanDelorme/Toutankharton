import pygame
import sys, os
import pickle

from toutankharton.map import dungeon
from toutankharton import utils
from toutankharton.entities.player import Player
from toutankharton.menu.crosshair import Crosshair
from toutankharton.entities.monsters import Slime
from toutankharton.tiling import tiling
from toutankharton.utils import Vector2


class Game:
    def __init__(self, level=1):
        if level < 1:
            raise Exception("Level must be greater than 0")

        self.level = level
        self.current_room = None
        self.dungeon = None

        self.screen_size = None
        self.screen = None
        self.tileset = None

    @staticmethod
    def start(game):
        pygame.init()
        game.screen_size = utils.Vector2(pygame.display.Info().current_w, pygame.display.Info().current_h - 100)
        game.screen = pygame.display.set_mode((game.screen_size.x, game.screen_size.y))

        game.level = 2
        if game.dungeon is None:
            game.generate_dungeon()

        game.tileset = tiling.Tileset()
        game.current_room = game.dungeon.get_cell(Vector2(1, 1))
        print(game.current_room)
        tilemap = tiling.Tilemap(game)
        clock = pygame.time.Clock()

        crosshair_group = pygame.sprite.Group()
        crosshair = Crosshair(crosshair_group, "../toutankharton/resources/images/mouse.png", "../toutankharton/resources/images/mouse_clic.png")

        pygame.mouse.set_visible(False)
        player_group = pygame.sprite.Group()
        player = Player(100, 100, player_group)
        monster_group = pygame.sprite.Group()
        slime1 = Slime(300, 300, monster_group, 1)

        pygame.mouse.set_visible(False)
        clock.tick(2)

        while True:
            pygame.display.flip()
            game.screen.fill("black")
            tilemap.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.save_state()
                    pygame.quit()
                    sys.exit()

            previous_pos = player.rect.topleft
            player.move()

            for wall in tilemap.walls_rect:
                if player.rect.colliderect(wall):
                    player.rect.topleft = previous_pos

            slime1.attack(player)

            monster_group.update(player)
            monster_group.draw(game.screen)

            player_group.update()
            player_group.draw(game.screen)

            crosshair_group.draw(game.screen)
            crosshair_group.update()

    def save_state(self):
        with open("resources/save/savegame.dat", "wb") as file:
            self.screen = None
            self.tileset = None
            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_state():
        if not os.path.isfile("resources/save/savegame.dat"):
            return Game()
        with open("resources/save/savegame.dat", "rb") as file:
            return pickle.load(file)

    def generate_dungeon(self):
        self.dungeon = dungeon.Dungeon(utils.Vector2(self.level + 1, self.level + 1))
        self.current_room = self.dungeon.start_room

    def __str__(self):
        return "Game level: {}".format(self.level)