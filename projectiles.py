import math

import pygame

import utils


class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, image, x, y, speed, damage):
        super().__init__()
        self.game = game
        self.image = pygame.transform.scale(image,
                                            (image.get_width() * utils.DisplayerCalculator.factor,
                                             image.get_height() * utils.DisplayerCalculator.factor)
                                            )
        self.rect = self.image.get_rect()
        self.rect.x = x - self.image.get_width() // 2
        self.rect.y = y - self.image.get_height() // 2
        self.speed = speed
        self.damage = damage
        self.last_update_time = pygame.time.get_ticks()

    def move(self, velocity=(0, 0)):
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time
        movement = (velocity[0] * self.speed * delta_time / 1000, velocity[1] * self.speed * delta_time / 1000)
        self.rect.move_ip(movement[0], movement[1])

    def hit(self, target):
        if self.rect.colliderect(target.rect):
            target.hp -= self.damage
            self.kill()
            self.game.projectiles.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class PaperBullet(Projectile):
    def __init__(self, game, x, y, direction, damage=1):
        super().__init__(game, utils.Resources.projectiles["paper_bullet"], x, y, 800, damage)
        self.direction = pygame.math.Vector2(direction)

    def move(self, velocity=(0, 0)):
        super().move((self.direction.x, self.direction.y))
