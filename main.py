import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo (1).png')
pygame.display.set_icon(icon)
playerIMG = pygame.image.load('arcade-game (1).png')
playerX = 370
playerY = 480

def player(x,y):
    screen.blit(playerIMG, (x, y))

running = True  
while running:
    screen.fill((0, 0, 128))
    playerX+=0.1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:

    player(playerX,playerY)

    pygame.display.update()