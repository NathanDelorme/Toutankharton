import math

import pygame

import utils


class Item(pygame.sprite.Sprite):
    def __init__(self, game, image, x, y):
        super().__init__()
        self.game = game
        self.image = pygame.transform.scale(image,
                                            (image.get_width() * utils.DisplayerCalculator.factor,
                                             image.get_height() * utils.DisplayerCalculator.factor)
                                            )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def use(self, target):
        self.kill()
        self.game.current_room.items.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def save(self):
        if hasattr(self, "images"):
            self.images = None
        self.image = None

    def load(self):
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * utils.DisplayerCalculator.factor,
                                             self.image.get_height() * utils.DisplayerCalculator.factor)
                                            )


class Heal(Item):
    def __init__(self, game, x, y):
        super().__init__(game, utils.Resources.items["heal"], x, y)

    def use(self, target):
        if self.rect.colliderect(target.rect) and target.hp < target.max_hp:
            target.hp += 1
            super().use(target)

    def load(self):
        self.image = utils.Resources.items["heal"]
        super().load()


class MaxHeal(Item):
    def __init__(self, game, x, y):
        super().__init__(game, utils.Resources.items["max_heal"], x, y)

    def use(self, target):
        if self.rect.colliderect(target.rect) and target.hp < target.max_hp:
            target.hp = target.max_hp
            super().use(target)

    def load(self):
        self.image = utils.Resources.items["max_heal"]
        super().load()

class Coin(Item):
    def __init__(self, game, x, y):
        self.images = utils.Resources.items_animations["coin"][0]
        self.current_frame = 0
        self.animation_tick = 0
        self.last_update_time = pygame.time.get_ticks()
        super().__init__(game, self.images[self.current_frame], x, y)

    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time
        self.animation_tick += delta_time

        if self.animation_tick > utils.Resources.items_animations["coin"][1]:
            self.animation_tick = 0
            self.current_frame += 1

            if self.current_frame >= len(self.images):
                self.current_frame = 0

            self.image = self.images[self.current_frame]
            self.image = pygame.transform.scale(self.image,
                                                (self.image.get_width() * utils.DisplayerCalculator.factor,
                                                 self.image.get_height() * utils.DisplayerCalculator.factor))

        super().draw(screen)

    def use(self, target):
        if self.rect.colliderect(target.rect):
            target.coins += 1
            super().use(target)

    def load(self):
        self.images = utils.Resources.items_animations["coin"][0]
        self.image = self.images[self.current_frame]
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * utils.DisplayerCalculator.factor,
                                             self.image.get_height() * utils.DisplayerCalculator.factor))

class LifeUpgrade(Item):
    def __init__(self, game, x, y):
        super().__init__(game, utils.Resources.items["life_upgrade"], x, y)

    def use(self, target):
        if self.rect.colliderect(target.rect):
            target.max_hp += 1
            super().use(target)

    def load(self):
        self.image = utils.Resources.items["life_upgrade"]
        super().load()

class DamageUpgrade(Item):
    def __init__(self, game, x, y):
        super().__init__(game, utils.Resources.items["attack_damage_upgrade"], x, y)

    def use(self, target):
        if self.rect.colliderect(target.rect):
            target.strength += 0.5
            super().use(target)

    def load(self):
        self.image = utils.Resources.items["attack_damage_upgrade"]
        super().load()


class AttackSpeedUpgrade(Item):
    def __init__(self, game, x, y):
        super().__init__(game, utils.Resources.items["attack_speed_upgrade"], x, y)

    def use(self, target):
        if self.rect.colliderect(target.rect):
            if target.attack_speed > 0.1:
                target.attack_speed -= 0.1 * math.log(target.attack_speed + 1)
            else:
                target.attack_speed = 0.1
            super().use(target)

    def load(self):
        self.image = utils.Resources.items["attack_speed_upgrade"]
        super().load()


class Buyable(Item):

    def __init__(self, game, image, x, y, price):
        super().__init__(game, image, x, y)
        self.price = price

    def use(self, target):
        if self.game.player.coins >= self.price:
            self.game.player.coins -= self.price
            super().use(target)
            return True
        return False


class LifeUpgradeShop(Buyable):
    def __init__(self, game, x, y):
        super().__init__(game, utils.Resources.items["life_upgrade"], x, y, 75)

    def use(self, target):

        if self.rect.colliderect(target.rect) and super().use(target):
            target.max_hp += 1

    def load(self):
        self.image = utils.Resources.items["life_upgrade"]
        super().load()

class DamageUpgradeShop(Buyable):
    def __init__(self, game, x, y):
        super().__init__(game, utils.Resources.items["attack_damage_upgrade"], x, y, 75)

    def use(self, target):

        if self.rect.colliderect(target.rect) and super().use(target):
            target.strength += 0.5

    def load(self):
        self.image = utils.Resources.items["attack_damage_upgrade"]
        super().load()


class AttackSpeedUpgradeShop(Buyable):
    def __init__(self, game, x, y):
        super().__init__(game, utils.Resources.items["attack_speed_upgrade"], x, y, 75)

    def use(self, target):

        if self.rect.colliderect(target.rect) and super().use(target):
            if target.attack_speed > 0.1:
                target.attack_speed -= 0.1 * math.log(target.attack_speed + 1)
            else:
                target.attack_speed = 0.1

    def load(self):
        self.image = utils.Resources.items["attack_speed_upgrade"]
        super().load()


class MaxHealShop(Buyable):
    def __init__(self, game, x, y):
        super().__init__(game, utils.Resources.items["max_heal_shop"], x, y, 25)

    def use(self, target):

        if self.rect.colliderect(target.rect) and super().use(target):
            target.hp = target.max_hp

    def load(self):
        self.image = utils.Resources.items["max_heal_shop"]
        super().load()