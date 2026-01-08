from game import *

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    # create a ui element
    begin_element = UIElement(
        center_position=(300, 475),
        font_size=30,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="Begin",
        action="BEGIN",
    )

    quit_element = UIElement(
        center_position=(500, 475),
        font_size=30,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

    character_element = UIElement(
        center_position=(400, 175),
        font_size=30,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="Character Selection",
        action="CHARACTER",
    )

    buttons = [begin_element, character_element, quit_element]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        mouse_pos = pygame.mouse.get_pos()
        mouse_up = pygame.mouse.get_pressed()[0]

        for btn in buttons:
            action = btn.update(mouse_pos, mouse_up)
            btn.draw(screen)
            if action == GameState.QUIT:
                running = False
            elif action == "BEGIN":
                click_sound.play()
            elif action == "CHARACTER":
                click_sound.play()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# call main when the script is run
if __name__ == "__main__":
    main()