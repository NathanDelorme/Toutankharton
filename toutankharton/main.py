import pygame
from toutankharton.game.menu.Menu import Menu

pygame.init()
game = Menu().start()
pygame.quit()
game.start(game)