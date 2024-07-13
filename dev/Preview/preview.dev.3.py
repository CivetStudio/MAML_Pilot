import pygame
import sys

# Initialize Pygame
pygame.init()

# Set window size and title
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Drawing Game")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up drawing variables
drawing = False
last_pos = None
brush_size = 5
brush_color = BLACK

# Set up toolbar UI
toolbar_height = 50
toolbar_surface = pygame.Surface((WINDOW_WIDTH, toolbar_height))
toolbar_surface.fill((200, 200, 200))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if event.pos[1] < toolbar_height:  # Check if clicked on toolbar
                    if 50 <= event.pos[0] <= 100:  # Color picker button
                        brush_color = screen.get_at(event.pos)
                    elif 150 <= event.pos[0] <= 200:  # Increase brush size button
                        brush_size = min(50, brush_size + 1)
                    elif 250 <= event.pos[0] <= 300:  # Decrease brush size button
                        brush_size = max(1, brush_size - 1)
                    elif 350 <= event.pos[0] <= 400:  # Clear screen button
                        screen.fill(WHITE)
                    elif 450 <= event.pos[0] <= 500:  # Exit button
                        running = False
                else:  # Clicked on canvas
                    drawing = True
                    last_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                current_pos = event.pos
                pygame.draw.line(screen, brush_color, last_pos, current_pos, brush_size)
                last_pos = current_pos

    # Draw toolbar UI
    screen.blit(toolbar_surface, (0, 0))
    # Draw toolbar buttons
    pygame.draw.rect(toolbar_surface, RED, (50, 10, 50, 30))  # Color picker button
    pygame.draw.rect(toolbar_surface, GREEN, (150, 10, 50, 30))  # Increase brush size button
    pygame.draw.rect(toolbar_surface, GREEN, (250, 10, 50, 30))  # Decrease brush size button
    pygame.draw.rect(toolbar_surface, BLUE, (350, 10, 50, 30))  # Clear screen button
    pygame.draw.rect(toolbar_surface, BLACK, (450, 10, 50, 30))  # Exit button

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
