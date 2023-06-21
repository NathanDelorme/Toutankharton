import random

import pygame

from toutankharton.tiling.tiling import Tilemap


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, group):
        super().__init__(group)
        self.x = x
        self.y = y

        self.image_base = pygame.image.load("../toutankharton/resources/images/player.png")
        self.image_base = pygame.transform.scale(self.image_base, (self.image_base.get_width() * Tilemap.displayer_multiplier, self.image_base.get_height() * Tilemap.displayer_multiplier))

        self.image_hurt = pygame.image.load("../toutankharton/resources/images/player_hurt.png")
        self.image_hurt = pygame.transform.scale(self.image_hurt, (self.image_hurt.get_width() * Tilemap.displayer_multiplier, self.image_hurt.get_height() * Tilemap.displayer_multiplier))

        self.image = self.image_base
        self.rect = self.image.get_rect()

        self.hp = 100
        self.speed = 1
        self.cooldown = 0

    def move(self):
        keys = pygame.key.get_pressed()
        y = 0
        x = 0
        if keys[pygame.K_z]:
            y -= self.speed
        if keys[pygame.K_q]:
            x -= self.speed
        if keys[pygame.K_s]:
            y += self.speed
        if keys[pygame.K_d]:
            x += self.speed
        self.rect.move_ip(x, y)

    def update(self):
        if self.cooldown == 0:
            self.image = self.image_base
        else:
            self.image = self.image_hurt
            self.cooldown -= 1
        self.image = pygame.transform.rotate(self.image, random.randint(0, 360) * Tilemap.easter_egg)

    def action(self):
        """
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            print("attaque!")
        if keys[pygame.K_e]:
            print ("intéraction")
        if keys[pygame.K_a]:
            print ("changement d'arme")
        """






