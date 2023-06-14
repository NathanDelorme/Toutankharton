import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, width, height, x, y, color, group, player_path, player_hurt_path):
        super().__init__(group)
        self.x = x
        self.y = y
        self.image = pygame.image.load(player_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.hp = 100
        self.speed = 3
        self.state = "idle"
        self.cooldown = 0
        self.player_path = player_path
        self.player_hurt_path = player_hurt_path

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.y -= self.speed
        if keys[pygame.K_q]:
            self.x -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

    def update(self):
        if self.cooldown == 0:
            self.image = pygame.image.load(self.player_path)
        else:
            self.image = pygame.image.load(self.player_hurt_path)
            self.cooldown -= 1
        self.rect.topleft = (self.x, self.y)

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






