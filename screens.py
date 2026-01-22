from game import *
from challenges import TextInput

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


def play_level(screen, player, sound=None):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="<--- Return to start",
        action=GameState.TITLE,
    )

    portland_btn = Button(300, 100, 'assets/buttons/portland_button.png', 2, action=GameState.PORTLAND)
    eugene_btn = Button(300, 250, 'assets/buttons/eugene_button.png', 2, action=GameState.EUGENE)
    corvallis_btn = Button(300, 400, 'assets/buttons/corvallis_button.png', 2, action=GameState.CORVALLIS)

    buttons = RenderUpdates(return_btn, portland_btn, eugene_btn, corvallis_btn)
    return game_loop(screen, buttons, sound, draw_extra=lambda s: coin_banner(s, player))


def portland_screen(screen, player, sound=None):
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

    level_display(sound, level_boxes, levels, player, "portland")

    buttons = RenderUpdates(return_btn)
    return game_loop(screen, buttons, sound, background_image, city="portland", level_boxes=level_boxes, levels=levels, draw_extra=lambda s: coin_banner(s, player), player=player)


def eugene_screen(screen, player, sound=None):
    coin_banner(screen, player)
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

    level_display(sound, level_boxes, levels, player, "eugene")

    buttons = RenderUpdates(return_btn)
    return game_loop(screen, buttons, sound, background_image, city="eugene" , level_boxes=level_boxes, levels=levels, draw_extra=lambda s: coin_banner(s, player), player=player)


def corvallis_screen(screen, player, sound=None):
    coin_banner(screen, player)
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

    level_display(sound, level_boxes, levels, player, "corvallis")

    buttons = RenderUpdates(return_btn)
    return game_loop(screen, buttons, sound, background_image, city="corvallis", level_boxes=level_boxes, levels=levels, draw_extra=lambda s: coin_banner(s, player), player=player)


def level_display(sound, level_boxes, levels, player, city):
    ''' Helper function for level screens, displays level boxes in grid '''
    ICON_SIZE = 160
    GAP_X = 40
    GAP_Y = 40
    START_X = 120
    START_Y = 100

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


def coin_banner(screen, player):
    ''' Displays coin banner at top of screen '''
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, 47)) # banner
    coin_img = pygame.image.load('assets/coin.png').convert_alpha()
    coin_img = pygame.transform.smoothscale(coin_img, (30, 30))
    screen.blit(coin_img, (WIDTH - 50, 9))
    
    font = pygame.font.Font("assets/ByteBounce.ttf", 24)
    coin_text = font.render(f"Coins: {player.points}", True, (255, 255, 255))
    player_text = font.render(f"Player: {player.name}", True, (255, 255, 255))
    screen.blit(player_text, (20, 15))
    screen.blit(coin_text, (WIDTH - 180, 15))


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


# def name_entry_screen(screen, player, sound=None):
#     """
#     Screen for entering the player's name.
#     Returns GameState.NEWGAME when done.
#     """
#     clock = pygame.time.Clock()

#     title_font = pygame.font.Font("assets/ByteBounce.ttf", 48)
#     text_font = pygame.font.Font("assets/ByteBounce.ttf", 22)

#     input_box = TextInput(pygame.Rect(250, 280, 300, 45))

#     confirm_button = Button(
#         350, 350,
#         "assets/buttons/enter_button.png",
#         scale=1,
#         action="CONFIRM"
#     )

#     buttons = RenderUpdates(confirm_button)

#     while True:
#         events = pygame.event.get()
#         mouse_up = False

#         for event in events:
#             if event.type == pygame.QUIT:
#                 return GameState.QUIT
#             if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
#                 mouse_up = True
#             if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
#                 if input_box.text.strip():
#                     player.name = input_box.text.strip()
#                     player.save_game()
#                     return GameState.NEWGAME

#         input_box.update(events)

#         mouse_pos = pygame.mouse.get_pos()
#         for button in buttons:
#             action = button.update(mouse_pos, mouse_up, sound)
#             if action == "CONFIRM" and input_box.text.strip():
#                 player.name = input_box.text.strip()
#                 player.save_game()
#                 return GameState.NEWGAME

#         # ---- DRAW ----
#         screen.fill((0, 0, 0))

#         title = title_font.render("ENTER YOUR NAME", True, (255, 255, 255))
#         subtitle = text_font.render("This will be saved to your profile", True, (180, 180, 180))

#         screen.blit(title, title.get_rect(center=(WIDTH // 2, 180)))
#         screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 225)))

#         input_box.draw(screen)

#         for button in buttons:
#             button.draw(screen)

#         pygame.display.flip()
#         clock.tick(60)
