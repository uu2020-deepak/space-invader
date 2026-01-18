import pygame
import random
from pygame import mixer
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

#background music
mixer.music.load('background.wav')
mixer.music.play(-1)

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
    enemy_x.append(random.randint(0, 735))  # Random starting X position
    enemy_y.append(random.randint(50, 150))  # Random starting Y position
    enemy_x_change.append(0.15)  # Horizontal movement speed
    enemy_y_change.append(40)  # Vertical movement speed (drops per edge touch)
#ready- bullet is on screen
#fire- bullet is visible and in motion

#bullet setup
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480  #starting Y position
bullet_x_change = 0
bullet_y_change = 7 #vertical speed
bullet_state = "ready"

def draw_player(x, y):
    """Draw the player sprite on the screen at position (x, y)"""
    screen.blit(player_img, (x, y))


def draw_enemy(x, y, i):
    """Draw the enemy sprite on the screen at position (x, y)"""
    screen.blit(enemy_imgs[i], (x, y))

def fire_bullet(x,y):
    """fire bullet on the screen using space bar"""
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x+16, y+10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    """Check for collision between enemy and bullet"""
    distance = ((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2) ** 0.5
    if distance < 27:
        return True
    else:
        return False

#score
score_value=0
font = pygame.font.Font("greats Race Italic.ttf", 50)
textX= 10
textY= 10

#game over text
over_font = pygame.font.Font("greats Race Italic.ttf", 100)

def show_score(x,y):
    score = font.render('score=' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))

def game_over_font():
    over_text = over_font.render("GAME OVER !!!", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
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
                player_x_change = -1
            if event.key == pygame.K_RIGHT:
                # Move player right
                player_x_change = 1
            if event.key == pygame.K_SPACE:
                # move bullet
                if bullet_state == "ready":
                    bullet_sound= mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
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
    for i in range(num_of_enemies):
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j]= 2000
            game_over_font()
            break


        enemy_x[i] += enemy_x_change[i]
    # Clamp enemy position and handle boundary behavior
    # Keep the enemy from going off the left edge
        if enemy_x[i] <= 0:
            enemy_x[i] = 0
        # Change direction to move right
            enemy_x_change[i] = 0.15
        # Move enemy down one step when it reaches the edge
            enemy_y[i] += enemy_y_change[i]
    # Keep the enemy from going off the right edge
        elif enemy_x[i] >= 736:
            enemy_x[i] = 736
        # Change direction to move left
            enemy_x_change[i] = -4
        # Move enemy down one step when it reaches the edge
            enemy_y[i] += enemy_y_change[i]
        collision= is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1

            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)
        draw_enemy(enemy_x[i], enemy_y[i], i)
    # Render all game objects on screen
    draw_player(player_x, player_y)
    draw_enemy(enemy_x[i], enemy_y[i], i)

    #movement of bullet
    if bullet_y <= 0 :
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
    # Update the display to show all drawn objects

    show_score(textX, textY)

    pygame.display.update()
