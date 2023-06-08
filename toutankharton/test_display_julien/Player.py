import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, width, height, pos_x, pos_y, color, group):
        super().__init__(group)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.hp = 100

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.pos_y -= 5
        if keys[pygame.K_q]:
            self.pos_x -= 5
        if keys[pygame.K_s]:
            self.pos_y += 5
        if keys[pygame.K_d]:
            self.pos_x += 5
        self.rect.center = [self.pos_x, self.pos_y]





