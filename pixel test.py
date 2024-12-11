import pygame

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 910
screen_height = 580
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Find Coordinates")

# Main game loop
running = True
font = pygame.font.Font(None, 30)  # Font for displaying coordinates
while running:
    screen.fill((0, 0, 0))  # Clear the screen with black

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Render the text with the mouse coordinates
    text = font.render(f"Mouse Position: {mouse_x}, {mouse_y}", True, (255, 255, 255))
    screen.blit(text, (10, 10))  # Display the coordinates at the top-left corner

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
