import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, width, height, pos_x, pos_y, color, group, player_path):
        super().__init__(group)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = pygame.image.load(player_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.hp = 100
        self.state = "idle"

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






