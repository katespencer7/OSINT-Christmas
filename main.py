from screens import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Christmas OSINT Adventure")
    clock = pygame.time.Clock()
    game_state = GameState.TITLE
        
    pygame.mixer.music.load('assets/sounds/soulomon-b-the-yume-collective-midnight-miracles-436039.mp3')
    pygame.mixer.music.play(-1) # play indefinetly
    click_sound = pygame.mixer.Sound("assets/sounds/90s-game-ui-6-185099.wav")

    running = True
    while running:
        for event in pygame.event.get(): # for window closing
            if event.type == pygame.QUIT:
                running = False

        if game_state == GameState.TITLE:
            game_state = title_screen(screen, click_sound)

        if game_state == GameState.NEWGAME:
            player = load_game()
            game_state = play_level(screen, player, click_sound)

        # elif game_state == GameState.CHARACTER:
        #     game_state = character_screen(screen)

        elif game_state == GameState.PORTLAND: # Portland game screen
            game_state = portland_screen(screen, click_sound)

        elif game_state == GameState.EUGENE: # Eugene game screen
            game_state = eugene_screen(screen, click_sound)
        
        elif game_state == GameState.CORVALLIS: # Corvallis game screen
            game_state = corvallis_screen(screen, click_sound)

        elif game_state == GameState.QUIT:
            player.save_game() # save the current game
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()