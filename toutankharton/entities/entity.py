import pygame
import pygame.rect


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, group, img_path, width, height):
        super().__init__(group)
        self.x = x
        self.y = y
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.topleft = (self.x, self.y)

