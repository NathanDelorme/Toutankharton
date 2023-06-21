import sys
import os
import pygame
from toutankharton.utils import Vector2
from toutankharton.game import Game

class Menu:
    def __init__(self):
        self.screen_size = Vector2(360, 340)
        self.screen = pygame.display.set_mode((self.screen_size.x, self.screen_size.y))
        self.buttons = []
        self.buttons.append(Button("Nouvelle partie", Vector2(10, 10), Vector2(340, 100), (255, 255, 255)))
        if not os.path.isfile("resources/save/savegame.dat"):
            self.buttons.append(Button("Continuer", Vector2(10, 120), Vector2(340, 100), (150, 150, 150)))
        else :
            self.buttons.append(Button("Continuer", Vector2(10, 120), Vector2(340, 100), (255, 255, 255)))
        self.buttons.append(Button("Quitter", Vector2(10, 230), Vector2(340, 100), (255, 255, 255)))

    def start(self):
        while True:
            pygame.display.flip()
            self.screen.fill("black")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    button_text = self.event_handler(mouse_pos)
                    if button_text == "Nouvelle partie":
                        return Game()
                    elif button_text == "Continuer" and os.path.isfile("savegame.dat"):
                        return Game.load_state()
                    elif button_text == "Quitter":
                        pygame.quit()
                        sys.exit()

            self.draw()

    def draw(self):
        for button in self.buttons:
            button.draw(self.screen)

    def event_handler(self, mouse_pos):
        for button in self.buttons:
            if button.event_handler(mouse_pos):
                return button.text


class Button:
    def __init__(self, text, position, size, color, font_size=30):
        self.text = text
        self.position = position
        self.size = size
        self.color = color
        self.font_size = font_size

        self.font = pygame.font.SysFont("Arial", self.font_size)
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))
        self.rect = pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, (self.position.x + self.size.x / 2 - self.text_surface.get_width() / 2,
                                        self.position.y + self.size.y / 2 - self.text_surface.get_height() / 2))

    def event_handler(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
