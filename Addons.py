import pygame
import sys
import random

# Initialize the game
pygame.init()

# Screen dimensions
width, height = 910, 580
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Agent Conman")

# Load images
agent_image = pygame.image.load("images/rb_7770.png").convert_alpha()
platform_image = pygame.image.load("images/piece of ground.jpg").convert_alpha()
coin_image = pygame.image.load("images/Coin 1.png").convert_alpha()

# Set the color key (RGB value of the background color to be removed)
agent_image.set_colorkey((255, 255, 255))  # Assuming the background is white

# Scale the character image
scaled_agent_image = pygame.transform.scale(agent_image, (40, 40))  # New size (width, height)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Clock settings
clock = pygame.time.Clock()
FPS = 60

# Player attributes
player_size = 40
start_x, start_y = 50, height - 500 - player_size  # Adjustable starting position (100px from the bottom)
agent_pos = pygame.Rect(start_x, start_y, player_size, player_size)
agent_speed = 5
jump_height = 35  # Increased jump height
is_jumping = False
jump_count = 10

# Gravity 
gravity = 0.3  # Reduced gravity
agent_velocity_y = 0

# Level elements
ground = pygame.Rect(0, height - 50, width, 50)  # Define the ground
platforms = [
    pygame.Rect(200, height - 150, 150, 30),  # Larger and lower platforms
    pygame.Rect(400, height - 250, 150, 30),
    pygame.Rect(600, height - 350, 150, 30)
]
finish_line = pygame.Rect(width - 100, height - 150, 50, 50)  # Finish line adjusted to be reachable and start from bottom
finish_line.y -= 350  # Moves the rectangle 50 pixels higher

# Coin attributes
coin_size = 30

def generate_coin_position():
    while True:
        coin_x = random.randint(0, width - coin_size)
        coin_y = random.randint(0, height - coin_size - 100)  # Ensure coin is reachable by player
        coin_pos = [coin_x, coin_y]
        if not any(platform.collidepoint(coin_pos) for platform in platforms):
            return coin_pos

coin_pos = generate_coin_position()

# Score
score = 0

# Font settings for the congratulatory message and pause menu
font = pygame.font.SysFont('Arial', 36)
congrats_message = font.render("You have reached your goal, Congratulations!", True, BLUE)
message_displayed = False

pause_font = pygame.font.SysFont('Arial', 48)
pause_texts = ["Resume", "New Game", "Exit"]
pause_buttons = []

for i in range(len(pause_texts)):
    text_surface = pause_font.render(pause_texts[i], True, WHITE)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2 + i * 60))
    pause_buttons.append((text_surface, text_rect))

paused = False

# Level display function
def draw_level_info(level):
    font = pygame.font.Font(None, 74)
    text = font.render(f"Level {level}", True, WHITE)
    screen.blit(text, (width // 2 - text.get_width() // 2, 10))

def draw_pause_menu():
    for text_surface, text_rect in pause_buttons:
        screen.blit(text_surface, text_rect)

def reset_game():
    global agent_pos, score, coin_pos
    agent_pos.topleft = (start_x, start_y)
    score = 0
    coin_pos = generate_coin_position()

# Game loop
level = 1
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
        
        if paused and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for i in range(len(pause_buttons)):
                if pause_buttons[i][1].collidepoint(mouse_pos):
                    if i == 0: # Resume button
                        paused = False
                    elif i == 1: # New Game button
                        reset_game()
                        paused = False
                    elif i == 2: # Exit button
                        running = False

    if not paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            agent_pos.x -= agent_speed
        if keys[pygame.K_RIGHT]:
            agent_pos.x += agent_speed
        if not is_jumping:
            if keys[pygame.K_UP]:
                is_jumping = True
        else:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                agent_pos.y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 10

        # Apply gravity
        agent_velocity_y += gravity 
        agent_pos.y += agent_velocity_y

        # Check for collision with the ground
        if agent_pos.y > ground.y - agent_pos.height:
            agent_pos.y = ground.y - agent_pos.height
            agent_velocity_y = 0

        # Check for collision with platforms
        for platform in platforms:
            if agent_pos.colliderect(platform) and agent_velocity_y > 0:
                agent_pos.y = platform.y - agent_pos.height
                agent_velocity_y = 0

        # Check if player reaches the finish line
        if agent_pos.colliderect(finish_line):
            print("Level Complete!")

        # Coin collision
        if (agent_pos[0] < coin_pos[0] < agent_pos[0] + player_size or agent_pos[0] < coin_pos[0] + coin_size < agent_pos[0] + player_size) and (agent_pos[1] < coin_pos[1] + player_size or agent_pos[1] < coin_pos[1] + coin_size < agent_pos[1] + player_size):
            score += 1
            coin_pos = generate_coin_position()

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, finish_line)
    pygame.draw.rect(screen, BLACK, ground)
    for platform in platforms:
        screen.blit(platform_image, platform.topleft)  
    screen.blit(scaled_agent_image, agent_pos)
    screen.blit(coin_image, coin_pos)

    # Display score
    font_score= pygame.font.SysFont("monospace",35)
    score_text= font_score.render("Score: "+str(score),True ,RED)
    screen.blit(score_text,(10 ,10))

    # Display the congratulatory message 
    if message_displayed: 
        screen.blit(congrats_message, (50, height // 2))

    # Display level info
    draw_level_info(level)

    if paused:
        draw_pause_menu()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
