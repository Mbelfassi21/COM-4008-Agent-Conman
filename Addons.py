import pygame
import sys

# Initialize the game
pygame.init()

# Screen dimensions
width = 910
height = 580
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Agent Conman")

# Load images
<<<<<<< Updated upstream
agent_image = pygame.image.load("images/rb_7770.png").convert_alpha()
=======
ground_zone_image = pygame.image.load("images/background.jpg").convert_alpha()
mario_image = pygame.image.load("images/rb_7770.png").convert_alpha()
>>>>>>> Stashed changes
platform_image = pygame.image.load("images/piece of ground.jpg").convert_alpha()
coin_image = pygame.image.load("images/Coin 1.png").convert_alpha()

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

# Clock settings
clock = pygame.time.Clock()
FPS = 60

# Player attributes
player_size = 40
start_x, start_y = 50, height - 500 - player_size  # Adjustable starting position (100px from the bottom)
<<<<<<< Updated upstream
agent_pos = pygame.Rect(start_x, start_y, player_size, player_size)
agent_speed = 5
=======
mario_pos = pygame.Rect(start_x, start_y, player_size, player_size)
mario_speed = 5
>>>>>>> Stashed changes
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
finish_line.y -= 350  # Moves the rectangle 350 pixels higher


# Draw menu with clicks
def draw_menu():
    screen.fill(BLACK)
    title = font.render("Agent Conman", True, WHITE)
    screen.blit(title, (width // 2 - title.get_width() // 2, 100))

    # Define menu options with rectangles
    options = ["Start Game", "Instructions", "Exit"]
    menu_buttons = []
    for i, option in enumerate(options):
        option_text = font.render(option, True, WHITE)
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

    # Add a Back button
    back_text = font.render("BACK", True, WHITE)
    back_rect = back_text.get_rect(center=(width // 2, height - 50))
    screen.blit(back_text, back_rect.topleft)

    return back_rect  # Return Back button for interaction

# Draw pause menu with clickable buttons
def draw_pause_menu():
    screen.fill(BLACK)
    pause_title = font.render("Paused", True, WHITE)
    screen.blit(pause_title, (width // 2 - pause_title.get_width() // 2, 100))

    # Define pause menu options with rectangles
    options = ["Resume", "New Game", "Exit"]
    pause_buttons = []
    for i, option in enumerate(options):
        option_text = font.render(option, True, WHITE)
        option_rect = option_text.get_rect(center=(width // 2, 200 + i * 50))
        screen.blit(option_text, option_rect.topleft)
        pause_buttons.append((option_rect, option))  # Store rect and associated option text

    return pause_buttons  # Return buttons for interaction

# Define ground zones
ground_zones = [
    pygame.Rect(0, height - 100, width, 50),  # Example zone
    pygame.Rect(100, height - 150, 50, 50),  # Another example zone
]

# Coin attributes
coin_size = 30

<<<<<<< Updated upstream
# Function to place coins on platforms
def place_coins_on_platforms(platforms):
    coins = []
    for platform in platforms:
        platform_width = platform.width
        platform_x = platform.x
        platform_y = platform.y
=======
def generate_coin_position():
    while True:
        coin_x = random.randint(0, width - coin_size)
        coin_y = random.randint(0, height - coin_size - 100)  # Ensure coin is reachable by player
        coin_pos = [coin_x, coin_y]
        if not any(platform.collidepoint(coin_pos) for platform in platforms):
            return coin_pos
>>>>>>> Stashed changes

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

# Level display function
def draw_level_info(level):
    font = pygame.font.Font(None, 74)
    text = font.render(f"Level {level}", True, WHITE)
    screen.blit(text, (width // 2 - text.get_width() // 2, 10))

def draw_pause_menu():
    for text_surface, text_rect in pause_buttons:
        screen.blit(text_surface, text_rect)

def reset_game():
    global agent_pos, score, coins
    agent_pos.topleft = (start_x, start_y)
    score = 0
    coins = place_coins_on_platforms(platforms)

# Before the game loop
pygame.mixer.init()
pygame.mixer.music.load("images/BGM1.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Game loop 

for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:  # Increase volume
            volume = min(pygame.mixer.music.get_volume() + 0.1, 1.0)
            pygame.mixer.music.set_volume(volume)
        if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:  # Decrease volume
            volume = max(pygame.mixer.music.get_volume() - 0.1, 0.0)
            pygame.mixer.music.set_volume(volume)

level = 1
running = True

<<<<<<< Updated upstream
=======
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
                    if i == 0:  # Resume button
                        paused = False
                    elif i == 1:  # New Game button
                        reset_game()
                        paused = False
                    elif i == 2:  # Exit button
                        running = False
>>>>>>> Stashed changes

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
            if event.type == pygame.MOUSEBUTTONDOWN:
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

    else:  # Game state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = True

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

        # Check for collision with ground zones
        for zone in ground_zones:
            if mario_pos.colliderect(zone):
                mario_pos.x, mario_pos.y = 15, 500

        # Check if player reaches the finish line
        if agent_pos.colliderect(finish_line):
            message_displayed = True
            pygame.time.delay(2000)  # Display congratulatory message briefly
            running = False  # End the game after finishing

        # Coin collision
        for coin in coins:
            if agent_pos.colliderect(coin):
                score += 1
                coins.remove(coin)

<<<<<<< Updated upstream
        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, finish_line)
        pygame.draw.rect(screen, BLACK, ground)
        for platform in platforms:
            screen.blit(platform_image, platform.topleft)
        screen.blit(scaled_agent_image, agent_pos)
        for coin in coins:
            screen.blit(coin_image, coin.topleft)

        # Display score
        font_score = pygame.font.SysFont("monospace", 35)
        score_text = font_score.render("Score: " + str(score), True, RED)
        screen.blit(score_text, (10, 10))

        # Display level info
        draw_level_info(level)
=======
    # Draw everything
    screen.blit(ground_zone_image, (50, 400))  # Draw the background
    pygame.draw.rect(screen, GREEN, finish_line)  # Draw the finish line
    pygame.draw.rect(screen, BLACK, ground)  # Draw the ground
    for platform in platforms:
        screen.blit(platform_image, platform.topleft)  # Draw the platforms
    for zone in ground_zones:
        pygame.draw.rect(screen, RED, zone, 2)  # Draw the ground zones for visualization
    screen.blit(scaled_mario_image, mario_pos)  # Draw the player
    screen.blit(coin_image, coin_pos)  # Draw the coin

    # Display score
    font_score = pygame.font.SysFont("monospace", 35)
    score_text = font_score.render("Score: " + str(score), True, RED)
    screen.blit(score_text, (10, 10))

    # Display the congratulatory message
    if message_displayed:
        screen.blit(congrats_message, (50, height // 2))
>>>>>>> Stashed changes

        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()
sys.exit()