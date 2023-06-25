import math
import time

import pygame

import projectiles
import utils


class Character(pygame.sprite.Sprite):
    def __init__(self, game, image, x, y, max_hp, speed, strength, attack_speed):
        super().__init__()
        self.game = game
        self.image = pygame.transform.scale(image,
                                            (image.get_width() * utils.DisplayerCalculator.factor,
                                             image.get_height() * utils.DisplayerCalculator.factor)
                                            )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.max_hp = max_hp
        self.hp = max_hp
        self.speed = speed
        self.init_speed = speed
        self.strength = strength
        self.attack_speed = attack_speed

        self.last_update_time = pygame.time.get_ticks()
        self.last_attack_time = 0

    def move(self, velocity=(0, 0)):
        if self.game.running:
            current_time = pygame.time.get_ticks()
            delta_time = current_time - self.last_update_time
            self.last_update_time = current_time
            movement = (velocity[0] * delta_time / 1000, velocity[1] * delta_time / 1000)
            if abs(movement[0]) <= 20 and abs(movement[1]) <= 20:
                self.rect.move_ip(movement[0], movement[1])


    def attack(self):
        current_time = time.time()
        if current_time - self.last_attack_time > self.attack_speed:
            self.last_attack_time = current_time
            return True
        else:
            return False


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def save(self):
        self.image = None

    def load(self):
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * utils.DisplayerCalculator.factor,
                                             self.image.get_height() * utils.DisplayerCalculator.factor)
                                            )


class Player(Character):
    stats = {
        "max_hp": 3,
        "speed": 400,
        "strength": 1,
        "attack_speed": 0.5
    }

    def __init__(self, game, x, y):
        super().__init__(game, utils.Resources.characters["player"],
                         x, y,
                         self.stats["max_hp"], self.stats["speed"], self.stats["strength"], self.stats["attack_speed"])
        self.coins = 0
        self.level = 1
        self.exp = 0
        self.equipment = []
        self.bullets = []

    def actions(self, velocity=(0, 0)):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] or keys[pygame.K_s]:
            if keys[pygame.K_z]:
                velocity = (velocity[0], velocity[1] - self.speed)
            if keys[pygame.K_s]:
                velocity = (velocity[0], velocity[1] + self.speed)

        elif keys[pygame.K_q] or keys[pygame.K_d]:
            if keys[pygame.K_q]:
                velocity = (velocity[0] - self.speed, velocity[1])
            if keys[pygame.K_d]:
                velocity = (velocity[0] + self.speed, velocity[1])
        super().move(velocity)

        for bullet in self.bullets:
            bullet.move()
            if bullet.rect.x < 0 or bullet.rect.x > self.game.screen.get_width() or bullet.rect.y < 0 or bullet.rect.y > self.game.screen.get_height():
                self.bullets.remove(bullet)

            for enemy in self.game.current_room.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.hp -= self.strength
                    if enemy.hp <= 0:
                        self.game.current_room.enemies.remove(enemy)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

        if keys[pygame.K_SPACE]:
            self.attack()

    def attack(self):
        if super().attack():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle_to_target = math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx)
            rounded_angle = round(angle_to_target / (math.pi / 4)) * (math.pi / 4)
            direction = (math.cos(rounded_angle), math.sin(rounded_angle))
            bullet = projectiles.PaperBullet(self.game, self.rect.x + self.image.get_width() // 2,
                                             self.rect.y + self.image.get_height() // 2, direction, self.stats["strength"])
            self.bullets.append(bullet)

    def load(self):
        self.image = utils.Resources.characters["player"]
        self.bullets = []
        super().load()

    def save(self):
        self.bullets = []
        super().save()

    def draw(self, screen):
        super().draw(screen)
        for bullet in self.bullets:
            bullet.draw(screen)


class Enemy(Character):
    target = None

    def __init__(self, game, image, x, y, max_hp, speed, strength, attack_speed):
        super().__init__(game, image, x, y, max_hp, speed, strength, attack_speed)

    def move(self, velocity=(0, 0)):
        super().move(velocity)

    @staticmethod
    def setTarget(target):
        Enemy.target = target


class Slime(Character):
    def __init__(self, game, image, x, y, max_hp, speed, strength, attack_speed):
        super().__init__(game, image, x, y, max_hp, speed, strength, attack_speed)

    def move(self, velocity=(0, 0)):
        if not self.game.running:
            return
        direction_x = self.game.player.rect.x - self.rect.x
        direction_y = self.game.player.rect.y - self.rect.y

        direction_length = math.hypot(direction_x, direction_y)
        if direction_length != 0:
            direction_x /= direction_length
            direction_y /= direction_length
            super().move((direction_x * self.speed, direction_y * self.speed))

    def attack(self):
        if self.rect.colliderect(self.game.player.rect) and super().attack():
            self.game.player.hp -= self.strength


class GreenSlime(Slime):
    stats = {
        "max_hp": 3,
        "speed": 250,
        "strength": 1,
        "attack_speed": 10
    }

    def __init__(self, game, x, y):
        super().__init__(game, utils.Resources.characters["green_slime"], x, y, self.stats["max_hp"],
                         self.stats["speed"], self.stats["strength"], self.stats["attack_speed"])

    def actions(self):
        super().move()
        super().attack()


    def load(self):
        self.image = utils.Resources.characters["green_slime"]
        super().load()

    def save(self):
        super().save()

class OrangeSlime(Slime):
    stats = {
        "max_hp": 5,
        "speed": 200,
        "strength": 2,
        "attack_speed": 2
    }

    def __init__(self, game, x, y):
        super().__init__(game, utils.Resources.characters["orange_slime"], x, y, self.stats["max_hp"],
                         self.stats["speed"], self.stats["strength"], self.stats["attack_speed"])

    def actions(self):
        self.move()
        super().attack()


    def load(self):
        self.image = utils.Resources.characters["orange_slime"]
        super().load()

    def save(self):
        super().save()

class RedSlime(Slime):
    stats = {
        "max_hp": 10,
        "speed": 150,
        "strength": 3,
        "attack_speed": 3
    }

    def __init__(self, game, x, y):
        super().__init__(game, utils.Resources.characters["red_slime"], x, y, self.stats["max_hp"],
                         self.stats["speed"], self.stats["strength"], self.stats["attack_speed"])

    def actions(self):
        self.move()
        super().attack()


    def load(self):
        self.image = utils.Resources.characters["red_slime"]
        super().load()

    def save(self):
        super().save()
