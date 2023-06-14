import pygame
from Entity import Entity


class Monster(Entity):
    def __init__(self, x, y, group, img_path, width, height, hp, speed, atk_speed, attack_damage, is_mele):
        super(Monster, self).__init__(x, y, group, img_path, width, height)
        self.hp = hp
        self.speed = speed
        self.atkSpeed = atk_speed
        self.attack_damage = attack_damage
        self.is_mele = is_mele

    def update(self, player):
        if player.x > self.x+35:
            self.x += self.speed
        elif player.x < self.x-35:
            self.x -= self.speed
        if player.y > self.y+35:
            self.y += self.speed
        elif player.y < self.y-35:
            self.y -= self.speed
        super(Monster, self).update()

    def attack(self, player):
        if pygame.Rect.colliderect(player.rect, self.rect) and self.is_mele and player.cooldown == 0:
            player.hp -= self.attack_damage
            player.cooldown = 45


class Slime(Monster):
    def __init__(self, x, y, group, mul):
        super(Slime, self).__init__(x, y, group, "../assets/images/king_slime.png", 50, 50, 20*mul, 1, 1, 5*mul, True)
