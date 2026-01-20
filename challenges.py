import pygame, shutil, os
from pygame.sprite import Sprite

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
GREEN = (0, 200, 0)

class OSINTLevel:
    """
    Represents a single OSINT challenge.
    Holds image path + str answer array.
    """
    def __init__(self, city, level_id):
        if city not in ["portland", "eugene", "corvallis"]:
            raise ValueError("Invalid city name")
        self.city = city
        self.level_id = level_id
        self.image_path = f"osint_levels/{city}/{level_id}/{level_id}.jpg"
        self.answer = self.load_solution(city, level_id)

    def load_solution(self, city, level_id):
        with open(f"osint_levels/{city}/{level_id}/{level_id}.txt", "r") as f:
            lat, lon = f.readline().strip().split(",")
        return [lat, lon]


class TextInput:
    """
    Simple text input box.
    """
    def __init__(self, rect, font_size=24):
        self.rect = rect
        self.font = pygame.font.Font('assets/ByteBounce.ttf', font_size)
        self.text = ""
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = self.rect.collidepoint(event.pos)
            
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    pass
                else:
                    self.text += event.unicode
        
        self.cursor_timer += 1
        
        if self.cursor_timer >= 20:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)
        txt_surf = self.font.render(self.text, True, BLACK)
        surface.blit(txt_surf, (self.rect.x + 5, self.rect.y + 5))
        
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + txt_surf.get_width() + 2
            cursor_y = self.rect.y + 5
            pygame.draw.line(surface, BLACK, (cursor_x, cursor_y),
                             (cursor_x, cursor_y + self.rect.height - 10), 2)


def osint_level_page(screen, level, click_sound, city):
    """
    Full-page screen for a single OSINT level.
    Returns the appropriate GameState to navigate back.
    """
    from game import Button, UIElement, RenderUpdates, GameState

    dict_city_state = {
        "portland": GameState.PORTLAND,
        "eugene": GameState.EUGENE,
        "corvallis": GameState.CORVALLIS,
    }
    state = dict_city_state.get(city, GameState.NEWGAME)  # default to NEWGAME if city not found

    running = True
    clock = pygame.time.Clock()

    level_img = pygame.image.load(level.image_path).convert_alpha()
    level_img = pygame.transform.smoothscale(level_img, (400, 280))
    level_rect = level_img.get_rect(topleft=(90, 110))

    title_font = pygame.font.Font("assets/ByteBounce.ttf", 28)
    text_font = pygame.font.Font("assets/ByteBounce.ttf", 18)

    input_box = TextInput(pygame.Rect(530, 230, 180, 40))

    return_button = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=(0,0,0),
        text_rgb=(255,255,255),
        text="<--- Return to levels",
        action=state,
    )
    enter_button = Button(600, 300, "assets/buttons/enter_button.png", 1, action="CHECK")
    download_button = Button(100, 410, "assets/buttons/download_button.png", 1.25, action="DOWNLOAD")

    buttons = RenderUpdates(return_button, enter_button, download_button)

    download_message = ""

    while running:
        events = pygame.event.get()
        mouse_up = False
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    user_input = input_box.text.replace(" ", "")
                    solution = ",".join(level.answer)
                    if user_input == solution:
                        return state

        input_box.update(events)

        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            action = button.update(mouse_pos, mouse_up, click_sound)
            if action == state:  # Return button clicked
                return state
            elif action == "DOWNLOAD":
                try:
                    downloads_path = os.path.expanduser("~/Downloads")
                    filename = f"osint_level_{level.level_id}.jpg"
                    shutil.copy(level.image_path, os.path.join(downloads_path, filename))
                    download_message = "Image downloaded successfully!"
                except Exception:
                    download_message = "Error downloading image!"
            elif action == "CHECK":
                user_input = input_box.text.replace(" ", "")
                solution = ",".join(level.answer)
                if user_input == solution:
                    return state # FIXME, want to display correct icon
                else:
                    download_message = "Incorrect solution!"

        screen.fill((0,0,0))
        screen.blit(level_img, level_rect)
        pygame.draw.rect(screen, (40, 40, 40), (520, 110, 200, 360), border_radius=8)

        title_surf = title_font.render(f"Level {level.level_id}", True, (255,255,255))
        screen.blit(title_surf, (530, 120))
        instructions_surf = text_font.render("Enter solution in form 0.000,0.000", True, (200,200,200))
        screen.blit(instructions_surf, (530, 170))

        input_box.draw(screen)

        for button in buttons:
            button.draw(screen)

        if download_message:
            msg_surf = text_font.render(download_message, True, (255, 255, 255))
            msg_rect = msg_surf.get_rect(center=(300, 400))
            screen.blit(msg_surf, msg_rect)

        pygame.display.flip()
        clock.tick(60)


def load_city_levels(city_name: str):
    """Reads osint_levels/<city_name>/ and returns a list of OSINTLevel objects."""
    if city_name not in ["portland", "eugene", "corvallis"]:
        raise ValueError("Invalid city name")

    levels = []
    for i in range(1, 6):
        levels.append(OSINTLevel(city_name, i))
    return levels
