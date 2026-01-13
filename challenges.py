import pygame
from pygame.sprite import Sprite

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


class TextInput:
    """
    Text input box for entering coordinates on OSINT game screen.
    """
    def __init__(self, rect, font_size=24, text_color=BLACK, bg_color=WHITE, border_color=BLACK):
        self.rect = rect
        self.font = pygame.font.Font('assets/ByteBounce.ttf', font_size)
        self.text = ""
        self.active = False
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.cursor_visible = True
        self.cursor_timer = 0

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN: # enter key
                    pass
                else:
                    self.text += event.unicode

        self.cursor_timer += 1
        if self.cursor_timer >= 5:  # blink every 5 frames
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect) # render background
        text_surf = self.font.render(self.text, True, self.text_color) # render text
        text_rect = text_surf.get_rect(midleft=(self.rect.left + 10, self.rect.centery))
        surface.blit(text_surf, text_rect)

        if self.active and self.cursor_visible: # cursor
            cursor_x = text_rect.right + 2
            cursor_y = self.rect.centery - self.font.get_height() // 2
            pygame.draw.line(surface, self.text_color, (cursor_x, cursor_y), (cursor_x, cursor_y + self.font.get_height()), 2)


class OSINTBox(Sprite):
    """
    Box overlay for OSINT challenges, activates when a level is clicked
    """
    def __init__(self, level: OSINTLevel):
        super().__init__()

        self.level = level
        self.visible = True
        self.completed = False

        self.rect = pygame.Rect(100, 80, 600, 440) # rectangle background

        self.image = pygame.image.load(level.image_path).convert() 
        self.image = pygame.transform.scale(self.image, (400, 250))
        
        self.textinput = TextInput(pygame.Rect(250, 400, 300, 40))

        # Enter button
        from game import Button
        self.enter_button = Button(555, 400, "assets/enter_button.png", 1.0)
        self.enter_button.rect.centery = 420  # Align vertically with text input center
        self.enter_action = False

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

        # Handle enter button
        if self.enter_action:
            self.enter_action = False
            return self.validate_coordinates()

        return None

    def validate_coordinates(self):
        """
        Compare user input to solution.
        """
        # user_input = self.textinput.text
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

        # overlay of background image ---- # FIXME
        overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, (30, 30, 30), self.rect, border_radius=12) # panel background
        # pygame.draw.rect(surface, (255, 255, 255), self.rect, 3, border_radius=12) # panel border

        surface.blit(self.image, (200, 120)) # challenge image
        self.textinput.draw(surface) # text input box

        # Draw enter button
        action = self.enter_button.draw(surface)
        if action:
            self.enter_action = True


    

def osint_level_screen(screen, player, level, click_sound):
    """
    Runs the OSINT challenge loop.
    Returns a GameState when finished.
    """
    pass


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

# if __name__ == "__main__":
#     # for testing
#     print(load_city_levels("portland")[4].answer)
