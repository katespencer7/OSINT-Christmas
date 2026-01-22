import pygame
from pygame.sprite import Sprite, RenderUpdates
import json, os
from enum import Enum

from challenges import load_city_levels, osint_level_page

# global variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 800, 600

# animation variables
center_x = WIDTH // 2
center_y = HEIGHT // 2
max_radius = max(WIDTH, HEIGHT) // 2 + 50
animation_speed = 5


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
                if sound:
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
    # CHARACTER = 2
    OSINT = 4
    
    PORTLAND = 10
    CORVALLIS = 11
    EUGENE = 12

    DOWNLOAD = 20
    CHECK = 21


class Player:
    """ Stores information about a player: points and name (under save_data.json)."""

    def __init__(self, save_file):
        self.points = save_file["points"]
        self.name = save_file["name"]

    def save_game(player): # FIXME
        try:
            with open("save_data.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            exit(-1)

        data["save_file"]["points"] = player.points
        data["save_file"]["name"] = player.name

        with open("save_data.json", "w") as f: # write back to file
            json.dump(data, f, indent=4)

    def update_levels(player, level:int, city:str):
        """ Marks a level as completed under player save file. """
        try:
            with open("save_data.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            exit(-1)

        level_key = str(level)  # ensure level is string for JSON keys

        data["save_file"]["levels"][city][level_key] = "completed"

        with open("save_data.json", "w") as f: # write back to file
            json.dump(data, f, indent=4)

    def check_levels(player, level:int, city:str) -> bool:
        """ Checks if a level has been completed under player save file. """
        try:
            with open("save_data.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            exit() # crash the game if save file can't be created

        level_key = str(level)  # ensure level is string for JSON keys

        return data["save_file"]["levels"][city].get(level_key) == "completed"


# class Character: # TODO
#     """ Character selection functions """
#     def __init__(self):
#         return


class Button(Sprite):
    """
    Button class for UI elements. From https://github.com/russs123/pygame_tutorials/blob/main/Button/button.py
    """
    def __init__(self, x, y, image_path, scale=None, size=None, action=None, unlocked=True):
        super().__init__()
        image = pygame.image.load(image_path).convert_alpha()
        
        if size is not None:
            scaled_image = pygame.transform.scale(image, (int(size[0]), int(size[1])))
            hover_size = (int(size[0] * 1.1), int(size[1] * 1.1))
            scaled_image_hover = pygame.transform.scale(image, hover_size)
        elif scale is not None:
            width = image.get_width()
            height = image.get_height()
            scaled_image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            scaled_image_hover = pygame.transform.scale(image, (int(width * scale * 1.1), int(height * scale * 1.1)))
        
        # Store images and rects as lists for hover effect
        self.images = [scaled_image, scaled_image_hover]
        rect_default = scaled_image.get_rect(topleft=(x, y))
        rect_hover = scaled_image_hover.get_rect(center=rect_default.center)
        self.rects = [rect_default, rect_hover]

        self.action = action
        self.clicked = False
        self.mouse_over = False
        self.unlocked = unlocked

    # properties that vary the image and its rect when the mouse is over the element
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up, sound):
        """ Updates appearance and returns `self.action` on click.
        If the button is locked (`unlocked=False`) this is a no-op.
        """
        if not self.unlocked:
            self.mouse_over = False
            return None

        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                if sound:
                    sound.play()
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos() # get mouse position

        if self.rect.collidepoint(pos):        #check mouseover and clicked conditions
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y)) # draw button on screen
        return action


def play_circle_animation(screen, state:GameState):
    """Plays the expanding circle animation."""
    clock = pygame.time.Clock()
    global current_radius
    current_radius = 0
    if state == GameState.PORTLAND:
        background = pygame.image.load(os.path.join('assets/background_images/portland_pixel.png')).convert()
    elif state == GameState.CORVALLIS:
        background = pygame.image.load(os.path.join('assets/background_images/corvallis_pixel.png')).convert()
    elif state == GameState.EUGENE:
        background = pygame.image.load(os.path.join('assets/background_images/eugene_pixel.png')).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))     # Scale the image to fit the window size

    
    while current_radius < max_radius:
        screen.fill(BLACK)

        # clip screen to circle
        clip_rect = pygame.Rect(
            center_x - current_radius,
            center_y - current_radius,
            current_radius * 2,
            current_radius * 2
        )

        screen.set_clip(clip_rect)
        screen.blit(background, (0, 0))
        screen.set_clip(None)
        pygame.display.flip()

        current_radius += 10   # speed control (bigger = faster)
        clock.tick(80)


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


def game_loop(screen, buttons, sound=None, background=None, city=None, level_boxes=None, levels=None, draw_extra=None, player=None):
    active_osint = None
    clock = pygame.time.Clock()

    while True:
        mouse_up = False
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        mouse_pos = pygame.mouse.get_pos()

        if active_osint:
            result = active_osint.update(events) #FIXME solution management

            if background:
                screen.blit(background, (0, 0))
            else:
                screen.fill(BLACK)

            active_osint.draw(screen)
            pygame.display.flip()
            clock.tick(60)

            if result is True:
                print("Correct!")
                active_osint = None

            elif result is False:
                print("Incorrect!")

            continue

        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)

        if draw_extra:
            draw_extra(screen)

        if level_boxes and levels:
            for box in level_boxes:
                clicked_level_id = box.update(mouse_pos, mouse_up, sound)
                box.draw(screen)

                if clicked_level_id:
                    level = levels[clicked_level_id - 1]
                    result = osint_level_page(screen, level, sound, city, player)
                    # Handle the result from osint_level_page
                    if result == "TITLE":
                        return GameState.TITLE
                    # Add more result handling as needed

        for button in buttons:
            action = button.update(mouse_pos, mouse_up, sound)
            if action is not None:
                if action in (GameState.PORTLAND, GameState.CORVALLIS, GameState.EUGENE):
                    play_circle_animation(screen, action)
                return action

        buttons.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

