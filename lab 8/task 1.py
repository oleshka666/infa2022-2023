import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((800, 600))
fill = [0, 255, 255]
screen.fill(fill)
#rect(screen, color, (x1, y1, x2 - x1, y2 - y1), 2)

circle(screen, (255, 255, 0), (200, 175), 100)
circle(screen, (0, 0, 0), (200, 175), 100, 5)

circle(screen, (255, 0, 255), (150, 150), 30)
circle(screen, (255, 0, 255), (250, 150), 20)
circle(screen, (25, 25, 112), (150, 150), 30, 5)
circle(screen, (25, 25, 112), (250, 150), 20, 5)

circle(screen, (25, 25, 112), (250, 150), 10)
circle(screen, (25, 25, 112), (150, 150), 15)

polygon(screen, (0, 0, 255), [(193, 135), (85, 74)], 25)
polygon(screen, (0, 0, 255), [(232, 132), (306, 90)], 15)
polygon(screen, (0, 0, 255), [(162, 234), (229, 234)], 25)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos)
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
