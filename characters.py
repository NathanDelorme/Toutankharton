import math
import random
import time

import pygame


import items
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
        "max_hp": 5,
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
        if keys[pygame.K_z]:
            velocity = (velocity[0], velocity[1] - self.speed)
        if keys[pygame.K_s]:
            velocity = (velocity[0], velocity[1] + self.speed)
        if keys[pygame.K_q]:
            velocity = (velocity[0] - self.speed, velocity[1])
        if keys[pygame.K_d]:
            velocity = (velocity[0] + self.speed, velocity[1])

        if velocity[0] != 0 and velocity[1] != 0:
            velocity = (velocity[0] / math.sqrt(2), velocity[1] / math.sqrt(2))

        super().move(velocity)

        for bullet in self.bullets:
            bullet.move()
            if bullet.rect.x < 0 or bullet.rect.x > self.game.screen.get_width() or bullet.rect.y < 0 or bullet.rect.y > self.game.screen.get_height():
                self.bullets.remove(bullet)

            for enemy in self.game.current_room.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    if enemy.is_boss:
                        if enemy.hp > 30 and enemy.hp - self.strength <= 30:
                            enemy.phase(1)
                        if enemy.hp > 20 and enemy.hp - self.strength <= 20:
                            enemy.phase(2)
                        if enemy.hp > 10 and enemy.hp - self.strength <= 10:
                            enemy.phase(3)
                        if enemy.hp - self.strength <= 0:
                            enemy.phase(4)
                    enemy.hp -= self.strength

                    if enemy.hp <= 0:
                        enemy.get_loot(self)
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
                                             self.rect.y + self.image.get_height() // 2, direction,
                                             self.stats["strength"])
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
        self.is_boss = False

    def move(self, velocity=(0, 0)):
        super().move(velocity)

    @staticmethod
    def setTarget(target):
        Enemy.target = target

    def get_loot(self, player):
        pass


class Slime(Enemy):
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
        "speed": 200,
        "strength": 1,
        "attack_speed": 1
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

    def get_loot(self, player):
        player.coins += random.randint(1, 3)


class OrangeSlime(Slime):
    stats = {
        "max_hp": 5,
        "speed": 175,
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

    def get_loot(self, player):
        player.coins += random.randint(2, 5)


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

    def get_loot(self, player):
        player.coins += random.randint(3, 8)


class KingSlime(Slime):
    stats = {
        "max_hp": 50,
        "speed": 75,
        "strength": 2,
        "attack_speed": 3
    }

    def __init__(self, game, x, y):
        super().__init__(game, utils.Resources.characters["king_slime"], x, y, self.stats["max_hp"],
                         self.stats["speed"], self.stats["strength"], self.stats["attack_speed"])
        self.is_boss = True

    def actions(self):
        self.move()
        super().attack()

    def load(self):
        self.image = utils.Resources.characters["king_slime"]
        super().load()

    def save(self):
        super().save()

    def get_loot(self, player):
        player.coins += random.randint(25, 50)
        rnd = random.randint(1, 3)
        if rnd == 1:
            self.game.current_room.items.append(items.LifeUpgrade(self.game, player.rect.x, player.rect.y))
        elif rnd == 2:
            self.game.current_room.items.append(items.AttackSpeedUpgrade(self.game, player.rect.x, player.rect.y))
        elif rnd == 3:
            self.game.current_room.items.append(items.DamageUpgrade(self.game, player.rect.x, player.rect.y))
        self.game.current_room.set_cell(utils.Vector2(self.game.current_room.size.x // 2, self.game.current_room.size.y // 2), 4)

        pos = utils.Vector2(self.game.current_room.size.x // 2, self.game.current_room.size.y // 2)
        disp_size = 16 * utils.DisplayerCalculator.factor
        image = pygame.transform.scale(self.game.tileset.get_tile("rock"),
                                       (16 * utils.DisplayerCalculator.factor, disp_size)), (
            utils.DisplayerCalculator.adjust_center[0] + pos.x * disp_size,
            utils.DisplayerCalculator.adjust_center[1] + pos.y * disp_size)
        self.game.doors_rect.append((pygame.Rect(image[1], (disp_size, disp_size)), pos))

    def phase(self, value):
        match value:
            case 1:
                self.strength = 3
                self.speed = 100
                self.game.current_room.enemies.append(GreenSlime(self.game, self.rect.topleft[0], self.rect.topleft[1]))
                self.game.current_room.enemies.append(GreenSlime(self.game, self.rect.topright[0], self.rect.topright[1]))
                self.game.current_room.enemies.append(GreenSlime(self.game, self.rect.bottomleft[0], self.rect.bottomleft[1]))
                self.game.current_room.enemies.append(GreenSlime(self.game, self.rect.bottomright[0], self.rect.bottomright[1]))
            case 2:
                self.speed = 125
                self.strength = 4
                self.game.current_room.enemies.append(OrangeSlime(self.game, self.rect.centerx, self.rect.top))
                self.game.current_room.enemies.append(GreenSlime(self.game, self.rect.topleft[0], self.rect.topleft[1]))
                self.game.current_room.enemies.append(GreenSlime(self.game, self.rect.topright[0], self.rect.topright[1]))
                self.game.current_room.enemies.append(OrangeSlime(self.game, self.rect.bottomright[0], self.rect.bottomright[1]))
                self.game.current_room.enemies.append(OrangeSlime(self.game, self.rect.bottomleft[0], self.rect.bottomleft[1]))
            case 3:
                self.speed = 150
                self.strength = 5
                self.game.current_room.enemies.append(RedSlime(self.game, self.rect.centerx, self.rect.top))
                self.game.current_room.enemies.append(RedSlime(self.game, self.rect.centerx, self.rect.bottom))
                self.game.current_room.enemies.append(OrangeSlime(self.game, self.rect.bottomright[0], self.rect.bottomright[1]))
                self.game.current_room.enemies.append(OrangeSlime(self.game, self.rect.bottomleft[0], self.rect.bottomleft[1]))
            case 4:
                self.game.current_room.enemies.append(GreenSlime(self.game, self.rect.centerx, self.rect.top))
                self.game.current_room.enemies.append(GreenSlime(self.game, self.rect.centerx, self.rect.bottom))
                self.game.current_room.enemies.append(GreenSlime(self.game, self.rect.left, self.rect.centery))
                self.game.current_room.enemies.append(GreenSlime(self.game, self.rect.right, self.rect.centery))
                self.game.current_room.enemies.append(GreenSlime(self.game, self.rect.topleft[0], self.rect.topleft[1]))
                self.game.current_room.enemies.append(GreenSlime(self.game, self.rect.topright[0], self.rect.topright[1]))
                self.game.current_room.enemies.append(GreenSlime(self.game, self.rect.bottomleft[0], self.rect.bottomleft[1]))
                self.game.current_room.enemies.append(GreenSlime(self.game, self.rect.bottomright[0], self.rect.bottomright[1]))