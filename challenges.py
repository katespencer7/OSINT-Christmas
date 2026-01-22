import pygame, shutil, os, pyperclip, time
# from pygame.sprite import Sprite

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
GREEN = (0, 200, 0)

point_vals = {1:1000, 2:1500, 3:2000, 4:3000, 5:5000}

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
        self.cursor_pos = 0

        pygame.key.set_repeat(300, 50) # enable key repeat for held keys

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = True
                    mouse_x = event.pos[0] - (self.rect.x + 5) # calculate cursor position for mouse click
                    self.cursor_pos = self._get_cursor_from_pos(mouse_x)
                else:
                    self.active = False
            
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    if self.cursor_pos > 0:
                        self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
                        self.cursor_pos -= 1
                
                elif event.key == pygame.K_DELETE:
                    if self.cursor_pos < len(self.text):
                        self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
                
                elif event.key == pygame.K_LEFT: # left arrow
                    self.cursor_pos = max(0, self.cursor_pos - 1)
                
                elif event.key == pygame.K_RIGHT: # right arrow
                    self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
                
                elif event.key == pygame.K_HOME:
                    self.cursor_pos = 0
                
                elif event.key == pygame.K_END:
                    self.cursor_pos = len(self.text)
                
                elif event.key == pygame.K_RETURN: # enter key
                    pass
                
                elif event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL or event.mod & pygame.KMOD_META):
                    try:
                        clip = pyperclip.paste()
                        if clip:
                            self.text = self.text[:self.cursor_pos] + clip + self.text[self.cursor_pos:]
                            self.cursor_pos += len(clip)
                    except Exception:
                        pass
                else: # insert charatcer at cursor position
                    self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
                    self.cursor_pos += len(event.unicode)
        
        self.cursor_timer += 1
        
        if self.cursor_timer >= 20: # cursor blink rate
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def _get_cursor_from_pos(self, mouse_x):
        """Calculate cursor position based on mouse x coordinate."""
        for i in range(len(self.text) + 1):
            text_width = self.font.render(self.text[:i], True, BLACK).get_width()
            if mouse_x < text_width:
                return max(0, i)
        
        return len(self.text)

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)
        txt_surf = self.font.render(self.text, True, BLACK)
        
        cursor_text = self.text[:self.cursor_pos] # calcuate cursor position
        cursor_width = self.font.render(cursor_text, True, BLACK).get_width()
        
        text_width = txt_surf.get_width() # calcuate text width
        available_width = self.rect.width - 10  # 5px padding on each side
        
        text_x = self.rect.x + 5 # text offset
        if text_width > available_width: # scrolling logic
            if cursor_width > available_width:
                text_x = self.rect.x + 5 - (cursor_width - available_width)
            elif cursor_width < 0:
                text_x = self.rect.x + 5 - cursor_width
        
        clip_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        surface.set_clip(clip_rect) # prevent text from overflowing box
        
        surface.blit(txt_surf, (text_x, self.rect.y + 5))
        
        if self.active and self.cursor_visible:
            cursor_x = text_x + cursor_width
            cursor_y = self.rect.y + 5
            pygame.draw.line(surface, BLACK, (cursor_x, cursor_y),
                             (cursor_x, cursor_y + self.rect.height - 10), 2)
        
        surface.set_clip(None)


def osint_level_page(screen, level, click_sound, city, player):
    """
    Full-page screen for a single OSINT level.
    Returns the appropriate GameState to navigate back.
    """
    from game import Button, UIElement, RenderUpdates, GameState

    correct_sound = pygame.mixer.Sound("assets/sounds/90s-game-ui-11-185104.wav")
    wrong_sound = pygame.mixer.Sound("assets/sounds/classic-game-action-negative-5-224417.wav")
    points_sound = pygame.mixer.Sound("assets/sounds/get-coin-351945.wav")

    dict_city_state = {
        "portland": GameState.PORTLAND,
        "eugene": GameState.EUGENE,
        "corvallis": GameState.CORVALLIS,
    }
    state = dict_city_state.get(city, GameState.NEWGAME)

    running = True
    clock = pygame.time.Clock()
    
    is_completed = player.check_levels(level.level_id, city) # check if level already completed

    level_img = pygame.image.load(level.image_path).convert_alpha()
    level_img = pygame.transform.smoothscale(level_img, (450, 330))
    level_rect = level_img.get_rect(topleft=(50, 80))

    title_font = pygame.font.Font("assets/ByteBounce.ttf", 45)
    text_font = pygame.font.Font("assets/ByteBounce.ttf", 20)
    coin_font = pygame.font.Font("assets/ByteBounce.ttf", 24)

    input_box = TextInput(pygame.Rect(530, 280, 210, 40))

    return_button = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=(0,0,0),
        text_rgb=(255,255,255),
        text="<--- Return to levels",
        action=state,
    )
    enter_button = Button(675, 340, "assets/buttons/enter_button.png", 1, action="CHECK")
    download_button = Button(52, 430, "assets/buttons/download_button.png", 1.35, action="DOWNLOAD")
    buttons = RenderUpdates(return_button, enter_button, download_button)

    download_message = ""
    result_image = None
    result_timer = 0
    show_points = False
    points_timer = 0
    points_awarded = 0

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
                        correct_sound.play()
                        result_image = pygame.image.load("assets/level_icons/check.png").convert_alpha()
                        result_timer = 80  # Display for 2 seconds at 60 fps
                        if not is_completed:
                            points_awarded = point_vals[level.level_id]
                    else:
                        wrong_sound.play()
                        result_image = pygame.image.load("assets/level_icons/x.png").convert_alpha()
                        result_timer = 80  # Display for 2 seconds at 60 fps


        input_box.update(events)
        
        # result image timer
        if result_timer > 0:
            result_timer -= 1
            if result_timer == 0:
                result_image = None
                
                if points_awarded > 0 and not show_points:
                    points_sound.play()
                    show_points = True
                    points_timer = 80
        
        # points display timer
        if points_timer > 0:
            points_timer -= 1
            if points_timer == 0:
                show_points = False
                player.points += points_awarded
                player.save_game()
                player.update_levels(level.level_id, city)
                points_awarded = 0

        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button_sound = None if button == enter_button else click_sound
            action = button.update(mouse_pos, mouse_up, button_sound)
            
            if action == state:
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
                    correct_sound.play()
                    result_image = pygame.image.load("assets/level_icons/check.png").convert_alpha()
                    result_timer = 120  # Display for 2 seconds at 60 fps
                    # Only award points if not already completed
                    if not is_completed:
                        points_awarded = point_vals[level.level_id]
                else:
                    wrong_sound.play()
                    result_image = pygame.image.load("assets/level_icons/x.png").convert_alpha()
                    result_timer = 80

        screen.fill((0,0,0))
        from screens import coin_banner
        coin_banner(screen, player)
        screen.blit(level_img, level_rect)
        pygame.draw.rect(screen, (40, 40, 40), (520, 80, 230, 450))

        title_surf = title_font.render(f"LEVEL {level.level_id}", True, (255,255,255))
        screen.blit(title_surf, (570, 95))
        
        if is_completed == True: # display if level is already completed
            level_completed_text(screen, level, coin_font, text_font)
        
        instructions_surf = text_font.render(f"Enter solution in form:", True, (200,200,200))
        instructions_sol = text_font.render(f"##.###,##.###", True, (200,200,200))
        screen.blit(instructions_surf, (530, 150))
        screen.blit(instructions_sol, (540, 167))

        example_surf = text_font.render("Example solution:", True, (200,200,200))
        example_sol = text_font.render("44.0175976,-123.9408846", True, (200,200,200))
        screen.blit(example_surf, (530, 210))
        screen.blit(example_sol, (540, 227))

        input_box.draw(screen) # text input box

        for button in buttons:
            button.draw(screen)

        if download_message:
            msg_surf = text_font.render(download_message, True, (255, 255, 255))
            msg_rect = msg_surf.get_rect(center=(320, 455))
            screen.blit(msg_surf, msg_rect)
        
        if result_image:
            img_rect = result_image.get_rect(center=(640, 450))
            screen.blit(result_image, img_rect)
        
        if show_points:
            points_surf = coin_font.render(f"+{points_awarded}", True, (255, 202, 40))
            points_rect = points_surf.get_rect(center=(705, 45))
            screen.blit(points_surf, points_rect)
        
        if player.check_levels(level.level_id, city): # recompute if level just completed
            level_completed_text(screen, level, coin_font, text_font)

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


def level_completed_text(screen, level, coin_font, text_font):
    """Display level completed message with points awarded."""
    completed_surf = coin_font.render("LEVEL COMPLETED!", True, (102, 187, 106))
    correct_surf = text_font.render(f"Correct solution:", True, (102, 187, 106))
    correct_sol = text_font.render(f"{",".join(level.answer)}", True, (102, 187, 106))
    screen.blit(completed_surf, (530, 400))
    screen.blit(correct_surf, (530, 430))
    screen.blit(correct_sol, (540, 450))