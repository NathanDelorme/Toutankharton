import pygame
import sys

from Player import Player

pygame.init()

display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

player_group = pygame.sprite.Group()
player = Player(50, 50, 100, 100, (255, 255, 255), player_group)

while True:
    pygame.display.flip()
    display.fill("black")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.QUIT

    player.move()

    player_group.draw(display)

    clock.tick(60)

