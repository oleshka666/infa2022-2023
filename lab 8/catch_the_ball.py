import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 1
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball():
    '''рисует новый шарик '''
    global x, y, r
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(50, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)


def new_ellipse():
    '''рисует новый шарик '''
    global x1, y1, a, b
    x1 = randint(100, 1100)
    y1 = randint(100, 900)
    a = randint(100, 200)
    b = randint(50, 100)
    color = COLORS[randint(0, 5)]
    ellipse(screen, color, (x1, y1, a, b))


def click(event):
    print(x, y, r)


pygame.display.update()
clock = pygame.time.Clock()
finished = False
pygame.display.set_caption("My program")

count = 0

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        '''if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos)'''
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # print('Click!')
            # click(pygame.MOUSEBUTTONUP)
            pos = pygame.mouse.get_pos()
            if ((pos[0]-x)**2+(pos[1]-y)**2 <= r**2) \
            or ((pos[0]-x1)**2/(a**2)+(pos[1]-y1)**2/(b**2) <= 1):
                count += 1
    
    new_ball()
    new_ellipse()
    pygame.display.update()

    screen.fill(BLACK)
    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 20)
    text_surface = my_font.render(f'Count: {count}', True, RED)
    screen.blit(text_surface, (0,0))

pygame.quit()
