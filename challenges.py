import os
from pygame.sprite import Sprite

# -----------------------------
# Data containers (no behavior)
# -----------------------------

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


def validate_coordinates(user_input, level):
    """
    Compares user input to level.answer using level.tolerance.
    Returns True/False.
    """
    pass


# -----------------------------
# UI helper objects
# -----------------------------

class LevelBox(Sprite):
    """
    Clickable level selector box for city screens.
    """
    def __init__(self, rect, level, unlocked):
        pass

    def update(self, mouse_pos, mouse_up):
        """
        Returns ("OSINT", level) if clicked.
        """
        pass

    def draw(self, surface):
        pass


class TextInput:
    """
    Handles typing coordinates.
    """
    def __init__(self, rect):
        pass

    def handle_event(self, event):
        pass

    def draw(self, surface):
        pass

    def get_value(self):
        pass


# -----------------------------
# OSINT gameplay screen
# -----------------------------

def osint_level_screen(screen, player, level, click_sound):
    """
    Runs the OSINT challenge loop.
    Returns a GameState when finished.
    """
    pass

if __name__ == "__main__":
    # for testing
    print(load_city_levels("portland")[4].answer)
