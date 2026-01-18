import pygame
import random
pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set game window title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo (1).png')
pygame.display.set_icon(icon)

# Load background image
background = pygame.image.load('background.jpg')

# Player setup
player_img = pygame.image.load('arcade-game (1).png')
player_x = 370  # Starting X position
player_y = 480  # Starting Y position (bottom of screen)
player_x_change = 0  # Player movement speed

# Enemy setup
enemy_img = pygame.image.load('enemy.png')
enemy_x = random.randint(0, 800)  # Random starting X position
enemy_y = random.randint(50, 150)  # Random starting Y position
enemy_x_change = 0.15  # Horizontal movement speed
enemy_y_change = 40  # Vertical movement speed (drops per edge touch)

def draw_player(x, y):
    """Draw the player sprite on the screen at position (x, y)"""
    screen.blit(player_img, (x, y))


def draw_enemy(x, y):
    """Draw the enemy sprite on the screen at position (x, y)"""
    screen.blit(enemy_img, (x, y))




# Game loop
running = True
while running:
    # Draw the background
    screen.blit(background, (0, 0))
    
    # Handle user input and window events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Close the game when user clicks window close button
            running = False
        if event.type == pygame.KEYDOWN:
            # When user presses a key
            if event.key == pygame.K_LEFT:
                # Move player left
                player_x_change = -0.1
            if event.key == pygame.K_RIGHT:
                # Move player right
                player_x_change = 0.1
        if event.type == pygame.KEYUP:
            # When user releases a key
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # Stop player movement
                player_x_change = 0
    
    # Update player position
    player_x += player_x_change
    
    # Clamp player position to screen boundaries
    # Keep the player from going off the left edge
    if player_x <= 0:
        player_x = 0
    # Keep the player from going off the right edge
    # 736 = 800 (screen width) - 64 (player sprite width)
    elif player_x >= 736:
        player_x = 736
    
    # Update enemy position and movement
    # Move the enemy horizontally
    enemy_x += enemy_x_change
    
    # Clamp enemy position and handle boundary behavior
    # Keep the enemy from going off the left edge
    if enemy_x <= 0:
        enemy_x = 0
        # Change direction to move right
        enemy_x_change = 0.15
        # Move enemy down one step when it reaches the edge
        enemy_y += enemy_y_change
    # Keep the enemy from going off the right edge
    elif enemy_x >= 736:
        enemy_x = 736
        # Change direction to move left
        enemy_x_change = -0.15
        # Move enemy down one step when it reaches the edge
        enemy_y += enemy_y_change
    # Render all game objects on screen
    draw_player(player_x, player_y)
    draw_enemy(enemy_x, enemy_y)
    
    # Update the display to show all drawn objects
    pygame.display.update()
