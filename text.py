import pygame

# --- Configuration ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
CIRCLE_COLOR = (0, 0, 0)  # Black circle
BACKGROUND_COLOR = (255, 255, 255)  # White background

# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Circle Opening Screen Effect")
clock = pygame.time.Clock()

# --- Animation Variables ---
center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2
# Calculate the maximum possible radius to cover the whole screen
max_radius = max(SCREEN_WIDTH, SCREEN_HEIGHT) // 2 + 50
current_radius = 0
animation_speed = 5  # Speed of the radius increase (pixels per frame)

# --- Main Game Loop ---
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update animation
    if current_radius < max_radius:
        current_radius += animation_speed
    else:
        # Stop animation once the screen is covered
        pass 

    # Drawing
    screen.fill(BACKGROUND_COLOR)  # Fill background first

    # Draw the expanding circle
    pygame.draw.circle(screen, CIRCLE_COLOR, (center_x, center_y), current_radius)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
