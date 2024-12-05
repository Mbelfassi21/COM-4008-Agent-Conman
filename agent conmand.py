import pygame
import sys
import random

# Initialize the game
pygame.init()

# Screen dimensions
width, height = 960, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Agent Command")

# Load images
bg = pygame.image.load("images/Baground.png")
agent_image = pygame.image.load("images/images.png").convert_alpha()
image = pygame.image.load("images/piece of ground.jpg")
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
CHARACTER_COLOR = (255, 100, 0)

# Clock settings
clock = pygame.time.Clock()
FPS = 60

# Player attributes
player_size = 40
agent_pos = pygame.Rect(100, 255, player_size, player_size)
agent_speed = 10

# Gravity 
gravity = 0.2
agent_image_velocity_y = 0
ground_level = 295

#coin attributes
coin_size = 30
coin_image = pygame.image.load("images/coin.jpg")
coin_pos = [random.randint(0, width - coin_size), random.randint(0, height - coin_size)]

#score
score = 0

# Level elements
ground = pygame.Rect(0, height - 50, width, 50)  # Define the ground
prohibited_zones = [pygame.Rect(300, 300, 100, 50), pygame.Rect(150, 200, 100, 50)]
safe_zone = pygame.Rect(300, 200, 50, 50)

# Font settings for the congratulatory 
font = pygame.font.SysFont('Arial', 36) 
congrats_message = font.render("You have reached your goal, Congratulations!", True, BLUE) 
message_displayed = False

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Movement of character
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        agent_pos.x -= agent_speed
    if keys[pygame.K_RIGHT]:
        agent_pos.x += agent_speed
    if keys[pygame.K_DOWN]:
        if agent_pos.y + agent_speed <= 255:
            agent_pos.y += agent_speed
    if keys[pygame.K_UP]:
        agent_pos.y -= agent_speed

    # Apply gravity
    agent_image_velocity_y += gravity 
    agent_pos.y += agent_image_velocity_y
    
    # Check for collision with the ground 
    if agent_pos.y > ground_level - agent_pos.height: 
        agent_pos.y = ground_level - agent_pos.height
        agent_image_velocity_y = 0

    # Collision detection
    if agent_pos.colliderect(ground):
        # Reset position if collided with the ground
        if keys[pygame.K_DOWN]:
            agent_pos.y -= agent_speed
        if keys[pygame.K_UP]:
            agent_pos.y += agent_speed

    for zone in prohibited_zones:
        if agent_pos.colliderect(zone):
            # Reset position if collided with prohibited zone
            agent_pos.x, agent_pos.y = 100, 255

    # Check if player reaches the safe zone
    if agent_pos.colliderect(safe_zone) and not message_displayed: message_displayed = True

    # Draw everything in the correct order
    screen.blit(bg, (0, 0))  # Draw background
    pygame.draw.rect(screen, GREEN, safe_zone)  # Draw safe zone
    for zone in prohibited_zones:
        pygame.draw.rect(screen, RED, zone)  # Draw prohibited zones
    screen.blit(scaled_agent_image, agent_pos)  # Draw scaled player
    screen.blit(image, (0 ,295))
    screen.blit(image, (224 ,295))
    screen.blit(image, (448 ,295))
    screen.blit(image, (0 ,381))
    screen.blit(image, (224 ,381))
    screen.blit(image, (448 ,381))

    #coin collision
    if (agent_pos[0] < coin_pos[0] < agent_pos[0] + player_size or agent_pos[0] < coin_pos[0] + coin_size < agent_pos[0] + player_size) and (agent_pos[1] < coin_pos[1] + player_size or agent_pos[1] < coin_pos[1] + coin_size < agent_pos[1] + player_size):
        score += 1
        coin_pos = [random.randint(0, width - coin_size), random.randint(0, height - coin_size)]

    #display score
    font = pygame.font.SysFont("monospace", 35)
    score_text = font.render("Score: " + str(score), True, RED)
    screen.blit(score_text, (10, 10)) 

    # Display the congratulatory message
    if message_displayed: 
        screen.blit(congrats_message, (50, height // 2))

    # Update screen
    pygame.display.flip()
    clock.tick(FPS)

# Quit game
pygame.quit()
sys.exit()
