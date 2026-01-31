import pygame
import random
from pygame import mixer
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo (1).png')
pygame.display.set_icon(icon)

background = pygame.image.load('background.jpg')

mixer.music.load('background.wav')
mixer.music.play(-1)

player_img = pygame.image.load('arcade-game (1).png')
player_x = 370
player_y = 480
player_x_change = 0

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

bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 1
bullet_state = "ready"

def draw_player(x, y):
    screen.blit(player_img, (x, y))

def draw_enemy(x, y, i):
    screen.blit(enemy_imgs[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x+16, y+10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = ((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2) ** 0.5
    if distance < 27:
        return True
    else:
        return False

score_value = 0
font = pygame.font.Font("greats Race Italic.ttf", 50)
textX = 10
textY = 10

over_font = pygame.font.Font("greats Race Italic.ttf", 100)

def show_score(x, y):
    score = font.render('score=' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_font():
    over_text = over_font.render("GAME OVER !!!", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

running = True
while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -1
            if event.key == pygame.K_RIGHT:
                player_x_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(num_of_enemies):
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_font()
            break

        enemy_x[i] += enemy_x_change[i]

        if enemy_x[i] <= 0:
            enemy_x[i] = 0
            enemy_x_change[i] = 0.15
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x[i] = 736
            enemy_x_change[i] = -4
            enemy_y[i] += enemy_y_change[i]

        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1

            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)
        draw_enemy(enemy_x[i], enemy_y[i], i)

    draw_player(player_x, player_y)
    draw_enemy(enemy_x[i], enemy_y[i], i)

    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    show_score(textX, textY)

    pygame.display.update()