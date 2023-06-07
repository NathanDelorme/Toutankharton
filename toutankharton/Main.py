import pygame, sys
from pytmx.util_pygame import load_pygame
import Tile

pygame.init()
screen = pygame.display.set_mode((640, 480))
tmxdata = load_pygame("C:\\Users\\natha\Desktop\\test.tmx")
sprite_group = pygame.sprite.Group()

for layer in tmxdata.layers:
    if hasattr(layer.data):
        print

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            sys.exit()
    screen.fill("black")
    sprite_group.draw(screen)
    pygame.display.update()