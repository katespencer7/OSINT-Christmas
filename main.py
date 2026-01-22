from screens import *
import pygame, sys, os

def resource_path(relative_path):
    """ Get absolute path to resource, works with PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main():
    WIDTH, HEIGHT = 800, 600
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.scrap.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Christmas OSINT Adventure")
    clock = pygame.time.Clock()
    game_state = GameState.TITLE

    # Load sounds
    pygame.mixer.music.load('assets/sounds/soulomon-b-the-yume-collective-midnight-miracles-436039.mp3')
    pygame.mixer.music.play(-1)  # play indefinitely
    click_sound = pygame.mixer.Sound("assets/sounds/90s-game-ui-6-185099.wav")
    points_sound = pygame.mixer.Sound("assets/sounds/get-coin-351945.wav")

    player = load_game()

    # if not player.name or player.name.strip() == "":
    #     game_state = GameState.NAME
    # else:
    #     game_state = GameState.TITLE

    running = True
    while running:
        events = pygame.event.get()
        for event in events: # closing window
            if event.type == pygame.QUIT:
                player.save_game()
                running = False

            if event.type == pygame.VIDEORESIZE: # resizing
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        if game_state == GameState.TITLE:
            game_state = title_screen(screen, click_sound)

        elif game_state == GameState.NEWGAME:
            game_state = play_level(screen, player, click_sound)

        elif game_state == GameState.PORTLAND:
            game_state = portland_screen(screen, player, click_sound)

        elif game_state == GameState.EUGENE:
            game_state = eugene_screen(screen, player, click_sound)

        elif game_state == GameState.CORVALLIS:
            game_state = corvallis_screen(screen, player, click_sound)

        elif game_state == GameState.QUIT:
            player.save_game()  # save the current game
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
