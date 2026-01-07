import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("OSINT CTF")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.Font('assets/ByteBounce.ttf', 36)

def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)
    draw_text("OSINT CTF - Press ESC to quit", 50, 50)

    pygame.display.flip()
    clock.tick(60)
