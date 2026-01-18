import pygame
from pygame.sprite import Sprite

WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

points = {1:1000, 2:1500, 3:2000, 4:3000, 5:4000}

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
    def __init__(self, position, level, unlocked=True, sound=None):
        super().__init__()

        self.level = level
        self.unlocked = unlocked
        self.sound = sound
        
        image = pygame.image.load(f"assets/level_icons/level_{level}.png").convert_alpha()
        scaled_image = pygame.transform.scale(image, (150, 150))
        scaled_image_hover = pygame.transform.scale(image, (int(150 * 1.1), int(150 * 1.1)))
        
        self.images = [scaled_image, scaled_image_hover]
        rect_default = scaled_image.get_rect(topleft=position)
        rect_hover = scaled_image_hover.get_rect(center=rect_default.center)
        self.rects = [rect_default, rect_hover]
        
        self.mouse_over = False

    # properties that vary the image and its rect when the mouse is over the element
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up, sound=None):
        if not self.unlocked:  # if level is locked, do nothing
            return None

        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                if sound:
                    sound.play()
                return self.level
        else:
            self.mouse_over = False
        
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
    def __init__(self, level: OSINTLevel, return_state):
        super().__init__()

        self.level = level
        self.return_state = return_state
        self.visible = True
        self.completed = False

        # ---------- Layout ----------
        self.panel_rect = pygame.Rect(60, 60, 680, 480)

        self.image_rect = pygame.Rect(90, 110, 400, 280)
        self.sidebar_rect = pygame.Rect(520, 110, 200, 360)

        # ---------- Image ----------
        self.image = pygame.image.load(level.image_path).convert()
        self.image = pygame.transform.scale(self.image, self.image_rect.size)

        # ---------- Fonts ----------
        self.title_font = pygame.font.Font("assets/ByteBounce.ttf", 28)
        self.text_font = pygame.font.Font("assets/ByteBounce.ttf", 18)

        # ---------- Text Input ----------
        self.textinput = TextInput(
            pygame.Rect(
                self.sidebar_rect.left + 10,
                self.sidebar_rect.top + 120,
                self.sidebar_rect.width - 20,
                40
            )
        )

        # ---------- Buttons ----------
        from game import Button, UIElement, GameState
        self.return_btn = UIElement(
            center_position=(140, 570),
            font_size=20,
            bg_rgb=BLACK,
            text_rgb=WHITE,
            text="<--- Return to levels",
            action=self.return_state,
        )
        
        self.enter_button = Button(
            self.sidebar_rect.left + 40,
            self.sidebar_rect.top + 180,
            "assets/buttons/enter_button.png",
            1.0
        )

        self.back_rect = pygame.Rect(90, 80, 220, 24)


    def update(self, events):
        if not self.visible:
            return None

        # Update text input
        self.textinput.update(events)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                # Submit with ENTER key
                if event.key == pygame.K_RETURN:
                    if self.textinput.value:
                        user_input = self.textinput.value
                        return self.check_answer(user_input)
                    else: continue

                # Escape = return to levels
                if event.key == pygame.K_ESCAPE:
                    self.visible = False
                    return self.return_state

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                # Submit button clicked
                if self.enter_button.rect.collidepoint(mouse_pos):
                    user_input = self.textinput.value
                    return self.check_answer(user_input)

                # Return button clicked
                if self.return_btn.rect.collidepoint(mouse_pos):
                    self.visible = False
                    return self.return_state

        return None


    def validate_coordinates(self):
        user = self.textinput.text.replace(" ", "")
        solution = ",".join(self.level.answer)

        if user == solution:
            self.completed = True
            self.visible = False
            return True

        return False


    def draw(self, surface):
        if not self.visible:
            return

        # Full black background (Figma-style)
        surface.fill((0, 0, 0))

        # Level image
        surface.blit(self.image, self.image_rect.topleft)

        # Sidebar (keep or remove depending on mockup)
        pygame.draw.rect(
            surface,
            (40, 40, 40),
            self.sidebar_rect,
            border_radius=8
        )

        # Level title
        title = self.title_font.render(
            f"Level {self.level.level_id}",
            True,
            (255, 255, 255)
        )
        surface.blit(
            title,
            (self.sidebar_rect.left + 12, self.sidebar_rect.top + 20)
        )

        # Instructions
        instructions = self.text_font.render(
            "Enter solution in form 0.000,0.000",
            True,
            (200, 200, 200)
        )
        surface.blit(
            instructions,
            (self.sidebar_rect.left + 12, self.sidebar_rect.top + 70)
        )

        # Input box
        self.textinput.draw(surface)

        # Submit button
        self.enter_button.draw(surface)

        # Return button
        self.return_btn.draw(surface)




    

# def osint_level_screen(screen, player, level, click_sound):
#     """
#     Runs the OSINT challenge loop.
#     Returns a GameState when finished.
#     """
#     pass


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
