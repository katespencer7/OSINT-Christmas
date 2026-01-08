import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
import sys
from enum import Enum

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BEGIN GAME")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.mixer.music.load('assets/sounds/soulomon-b-the-yume-collective-midnight-miracles-436039.mp3')
pygame.mixer.music.play(-1) # play indefinetly
click_sound = pygame.mixer.Sound("assets/sounds/90s-game-ui-6-185099.wav")

def create_surface_with_text(text, font_size, text_rgb, bg_rgb=None):
    # Resize font if needed
    font = pygame.font.Font('assets/ByteBounce.ttf', int(font_size))
    surface = font.render(text, True, text_rgb, bg_rgb)  # antialias=True
    return surface.convert_alpha()

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

    def update(self, mouse_pos, mouse_up):
        """ Updates the element's appearance depending on the mouse position
            and returns the button's action if clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                click_sound.play()
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

def title_screen(screen):
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

    buttons = [begin_element, character_element, quit_element]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # for window closing
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLACK)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()


def play_level(screen):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="<--- Return to start",
        action=GameState.TITLE,
    )

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # for window closing
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLACK)

        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(screen)

        pygame.display.flip()