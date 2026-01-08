from game import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    game_state = GameState.TITLE
    running = True

    while running:
        for event in pygame.event.get(): # for window closing
            if event.type == pygame.QUIT:
                running = False

        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        elif game_state == GameState.NEWGAME:
            game_state = play_level(screen)

        elif game_state == GameState.CHARACTER:
            game_state = play_level(screen)

        elif game_state == GameState.QUIT:
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()