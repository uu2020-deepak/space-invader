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
enemy_imgs = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_imgs.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(0.15)
    enemy_y_change.append(40)

# Bullet setup
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 0.5
bullet_state = "ready"


def draw_player(x, y):
    """Draw the player sprite on the screen at position (x, y)"""
    screen.blit(player_img, (x, y))


def draw_enemy(x, y, i):
    """Draw the enemy sprite on the screen at position (x, y)"""
    screen.blit(enemy_imgs[i], (x, y))


def fire_bullet(x, y):
    """Fire bullet on the screen using space bar"""
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    """Check for collision between enemy and bullet"""
    distance = ((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2) ** 0.5
    return distance < 27


# Game loop
score = 0
running = True

while running:
    # Draw the background
    screen.blit(background, (0, 0))

    # Handle user input and window events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.5
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Update player position
    player_x += player_x_change

    # Clamp player position to screen boundaries
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Update enemy position and movement
    for i in range(num_of_enemies):
        enemy_x[i] += enemy_x_change[i]

        # Handle boundary collisions
        if enemy_x[i] <= 0:
            enemy_x[i] = 0
            enemy_x_change[i] = 0.15
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x[i] = 736
            enemy_x_change[i] = -0.15
            enemy_y[i] += enemy_y_change[i]

        # Check collision with bullet
        if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            bullet_y = 480
            bullet_state = "ready"
            score += 1
            print(f"Score: {score}")
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)

        draw_enemy(enemy_x[i], enemy_y[i], i)

    # Render all game objects on screen
    draw_player(player_x, player_y)

    # Update bullet movement
    if bullet_state == "fire":
        bullet_x = player_x + 16
        screen.blit(bullet_img, (bullet_x, bullet_y))
        bullet_y -= bullet_y_change

    # Reset bullet when it goes off screen
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    pygame.display.update()

    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
    # Update the display to show all drawn objects
    pygame.display.update()
