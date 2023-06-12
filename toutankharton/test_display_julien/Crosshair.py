import pygame


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, group, image_path_idle, image_path_clic):
        super().__init__(group)
        self.image_path_clic = image_path_clic
        self.image_path_idle = image_path_idle
        self.image = pygame.image.load(image_path_idle)
        self.rect = self.image.get_rect()

    def update(self):
        mouse = pygame.mouse.get_pressed()

        if mouse[0]:
            self.image = pygame.image.load(self.image_path_clic)
        else:
            self.image = pygame.image.load(self.image_path_idle)
        self.rect.topleft = pygame.mouse.get_pos()
