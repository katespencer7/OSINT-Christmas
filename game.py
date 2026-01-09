import pygame
import pygame.freetype
from pygame.sprite import Sprite, RenderUpdates
from pygame.rect import Rect
import sys, json, os
from enum import Enum

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 800, 600


def create_surface_with_text(text, font_size, text_rgb, bg_rgb=None):
    """ Returns surface with text written on """
    font = pygame.font.Font('assets/ByteBounce.ttf', int(font_size))
    surface = font.render(text, True, text_rgb, bg_rgb)  # antialias=True
    return surface.convert_alpha()

def load_game():
    ''' For loading game information from save_data.json. '''
    try:
        with open("save_data.json", "r") as f:
            data = json.load(f)
        return Player(**data)
    except FileNotFoundError:
        return Player()  # fresh save


class UIElement(Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
        """
        self.mouse_over = False  # indicates if the mouse is over the element

        # create the default image
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # create the image that shows when mouse is over the element
        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # add both images and their rects to lists
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        # calls the init method of the parent sprite class
        super().__init__()

    # properties that vary the image and its rect when the mouse is over the element
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up, sound):
        """ Updates the element's appearance depending on the mouse position
            and returns the button's action if clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                sound.play()
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    CHARACTER = 2
    NEXT_LEVEL = 3
    
    PORTLAND = 10
    CORVALLIS = 11
    EUGENE = 12


class Player:
    """ Stores information about a player """

    def __init__(self, score=0, current_level=1):
        self.score = score
        self.current_level = current_level

    def save_game(player):
        data = {
            "score": player.score,
            "current_level": player.current_level,
        }

        with open("save_data.json", "w") as f:
            json.dump(data, f, indent=4)


class Character: # TODO
    """ Character selection functions """
    def __init__(self):
        return


def title_screen(screen, sound=None):
    background_image = pygame.image.load(os.path.join('assets/background_images/background_pixel.png')).convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))     # Scale the image to fit the window size

    begin_element = UIElement(
        center_position=(300, 475),
        font_size=30,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="Begin",
        action=GameState.NEWGAME,
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
        action=GameState.CHARACTER,
    )

    buttons = RenderUpdates(begin_element, character_element, quit_element)
    return game_loop(screen, buttons, sound, background_image)

def portland_screen(screen, sound=None):
    background_image = pygame.image.load(os.path.join('assets/background_images/portland_pixel.png')).convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))     # Scale the image to fit the window size

    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="<--- Return to menu",
        action=GameState.NEWGAME,
    )

    buttons = RenderUpdates(return_btn)
    return game_loop(screen, buttons, sound, background_image, draw_box=True)

def eugene_screen(screen, sound=None):
    background_image = pygame.image.load(os.path.join('assets/background_images/eugene_pixel.png')).convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))     # Scale the image to fit the window size

    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="<--- Return to menu",
        action=GameState.NEWGAME,
    )

    buttons = RenderUpdates(return_btn)
    return game_loop(screen, buttons, sound, background_image)

def corvallis_screen(screen, sound=None):
    background_image = pygame.image.load(os.path.join('assets/background_images/corvallis_pixel.png')).convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))     # Scale the image to fit the window size

    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="<--- Return to menu",
        action=GameState.NEWGAME,
    )

    buttons = RenderUpdates(return_btn)
    return game_loop(screen, buttons, sound, background_image)

def character_screen(screen, player, sound=None):
    ''' Character selection page. Uses Character class for character values '''
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="<--- Return to start",
        action=GameState.TITLE,
    )

    buttons = RenderUpdates(return_btn)
    return game_loop(screen, buttons, sound)

def play_level(screen, player, sound=None):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="<--- Return to start",
        action=GameState.TITLE,
    )
    nextlevel_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text=f"Next level ({player.current_level + 1})",
        action=GameState.NEXT_LEVEL,
    )
    portland_btn = UIElement(
        center_position=(200, 100),
        font_size=30,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text=f"Portland",
        action=GameState.PORTLAND,
    )
    eugene_btn = UIElement(
        center_position=(400, 100),
        font_size=30,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text=f"Eugene",
        action=GameState.EUGENE,
    )
    corvallis_btn = UIElement(
        center_position=(600, 100),
        font_size=30,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text=f"Corvallis",
        action=GameState.CORVALLIS,
    )

    buttons = RenderUpdates(return_btn, nextlevel_btn, portland_btn, eugene_btn, corvallis_btn)
    return game_loop(screen, buttons, sound)

def game_loop(screen, buttons, sound=None, background=None, draw_box=False):
    """ Handles game loop until an action is return by a button in the
    buttons sprite renderer.
    """
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # for window closing
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)

        if draw_box:
            level_1 = pygame.Rect(50, 50, 100, 100)
            pygame.draw.rect(screen, BLACK, level_1)

            level_2 = pygame.Rect(200, 50, 100, 100)
            pygame.draw.rect(screen, BLACK, level_2)

            level_3 = pygame.Rect(350, 50, 100, 100)
            pygame.draw.rect(screen, BLACK, level_3)

            level_4 = pygame.Rect(500, 50, 100, 100)
            pygame.draw.rect(screen, BLACK, level_4)

            level_5 = pygame.Rect(650, 50, 100, 100)
            pygame.draw.rect(screen, BLACK, level_5)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up, sound)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)
        pygame.display.flip()

