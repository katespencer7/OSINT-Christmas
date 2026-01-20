from game import *

def title_screen(screen, sound=None):
    quit_button = Button(200, 400, 'assets/buttons/quit_button.png', 2, action=GameState.QUIT)
    begin_button = Button(450, 400, 'assets/buttons/begin_button.png', 2, action=GameState.NEWGAME)

    buttons = RenderUpdates(quit_button, begin_button)

    title_font = pygame.font.Font("assets/ByteBounce.ttf", 72)
    subtitle_font = pygame.font.Font("assets/ByteBounce.ttf", 28)

    def draw_title(screen):
        title = title_font.render("OSINT CHRISTMAS", True, (255, 255, 255))
        subtitle = subtitle_font.render("Open-Source Intelligence Challenge", True, (180, 180, 180))

        screen.blit(title, title.get_rect(center=(WIDTH // 2, 140)))
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 200)))

    return game_loop(screen, buttons, sound, draw_extra=draw_title)


def portland_screen(screen, sound=None):
    background_image = pygame.image.load(os.path.join('assets/background_images/portland_pixel.png')).convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=None,
        text_rgb=WHITE,
        text="<--- Return to menu",
        action=GameState.NEWGAME,
    )

    levels = load_city_levels("portland")
    level_boxes = RenderUpdates()

    level_display(sound, level_boxes, levels)

    buttons = RenderUpdates(return_btn)
    return game_loop(screen, buttons, sound, background_image, city="portland", level_boxes=level_boxes, levels=levels)


def eugene_screen(screen, sound=None):
    background_image = pygame.image.load(os.path.join('assets/background_images/eugene_pixel.png')).convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))     # Scale the image to fit the window size

    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=None,
        text_rgb=WHITE,
        text="<--- Return to menu",
        action=GameState.NEWGAME,
    )

    levels = load_city_levels("eugene")
    level_boxes = RenderUpdates()

    level_display(sound, level_boxes, levels)

    buttons = RenderUpdates(return_btn)
    return game_loop(screen, buttons, sound, background_image, city="eugene" , level_boxes=level_boxes, levels=levels)


def corvallis_screen(screen, sound=None):
    background_image = pygame.image.load(os.path.join('assets/background_images/corvallis_pixel.png')).convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))     # Scale the image to fit the window size

    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=None,
        text_rgb=WHITE,
        text="<--- Return to menu",
        action=GameState.NEWGAME,
    )

    levels = load_city_levels("corvallis")
    level_boxes = RenderUpdates()

    level_display(sound, level_boxes, levels)

    buttons = RenderUpdates(return_btn)
    return game_loop(screen, buttons, sound, background_image, city="corvallis", level_boxes=level_boxes, levels=levels)


def level_display(sound, level_boxes, levels):
    ''' Helper function for level screens, displays level boxes in grid '''
    ICON_SIZE = 160
    GAP_X = 40
    GAP_Y = 40
    START_X = 100
    START_Y = 60

    for i, level in enumerate(levels):
        if i < 3:
            col, row = i, 0
        else:
            col, row = i - 3, 1

        x = START_X + col * (ICON_SIZE + GAP_X)
        y = START_Y + row * (ICON_SIZE + GAP_Y)

        # Use Button for level icons so hover/click behavior is shared
        btn = Button(x, y, f"assets/level_icons/level_{level.level_id}.png", size=(ICON_SIZE, ICON_SIZE), action=level.level_id, unlocked=True,)
        level_boxes.add(btn)


# def character_screen(screen, sound=None):
#     ''' Character selection page. Uses Character class for character values '''
#     return_btn = UIElement(
#         center_position=(140, 570),
#         font_size=20,
#         bg_rgb=BLACK,
#         text_rgb=WHITE,
#         text="<--- Return to start",
#         action=GameState.TITLE,
#     )

#     buttons = RenderUpdates(return_btn)
#     return game_loop(screen, buttons, sound)