import Tile
import pygame
import sys
from pytmx.util_pygame import load_pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
tmx_data = load_pygame("test.tmx")
sprite_group = pygame.sprite.Group()

for layer in tmx_data.visible_layers:
    if hasattr(layer,'data'):
        for x,y,surf in layer.tiles():
            pos = (x * 16 + SCREEN_WIDTH//2 - (5*16*2), y * 16 + SCREEN_HEIGHT//2 - (5*16*2))
            print(pos)
            Tile.TileBase(pos = pos, image = surf, groups = sprite_group)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill("black")
    sprite_group.draw(screen)
    pygame.display.flip()