import os
import sys

import pygame
import pygame_gui
import utils


class Crosshair(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = utils.Resources.gui["crosshair"]
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * utils.DisplayerCalculator.factor//2,
                                             self.image.get_height() * utils.DisplayerCalculator.factor//2))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.topleft = pygame.mouse.get_pos()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def display_hud(game):
    heart_image = utils.Resources.gui["filled_heart_frame"]
    heart_image = pygame.transform.scale(heart_image,
                                         (heart_image.get_width() * utils.DisplayerCalculator.factor,
                                          heart_image.get_height() * utils.DisplayerCalculator.factor))
    empty_heart_image = utils.Resources.gui["empty_heart_frame"]
    empty_heart_image = pygame.transform.scale(empty_heart_image,
                                               (empty_heart_image.get_width() * utils.DisplayerCalculator.factor,
                                                empty_heart_image.get_height() * utils.DisplayerCalculator.factor))
    for i in range(game.player.max_hp):
        if i < game.player.hp:
            game.screen.blit(heart_image, (game.screen.get_width() - heart_image.get_width() * (i + 1) - 5 * (i + 1), 5))
        else:
            game.screen.blit(empty_heart_image, (game.screen.get_width() - heart_image.get_width() * (i + 1) - 5 * i, 5))

    coin_image = utils.Resources.gui["coin"]
    coin_image = pygame.transform.scale(coin_image,
                                        (coin_image.get_width() * utils.DisplayerCalculator.factor,
                                         coin_image.get_height() * utils.DisplayerCalculator.factor))
    game.screen.blit(coin_image, (game.screen.get_width() - coin_image.get_width() - 5, 5 + heart_image.get_height() + 5))
    coin_text = utils.Resources.fonts["default"].render(str(game.player.coins), True, (255, 255, 255))
    coin_text = pygame.transform.scale(coin_text,
                                        (coin_text.get_width() * utils.DisplayerCalculator.factor,
                                            coin_text.get_height() * utils.DisplayerCalculator.factor))
    game.screen.blit(coin_text, (game.screen.get_width() - coin_text.get_width() - 5 - coin_image.get_width() - 5, 5 + heart_image.get_height()))

    attack_damage_image = utils.Resources.gui["attack_damage"]
    attack_damage_image = pygame.transform.scale(attack_damage_image,
                                                 (attack_damage_image.get_width() * utils.DisplayerCalculator.factor,
                                                  attack_damage_image.get_height() * utils.DisplayerCalculator.factor))
    game.screen.blit(attack_damage_image, (game.screen.get_width() - attack_damage_image.get_width() - 5, 5 + heart_image.get_height() + 5 + coin_image.get_height() + 5))
    attack_damage_text = utils.Resources.fonts["default"].render(str(game.player.strength), True, (255, 255, 255))
    attack_damage_text = pygame.transform.scale(attack_damage_text,
                                                    (attack_damage_text.get_width() * utils.DisplayerCalculator.factor,
                                                        attack_damage_text.get_height() * utils.DisplayerCalculator.factor))
    game.screen.blit(attack_damage_text, (game.screen.get_width() - attack_damage_text.get_width() - 5 - attack_damage_image.get_width() - 5, 5 + heart_image.get_height() + 5 + coin_image.get_height()))

    attack_speed_image = utils.Resources.gui["attack_speed"]
    attack_speed_image = pygame.transform.scale(attack_speed_image,
                                                (attack_speed_image.get_width() * utils.DisplayerCalculator.factor,
                                                    attack_speed_image.get_height() * utils.DisplayerCalculator.factor))
    game.screen.blit(attack_speed_image, (game.screen.get_width() - attack_speed_image.get_width() - 5, 5 + heart_image.get_height() + 5 + coin_image.get_height() + 5 + attack_damage_image.get_height() + 5))
    attack_speed_text = utils.Resources.fonts["default"].render(format(game.player.attack_speed, '.2f') + "/s", True, (255, 255, 255))
    attack_speed_text = pygame.transform.scale(attack_speed_text,
                                                    (attack_speed_text.get_width() * utils.DisplayerCalculator.factor,
                                                        attack_speed_text.get_height() * utils.DisplayerCalculator.factor))
    game.screen.blit(attack_speed_text, (game.screen.get_width() - attack_speed_text.get_width() - 5 - attack_speed_image.get_width() - 5, 5 + heart_image.get_height() + 5 + coin_image.get_height() + 5 + attack_damage_image.get_height()))

    quit_text = utils.Resources.fonts["default"].render("Escape pour sauvegarder et quitter", True, (255, 255, 255))
    quit_text = pygame.transform.scale(quit_text,
                                       (quit_text.get_width() * utils.DisplayerCalculator.factor//2,
                                        quit_text.get_height() * utils.DisplayerCalculator.factor//2))
    game.screen.blit(quit_text, (5, game.screen.get_height() - quit_text.get_height() - 5))

def launch_main_menu():
    #screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) TODO
    screen = pygame.display.set_mode((720, 480))
    ui_manager = pygame_gui.UIManager(screen.get_size())
    crosshair = Crosshair()

    title_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((screen.get_width() // 4, 0),
                                                                       (screen.get_width() // 2, screen.get_height() // 11)),
                                             text="Toutankharton",
                                             manager=ui_manager)
    best_score_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((screen.get_width() // 4, screen.get_height() // 11 * 1),
                                                                            (screen.get_width() // 2, screen.get_height() // 11)),
                                                  text="Meilleur score: ",
                                                  manager=ui_manager)
    new_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen.get_width() // 4, screen.get_height() // 11 * 3),
                                                                             (screen.get_width() // 2, screen.get_height() // 11)),
                                                   text="Nouvelle Partie",
                                                   manager=ui_manager)
    continue_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen.get_width() // 4, screen.get_height() // 11 * 5),
                                                                             (screen.get_width() // 2, screen.get_height() // 11)),
                                                   text="Continuer",
                                                   manager=ui_manager)
    if not os.path.exists("save/savegame.dat"):
        continue_button.disable()
    quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen.get_width() // 4, screen.get_height() // 11 * 7),
                                                                         (screen.get_width() // 2, screen.get_height() // 11)),
                                               text="Quitter",
                                               manager=ui_manager)
    version_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((screen.get_width() // 4, screen.get_height() // 11 * 10),
                                                                       (screen.get_width() // 2, screen.get_height() // 11)),
                                               text="Version " + utils.GameInfo.version,
                                               manager=ui_manager)

    clock = pygame.time.Clock()
    running = True

    while running:
        time_delta = clock.tick()/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            ui_manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == new_game_button:
                    return utils.MenuOption.NEW_GAME
                elif event.ui_element == continue_button:
                    return utils.MenuOption.CONTINUE
                elif event.ui_element == quit_button:
                    pygame.quit()
                    return utils.MenuOption.QUIT

        screen.fill((0, 0, 0))

        ui_manager.update(time_delta)
        crosshair.update()

        ui_manager.draw_ui(screen)
        crosshair.draw(screen)
        pygame.display.update()
