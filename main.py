import sys, os
import pygame

import gui
from game import Game
import utils


def launch_game():
    pygame.init()

    score_file = open("save/score.dat", "rb")
    Game.best_score = int(score_file.read())

    utils.Resources.load()
    selected_option = gui.launch_main_menu()
    game = None
    if selected_option == utils.MenuOption.NEW_GAME:
        game = Game()
    elif selected_option == utils.MenuOption.CONTINUE:
        game = Game.load_game()
    elif selected_option == utils.MenuOption.QUIT:
        pygame.quit()
        sys.exit()
    pygame.mouse.set_visible(False)
    crosshair = gui.Crosshair()
    accumulator = 0
    tilemap = game.start_dungeon()

    game.running = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                game.save_game()

            elif game.running and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.running = False
                    pygame.quit()
                    game.save_game()
                    sys.exit()

        if game.running:
            game.screen.fill("black")
            tilemap.draw()
            previous_pos = game.player.rect.topleft

            accumulator += game.clock.tick() / 1000
            while accumulator >= game.delta_time:
                game.handle_events()
                accumulator -= game.delta_time

            for wall in game.walls_rect:
                if game.player.rect.colliderect(wall):
                    game.player.rect.topleft = previous_pos
            i = 0
            for enemy in game.current_room.enemies:
                i += 1
                has_collided = False
                for wall in game.walls_rect:
                    if enemy.rect.colliderect(wall) and not has_collided and enemy.stats["speed"] == enemy.speed:
                        has_collided = True
                        enemy.speed /= 2
                if not has_collided and enemy.stats["speed"] != enemy.speed:
                    enemy.speed = enemy.stats["speed"]

            for door in game.doors_rect:
                if game.player.rect.colliderect(door[0]):
                    if door[1].x == game.current_room.size.x // 2 and door[1].y == 0:
                        game.player.rect.topleft = ((game.screen.get_width() - game.player.image.get_width()) // 2, tilemap.center_adjust.y + (game.current_room.size.y-2) * 16 * utils.DisplayerCalculator.factor)
                        game.current_room = game.dungeon.get_cell(utils.Vector2(game.current_room.pos.x, game.current_room.pos.y - 1))
                    elif door[1].x == game.current_room.size.x // 2 and door[1].y == game.current_room.size.y - 1:
                        game.player.rect.topleft = ((game.screen.get_width() - game.player.image.get_width()) // 2, tilemap.center_adjust.y + 1 * 16 * utils.DisplayerCalculator.factor)
                        game.current_room = game.dungeon.get_cell(utils.Vector2(game.current_room.pos.x, game.current_room.pos.y + 1))
                    elif door[1].x == 0 and door[1].y == game.current_room.size.y // 2:
                        game.player.rect.topleft = (tilemap.center_adjust.x + (game.current_room.size.x-2) * 16 * utils.DisplayerCalculator.factor, (game.screen.get_height() - game.player.image.get_height()) // 2)
                        game.current_room = game.dungeon.get_cell(utils.Vector2(game.current_room.pos.x - 1, game.current_room.pos.y))
                    elif door[1].x == game.current_room.size.x - 1 and door[1].y == game.current_room.size.y // 2:
                        game.player.rect.topleft = (tilemap.center_adjust.x + 1 * 16 * utils.DisplayerCalculator.factor, (game.screen.get_height() - game.player.image.get_height()) // 2)
                        game.current_room = game.dungeon.get_cell(utils.Vector2(game.current_room.pos.x + 1, game.current_room.pos.y))
                    else:
                        game.level += 1
                        if Game.best_score < game.level:
                            Game.best_score = game.level - 1
                        game.player.rect.center = game.screen.get_rect().center
                        game.generate_dungeon(game)
                    tilemap = game.start_dungeon()
            game.draw()

            if game.player.hp <= 0:
                if os.path.exists("save/savegame.dat"):
                    os.remove("save/savegame.dat")
                return

        crosshair.update()

        gui.display_hud(game)
        crosshair.draw(game.screen)
        pygame.display.flip()
        pygame.display.update()


if __name__ == "__main__":
    while True:
        launch_game()
