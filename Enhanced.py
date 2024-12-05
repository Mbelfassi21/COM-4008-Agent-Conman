import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 910, 580
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Agent Conman")

# Load images
bg = pygame.image.load("images/Background 910X584.png")
bg = pygame.transform.scale(bg, (width, height))  # Scale to fit the screen
mario_image = pygame.image.load("images/images.png").convert_alpha()
platform_image = pygame.image.load("images/piece of ground.jpg").convert_alpha()
coin_image = pygame.image.load("images/Coin 1.png").convert_alpha()

# Set color key and scale images
mario_image.set_colorkey((255, 255, 255))
scaled_mario_image = pygame.transform.scale(mario_image, (40, 40))
platform_image = pygame.transform.scale(platform_image, (100, 20))
coin_image = pygame.transform.scale(coin_image, (30, 30))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Clock settings
clock = pygame.time.Clock()
FPS = 60

# Font
font = pygame.font.SysFont("Arial", 36)

# Player attributes
player_size = 40
start_x, start_y = 50, height - 120 - player_size  # Start 120px from the bottom
mario_pos = pygame.Rect(start_x, start_y, player_size, player_size)
mario_speed = 5
is_jumping = False
jump_power = 10  # Adjusted jump power for better gameplay
gravity = 0.5  # Smoothed gravity for realistic falling
velocity_y = 0

# Ground
ground = pygame.Rect(0, height - 50, width, 50)

# Platforms
platforms = [
    pygame.Rect(200, height - 250 - 20, 100, 20),  # Corrected y-position of platforms
    pygame.Rect(400, height - 400 - 20, 100, 20),
    pygame.Rect(600, height - 550 - 20, 100, 20)
]

# Finish line
finish_line = pygame.Rect(width - 100, height - 150, 50, 50)

# Coin attributes
coin_size = 30

def generate_coin_position():
    while True:
        coin_x = random.randint(0, width - coin_size)
        coin_y = random.randint(0, height - coin_size - 100)
        coin_pos = [coin_x, coin_y]
        if not any(platform.collidepoint(coin_pos) for platform in platforms):
            return coin_pos

coin_pos = generate_coin_position()

# Score and level
score = 0
level = 1

# Menu variables
main_menu = True
paused = False
instructions = False

# Reset game function
def reset_game():
    global mario_pos, score, coin_pos, level
    mario_pos.topleft = (start_x, start_y)
    score = 0
    coin_pos = generate_coin_position()
    level = 1

# Collision detection function
def check_collision(rect, platforms):
    for platform in platforms:
        if rect.colliderect(platform):
            return platform
    return None

# Draw menu
def draw_menu():
    screen.fill(BLACK)
    title = font.render("Agent Conman", True, WHITE)
    screen.blit(title, (width // 2 - title.get_width() // 2, 100))
    options = ["Start Game", "Instructions", "Exit"]
    for i, option in enumerate(options):
        option_text = font.render(option, True, WHITE)
        screen.blit(option_text, (width // 2 - option_text.get_width() // 2, 200 + i * 50))

# Draw instructions
def draw_instructions():
    screen.fill(BLACK)
    lines = [
        "Instructions:",
        "1. Use arrow keys to move left and right.",
        "2. Press UP to jump.",
        "3. Collect coins and reach the finish line.",
        "4. Press P to pause the game.",
        "Press ESC to return to the menu."
    ]
    for i, line in enumerate(lines):
        text = font.render(line, True, WHITE)
        screen.blit(text, (50, 50 + i * 40))

# Draw pause menu
def draw_pause_menu():
    screen.fill(BLACK)
    pause_title = font.render("Paused", True, WHITE)
    screen.blit(pause_title, (width // 2 - pause_title.get_width() // 2, 100))
    options = ["Resume", "New Game", "Exit"]
    for i, option in enumerate(options):
        option_text = font.render(option, True, WHITE)
        screen.blit(option_text, (width // 2 - option_text.get_width() // 2, 200 + i * 50))

# Main game loop
running = True
while running:
    if main_menu:
        draw_menu()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main_menu = False
                elif event.key == pygame.K_2:
                    instructions = True
                elif event.key == pygame.K_3:
                    running = False

    elif instructions:
        draw_instructions()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    instructions = False
                    main_menu = True

    elif paused:
        draw_pause_menu()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    paused = False
                elif event.key == pygame.K_2:
                    reset_game()
                    paused = False
                elif event.key == pygame.K_3:
                    running = False

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = True

        # Game mechanics
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            mario_pos.x -= mario_speed
        if keys[pygame.K_RIGHT]:
            mario_pos.x += mario_speed
        if keys[pygame.K_UP] and not is_jumping:
            is_jumping = True
            velocity_y = -jump_power

        # Apply gravity
        velocity_y += gravity
        mario_pos.y += velocity_y

        # Boundary checks
        mario_pos.x = max(0, min(width - mario_pos.width, mario_pos.x))

        # Ground collision
        if mario_pos.y >= ground.y - mario_pos.height:
            mario_pos.y = ground.y - mario_pos.height
            velocity_y = 0
            is_jumping = False

        # Platform collision
        platform = check_collision(mario_pos, platforms)
        if platform and velocity_y > 0:
            mario_pos.y = platform.y - mario_pos.height
            velocity_y = 0
            is_jumping = False

        # Coin collision
        if mario_pos.colliderect(pygame.Rect(*coin_pos, coin_size, coin_size)):
            score += 1
            coin_pos = generate_coin_position()

        # Finish line collision
        if mario_pos.colliderect(finish_line):
            level += 1
            reset_game()

        # Draw everything
        screen.blit(bg, (0, 0))
        pygame.draw.rect(screen, BLACK, ground)
        for platform in platforms:
            screen.blit(platform_image, platform.topleft)
        screen.blit(scaled_mario_image, mario_pos)
        screen.blit(coin_image, coin_pos)
        pygame.draw.rect(screen, GREEN, finish_line)

        # Display score and level
        score_text = font.render(f"Score: {score}", True, RED)
        screen.blit(score_text, (10, 10))
        level_text = font.render(f"Level: {level}", True, RED)
        screen.blit(level_text, (width - 200, 10))

        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()
sys.exit()
