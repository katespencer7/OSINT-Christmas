# import os
import pygame
from pygame.sprite import Sprite
from pygame_textinput import TextInputVisualizer, TextInputManager

WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

class OSINTLevel:
    """
    Represents a single OSINT challenge.
    Holds image path + str answer array.
    """
    def __init__(self, city, level_id, points=None):
        if city not in ["portland", "eugene", "corvallis"]:
            raise ValueError("Invalid city name for OSINTLevel") # error checking
        else: self.city = city

        self.level_id = level_id
        self.image_path = f"osint_levels/{city}/{level_id}/{level_id}.jpg" # default image path
        self.answer = self.load_level_solution(city, level_id)
        self.points = points

    def load_level_solution(self, city_name, level_id):
        """
        Loads level solution from filesystem, returns anwser as [lat, lon] string array.
        """
        anwsers = open(f"osint_levels/{city_name}/{level_id}/{level_id}.txt", "r").readlines()
        lat, lon = anwsers[0].strip().split(",")
        return [lat, lon]


class LevelBox(Sprite):
    """
    Clickable level selector icon for city screens.
    """
    def __init__(self, position, level, unlocked=True):
        super().__init__()

        self.level = level
        self.unlocked = unlocked
        self.hovered = False

        self.image = pygame.image.load(f"assets/level_icons/level_{level}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (250, 250)) # scale icon
        self.rect = self.image.get_rect(topleft=position)

    def update(self, mouse_pos, mouse_up):
        if not self.unlocked: # if level is locked, do nothing
            return None

        if self.rect.collidepoint(mouse_pos) and mouse_up:
            return self.level
        else:
            return None


    def draw(self, surface):
        surface.blit(self.image, self.rect)


class OSINTBox(Sprite):
    def __init__(self, level: OSINTLevel):
        super().__init__()

        self.level = level
        self.visible = True
        self.completed = False

        self.rect = pygame.Rect(100, 80, 600, 440) # rectangle

        # Load challenge image
        self.image = pygame.image.load(level.image_path).convert()
        self.image = pygame.transform.scale(self.image, (400, 250))

        # Text input
        self.textinput = TextInputVisualizer()

    def update(self, events):
        """
        Handle keyboard input while OSINT box is open.
        """
        self.textinput.update(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return self.validate_coordinates()

                if event.key == pygame.K_ESCAPE:
                    self.visible = False

        return None

    def validate_coordinates(self):
        """
        Compare user input to solution.
        """
        # user_input = self.textinput.value
        # solution = self.level.answer

        # if user_input.replace(" ", "") == ",".join(solution):
        #     self.completed = True
        #     self.visible = False
        #     return True

        # return False
        pass

    def draw(self, surface):
        """
        Draw modal overlay + contents.
        """
        if not self.visible:
            return

        # Dark overlay
        overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Panel
        pygame.draw.rect(surface, (30, 30, 30), self.rect, border_radius=12)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 3, border_radius=12)

        # Image
        surface.blit(self.image, (200, 120))

        # Input
        surface.blit(self.textinput.surface, (250, 400))


    

def osint_level_screen(screen, player, level, click_sound):
    """
    Runs the OSINT challenge loop.
    Returns a GameState when finished.
    """
    pass


# class TextInput:
#     """
#     Handles typing coordinates.
#     """
#     def __init__(self, rect):
#         pass

#     def handle_event(self, event):
#         pass

#     def draw(self, surface):
#         pass

#     def get_value(self):
#         pass


def load_city_levels(city_name:str):
    """
    Reads osint_levels/<city_name>/ and returns a list of OSINTLevel objects.
    """
    if city_name not in ["portland", "eugene", "corvallis"]:
        raise ValueError("Invalid city name for OSINTLevel") # error checking
    
    OSINT_levels = []
    for i in range(1, 6):  # levels 1, 2, 3, 4, and 5
        level = OSINTLevel(city_name, i)
        OSINT_levels.append(level)

    return OSINT_levels

if __name__ == "__main__":
    # for testing
    print(load_city_levels("portland")[4].answer)
