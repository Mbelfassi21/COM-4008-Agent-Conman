import pygame
import sys
import random

# Initialize the game
pygame.init()

# Screen dimensions
width, height = 910, 580
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Agent Conman")


# Defining Finish_Line
finish_line = pygame.Rect(width - 100, height - 150, 50, 50)  # Define finish line rectangle
finish_line.y -= 350  # Adjust position

# Load images
agent_image = pygame.image.load("images/rb_7770.png").convert_alpha()
platform_image = pygame.image.load("images/piece of ground.jpg").convert_alpha()
coin_image = pygame.image.load("images/Coin 1.png").convert_alpha()
finish_line_image = pygame.image.load("images/gold chest.png").convert_alpha()
scaled_finish_line_image = pygame.transform.scale(finish_line_image, (finish_line.width, finish_line.height))
menu_background_image = pygame.image.load("images/Menu_Bg.png").convert_alpha()
menu_background_image = pygame.transform.scale(menu_background_image, (width, height))  # Scale to screen size

spike_width, spike_height = 200, 40  # Make the spike image wider (60px width)

# Load spike image
spike_image = pygame.image.load("images/Spikes.png").convert_alpha()
scaled_spike_image = pygame.transform.scale(spike_image, (spike_width, spike_height))



# Pause button 
pause_button_width = 50
pause_button_height = 50
pause_button_rect = pygame.Rect(width - pause_button_width - 10, 10, pause_button_width, pause_button_height)

#Pause button icon
pause_button_image = pygame.image.load("images/pause_icon.png").convert_alpha()  # Replace with your image
pause_button_image = pygame.transform.scale(pause_button_image, (pause_button_width, pause_button_height))

#Music 
pygame.mixer.init()
pygame.mixer.music.load("images/BGM1.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Set the color key (RGB value of the background color to be removed)
agent_image.set_colorkey((255, 255, 255))  # Assuming the background is white

# Scale the character image
scaled_agent_image = pygame.transform.scale(agent_image, (40, 40))  # New size (width, height)

# Menu variables
main_menu = True
paused = False
instructions = False

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

#Font
custom_font = pygame.font.Font("Fonts/Algerian Regular.ttf", 72)  # Replace with your font file and desired size
title = custom_font.render("Agent Conman", True, WHITE)

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
# Level data initialization
ground = pygame.Rect(0, height - 50, width, 50)  # Define the ground

# Level data initialization
levels = [
    {  # Level 1
        "platforms": [
            pygame.Rect(120, height - 470, 150, 30),
            pygame.Rect(130, height - 265, 150, 30),
            pygame.Rect(290, height - 130, 150, 30),
            pygame.Rect(360, height - 340, 150, 30),
            pygame.Rect(560, height - 300, 150, 30),
        ],
        "finish_line": pygame.Rect(width - 80, height - 100, 50, 50),
    },
    {  # Level 2
        "platforms": [
            pygame.Rect(150, height - 200, 150, 30),
            pygame.Rect(350, height - 300, 150, 30),
            pygame.Rect(550, height - 470, 150, 30),
            pygame.Rect(750, height - 400, 150, 30)
        ],
        "finish_line": pygame.Rect(width - 100, height - 490, 50, 50),
    },
    {  # Level 3
        "platforms": [
            pygame.Rect(100, height - 150, 150, 30),
            pygame.Rect(300, height - 250, 150, 30),
            pygame.Rect(500, height - 235, 150, 30),
            pygame.Rect(700, height - 300, 150, 30)
        ],
        "finish_line": pygame.Rect(width - 150, height - 420, 50, 50),
    },
    {  # Level 4
        "platforms": [
            pygame.Rect(150, height - 180, 200, 30),
            pygame.Rect(450, height - 250, 150, 30),
            pygame.Rect(300, height - 400, 150, 30),
            pygame.Rect(600, height - 350, 200, 30)
        ],
        "finish_line": pygame.Rect(width - 100, height - 250, 50, 50),
    },
    {  # Level 5
        "platforms": [
            pygame.Rect(100, height - 150, 100, 30),
            pygame.Rect(300, height - 300, 120, 30),
            pygame.Rect(500, height - 400, 140, 30),
            pygame.Rect(700, height - 350, 160, 30),
            pygame.Rect(400, height - 400, 180, 30),
        ],
        "finish_line": pygame.Rect(width - 120, height - 500, 50, 50),
    },
    {  # Level 6
        "platforms": [
            pygame.Rect(50, height - 100, 120, 30),
            pygame.Rect(200, height - 250, 120, 30),
            pygame.Rect(400, height - 150, 120, 30),
            pygame.Rect(650, height - 300, 120, 30),
            pygame.Rect(800, height - 200, 120, 30)
        ],
        "finish_line": pygame.Rect(width - 80, height - 400, 50, 50),
    },
    {  # Level 7
        "platforms": [
            pygame.Rect(100, height - 200, 180, 30),
            pygame.Rect(350, height - 250, 200, 30),
            pygame.Rect(600, height - 400, 120, 30),
            pygame.Rect(400, height - 450, 100, 30),
            pygame.Rect(750, height - 150, 150, 30),
            pygame.Rect(200, height - 350, 145, 30)
        ],
        "finish_line": pygame.Rect(width - 220, height - 450, 50, 50),
    },
    {  # Level 8 (Final Level)
        "platforms": [
            pygame.Rect(50, height - 150, 100, 30),
            pygame.Rect(200, height - 300, 120, 30),
            pygame.Rect(400, height - 450, 150, 30),
            pygame.Rect(600, height - 200, 200, 30),
            #pygame.Rect(350, height - 400, 140, 30),
        ],
        "finish_line": pygame.Rect(width - 120, height - 400, 50, 50),
    }
]

# Function to load level elements
def load_level(level):
    global platforms, finish_line
    if level > len(levels):  # If no more levels
        print("Congratulations, you finished the game!")
        pygame.quit()
        sys.exit()
    platforms = levels[level - 1]["platforms"]  # Load platforms for the level
    finish_line = levels[level - 1]["finish_line"]  # Load the finish line for the level

# Initial level setup
level = 1  # Start from level 1
load_level(level)  # Load the first level

# Draw menu with clicks
def draw_menu():
    screen.blit(menu_background_image, (0, 0))
    custom_font = pygame.font.Font("Fonts/Algerian Regular.ttf", 72)  # Replace with your font file path
    title = custom_font.render("Agent Conman", True, BLACK)
    screen.blit(title, (width // 2 - title.get_width() // 2, 100))

    # Get the current mouse position
    mouse_pos = pygame.mouse.get_pos()
    custom_font2 = pygame.font.Font("Fonts/Algerian Regular.ttf", 50 )
    # Define menu options with rectangles
    options = ["Start Game", "Instructions", "Exit"]
    menu_buttons = []
    for i, option in enumerate(options):
        # Highlight the option if the mouse is over it
        highlight_color = YELLOW if pygame.Rect(width // 2 - 100, 200 + i * 50 - 10, 200, 40).collidepoint(mouse_pos) else BLACK
        option_text = custom_font2.render(option, True, highlight_color)
        option_rect = option_text.get_rect(center=(width // 2, 200 + i * 50))
        screen.blit(option_text, option_rect.topleft)
        menu_buttons.append((option_rect, option))  

    return menu_buttons


# Draw instructions
def draw_instructions():
    screen.fill(BLACK)
    lines = [
        "Instructions:",
        "1. Use arrow keys to move left and right.",
        "2. Press UP to jump.",
        "3. Collect coins and reach the finish line.",
        "4. Press P to pause the game.",
        "Click BACK to return to the menu."
    ]

    # Render instructions text
    for i, line in enumerate(lines):
        text = font.render(line, True, WHITE)
        screen.blit(text, (50, 50 + i * 40))

    # Get the current mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Highlight the Back button if hovered
    back_highlight_color = YELLOW if pygame.Rect(width // 2 - 50, height - 70, 100, 40).collidepoint(mouse_pos) else WHITE
    back_text = font.render("BACK", True, back_highlight_color)
    back_rect = back_text.get_rect(center=(width // 2, height - 50))
    screen.blit(back_text, back_rect.topleft)

    return back_rect

# Draw pause menu with clickable buttons
def draw_pause_menu():
    screen.fill(BLACK)
    pause_title = font.render("Paused", True, WHITE)
    screen.blit(pause_title, (width // 2 - pause_title.get_width() // 2, 100))

    # Get the current mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Define pause menu options with rectangles
    options = ["Resume", "New Game", "Exit"]
    pause_buttons = []
    for i, option in enumerate(options):
        # Highlight the option if the mouse is over it
        highlight_color = YELLOW if pygame.Rect(width // 2 - 100, 200 + i * 50 - 10, 200, 40).collidepoint(mouse_pos) else WHITE
        option_text = font.render(option, True, highlight_color)
        option_rect = option_text.get_rect(center=(width // 2, 200 + i * 50))
        screen.blit(option_text, option_rect.topleft)
        pause_buttons.append((option_rect, option))  

    return pause_buttons

# Coin attributes
coin_size = 30

#Spikes
spike_width, spike_height = 910, 40  # Dimensions of the spikes
lives = 3  # Player starts with 3 lives

def place_spikes_on_ground():
    spikes = []
    for i in range(100, width, 180):
        spike_x = i
        spike_y = ground.y - spike_height
        spikes.append(pygame.Rect(spike_x, spike_y, spike_width, spike_height)) 
    return spikes

spikes = place_spikes_on_ground()

def reset_lives():
    global lives
    lives = 3

    
# Function to place coins on platforms
def place_coins_on_platforms(platforms):
    coins = []
    for platform in platforms:
        platform_width = platform.width
        platform_x = platform.x
        platform_y = platform.y

        # Calculate positions for three coins evenly spaced on the platform
        coin_positions = [
            (platform_x + platform_width // 4 - coin_size // 2, platform_y - coin_size),
            (platform_x + platform_width // 2 - coin_size // 2, platform_y - coin_size),
            (platform_x + 3 * platform_width // 4 - coin_size // 2, platform_y - coin_size)
        ]

        for pos in coin_positions:
            coins.append(pygame.Rect(pos[0], pos[1], coin_size, coin_size))

    return coins

# Initialize coins
coins = place_coins_on_platforms(platforms)

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

def load_level(level):
    global platforms, coins, finish_line, agent_pos
    if level > len(levels):  # Check if the player has finished all levels
        print("You completed the game! Congratulations!")
        pygame.quit()
        sys.exit()

    # Load the new level's data
    platforms = levels[level - 1]["platforms"]
    finish_line = levels[level - 1]["finish_line"]
    coins = place_coins_on_platforms(platforms)
    agent_pos.topleft = (start_x, start_y)  # Reset agent position


# Level display function
def draw_level_info(level):
    font = pygame.font.Font(None, 74)
    text = font.render(f"Level {level}", True, WHITE)
    screen.blit(text, (width // 2 - text.get_width() // 2, 10))

def draw_pause_menu():
    for text_surface, text_rect in pause_buttons:
        screen.blit(text_surface, text_rect)

def reset_game():
    global level, score, lives, game_over
    level = 1  # Reset to the first level
    load_level(level)
    score = 0
    lives = 3  # Reset lives
    game_over = False

# Load the first level
load_level(level)

game_over = False

def draw_game_over_screen():
    screen.fill(BLACK)
    font_game_over = pygame.font.Font(None, 72)  # Adjust font size as needed
    game_over_text = font_game_over.render("You Lost!", True, RED)
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 100))

    # Draw the "New Game" button
    font_button = pygame.font.Font(None, 48)
    new_game_text = font_button.render("New Game", True, WHITE)
    new_game_rect = new_game_text.get_rect(center=(width // 2, height // 2 + 50))
    screen.blit(new_game_text, new_game_rect.topleft)

    return new_game_rect  # Return the button's rectangle for click detection

# Game loop 
level = 1
running = True

menu_buttons = []  # Store menu buttons
back_button = None  # Store back button for instructions

while running:
    if main_menu:
        menu_buttons = draw_menu()  # Draw main menu and get buttons
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse clicks
                mouse_pos = event.pos
                for button_rect, option in menu_buttons:
                    if button_rect.collidepoint(mouse_pos):  # If button is clicked
                        if option == "Start Game":
                            main_menu = False  # Start the game
                        elif option == "Instructions":
                            instructions = True  # Go to instructions menu
                            main_menu = False
                        elif option == "Exit":
                            running = False  # Exit the game

    elif instructions:
        back_button = draw_instructions()  # Draw instructions screen
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse clicks
                mouse_pos = event.pos
                if back_button.collidepoint(mouse_pos):  # If back button is clicked
                    instructions = False
                    main_menu = True  # Return to the main menu

    elif paused:
        draw_pause_menu()  # Draw pause menu
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, (_, button_rect) in enumerate(pause_buttons):
                    if button_rect.collidepoint(mouse_pos):
                        if i == 0:  # Resume button
                           paused = False
                        elif i == 1:  # New Game button
                             reset_game()
                             paused = False
                        elif i == 2:  # Exit button
                             running = False
                if pause_button_rect.collidepoint(mouse_pos):  # Unpause if pause button clicked
                     paused = False
    
    elif game_over:
        new_game_button = draw_game_over_screen()  # Draw the game over screen
        pygame.display.flip()

        for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
           elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if new_game_button.collidepoint(mouse_pos):  # Restart the game if the button is clicked
                   reset_game()  # Reset the game variables
                   game_over = False


    else:  # Game state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse clicks
                mouse_pos = event.pos
                if pause_button_rect.collidepoint(mouse_pos):  # If pause button is clicked
                    paused = not paused  # Toggle pause state


        # Player movement logic
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

        # Check for collision with spikes
        for spike in spikes:
            if agent_pos.colliderect(spike):
                lives -= 1
                agent_pos.topleft = (start_x, start_y)  # Reset agent position
                if lives <= 0:
                  game_over = True


        # Check if player reaches the finish line
            if agent_pos.colliderect(finish_line):
               level += 1  # Advance to the next level
               load_level(level)  # Load the new level

        # Coin collision
        for coin in coins:
            if agent_pos.colliderect(coin):
                score += 1
                coins.remove(coin)

        # Spike collision
        for spike in spikes:
            if agent_pos.colliderect(spike):
                lives -= 1
                print(f"Lives remaining: {lives}")
                if lives <= 0:
                    print("Game Over!")
                    running = False
                # Reset player position after losing a life
                agent_pos.topleft = (start_x, start_y)


        # Constrain player within the screen boundaries
        if agent_pos.x < 0:
            agent_pos.x = 0
        elif agent_pos.x + agent_pos.width > width:
            agent_pos.x = width - agent_pos.width

        if agent_pos.y < 0:
            agent_pos.y = 0
        elif agent_pos.y + agent_pos.height > height:
            agent_pos.y = height - agent_pos.height

        # Draw everything
        screen.fill(BLACK)
        screen.blit(scaled_finish_line_image, finish_line.topleft)
        screen.blit(pause_button_image, pause_button_rect.topleft)
        pygame.draw.rect(screen, BLACK, ground)
        for platform in platforms:
            screen.blit(platform_image, platform.topleft)
        screen.blit(scaled_agent_image, agent_pos)
        for coin in coins:
            screen.blit(coin_image, coin.topleft)
        for spike in spikes:
            screen.blit(scaled_spike_image, spike.topleft)

        # Display score
        font_score = pygame.font.SysFont("monospace", 35)
        score_text = font_score.render("Score: " + str(score), True, RED)
        screen.blit(score_text, (10, 10))

        # Display lives
        lives_text = font_score.render("Lives: " + str(lives), True, GREEN)
        screen.blit(lives_text, (10, 50))

        # Display level info
        draw_level_info(level)

        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()
sys.exit()