import pygame
import sys

from Player import Player
from Crosshair import Crosshair
from Monsters import *

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

crosshair_group = pygame.sprite.Group()
crosshair = Crosshair(crosshair_group, "../assets/images/mouse.png", "../assets/images/mouse_clic.png")


player_group = pygame.sprite.Group()
player = Player(50, 50, 100, 100, (255, 255, 255), player_group, "../assets/images/player.png", "../assets/images/player_hurt.png")
monster_group = pygame.sprite.Group()
slime1 = Slime(300, 300, monster_group, 1)

pygame.mouse.set_visible(False)

while True:
    pygame.display.flip()
    screen.fill((60, 160, 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.QUIT
    """
    player.action()
    """
    player.move()
    slime1.attack(player)

    monster_group.update(player)
    monster_group.draw(screen)

    player_group.update()
    player_group.draw(screen)

    crosshair_group.draw(screen)
    crosshair_group.update()

    print(player.hp)

    clock.tick(60)

