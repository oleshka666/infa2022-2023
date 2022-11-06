import pygame
from pygame.draw import *
from random import randint
pygame.init()

#параметры системы
FPS = 60
Oy=900
Ox=1200
screen = pygame.display.set_mode((Ox, Oy))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

#создаем шарик
class Ball:
    def __init__(self, x_lim=(100, 1100), y_lim=(100, 900), vx_lim=(-10, 10), vy_lim=(-10, 10), r_lim=(50, 100), colors=COLORS, cost=1):
        self.cost=cost
        self.x = randint(x_lim[0], x_lim[1])
        self.y = randint(y_lim[0], y_lim[1])
        self.a = randint(r_lim[0], r_lim[1])
        self.b = self.a
        self.vy = randint(vy_lim[0], vy_lim[1])
        self.vx = randint(vx_lim[0], vx_lim[1])
        self.color = colors[randint(0, len(colors) - 1)]

    def render(self, surface):
        circle(surface, self.color, (self.x, self.y), self.a)

    def boost(self,f,g,t,j):
        pass

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def collision(self,dt):
        if not(Ox - self.a > self.x + self.vx * dt > self.a):
            self.vx = - self.vx
        if not(Oy - self.a > self.y + self.vy * dt > self.a):
            self.vy = - self.vy

#создаем еллипс
class Ellipse:
    def __init__(self, x_lim=(100, 1100), y_lim=(100, 900), vx_lim=(-10, 10), vy_lim=(-10, 10), r_lim=(50, 100), colors=COLORS, cost=1):
        self.cost = cost
        self.x = randint(x_lim[0], x_lim[1])
        self.y = randint(y_lim[0], y_lim[1])
        self.a = randint(r_lim[0], r_lim[1])
        self.b = randint(r_lim[0], r_lim[1])
        self.vy = randint(vy_lim[0], vy_lim[1])
        self.vx = randint(vx_lim[0], vx_lim[1])
        self.color = colors[randint(0, len(colors) - 1)]

    def render(self, surface):
        ellipse(surface, self.color, (self.x, self.y, self.a, self.b))

    def boost(self,dt,g,x0=0,y0=0):
        self.vy += g * dt

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def collision(self,dt):
        indicator=True
        if not(Ox - self.a > self.x + self.vx * dt > self.a) and indicator:
            self.vx = - self.vx
            self.a, self.b = self.b, self.a
            indicator = False
        if not(Oy - self.b > self.y + self.vy * dt > self.b) and indicator:
            self.vy = - self.vy
            self.a, self.b = self.b, self.a
            indicator = False

#делаем уникальный шарик
class unicue:
    def __init__(self, x_lim=(200, 1000), y_lim=(200, 700), vx_lim=(-5, 5), vy_lim=(-5, 5), r_lim=(50, 200), colors=COLORS,cost_lim=(5,10)):
        self.cost=randint(cost_lim[0], cost_lim[1])
        self.x = randint(x_lim[0], x_lim[1])
        self.y = randint(y_lim[0], y_lim[1])
        self.a = randint(r_lim[0], r_lim[1])
        self.b = randint(r_lim[0], r_lim[1])
        self.vy = randint(vy_lim[0], vy_lim[1])
        self.vx = randint(vx_lim[0], vx_lim[1])
        self.color = colors[randint(0, len(colors) - 1)]

    def render(self, surface):
        ellipse(surface, self.color, (self.x, self.y, self.a, self.b))
    
    def boost(self,dt,a=0,x0=0,y0=0):
        a=1000
        x0=Ox/2
        y0=Oy/2
        r=(self.x-x0)**2+(self.y-y0)**2
        self.vx -= a * r**(-3/2) *(self.x-x0) * dt
        self.vy -= a * r**(-3/2) *(self.y-y0) * dt

    def change(self,r_lim=(50, 200), colors=COLORS):
        self.color = colors[randint(0, len(colors) - 1)]
        self.a = randint(r_lim[0], r_lim[1])
        self.b = randint(r_lim[0], r_lim[1])

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def collision(self,dt):
        if not(Ox - self.a > self.x + self.vx * dt > self.a):
            self.vx = - self.vx
        if not(Oy - self.b > self.y + self.vy * dt > self.b):
            self.vy = - self.vy

#создаем массив фигур
N,fig=4,[unicue()]
for i in range(1,N):
    S = randint(0,1)
    if S ==1:
        fig += [Ellipse()]
    else:
        fig += [Ball()]
ell1=Ellipse()
ball2=Ball()
ball1=Ball()


clock = pygame.time.Clock()
finished = False

pygame.display.set_caption("My program")
font1 = pygame.font.SysFont('Comic Sans MS', 100)
font2 = pygame.font.SysFont('Comic Sans MS', 30)

dt=1
g=1
count = 0
none_clicked = True

while not finished:
    clock.tick(FPS)

    for event in pygame.event.get():
        '''if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos)'''
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i in range(N):
                if (pos[0]-fig[i].x)**2/(fig[i].a**2)+(fig[i].y-pos[1])**2/(fig[i].b**2) <= 1:
                    count += fig[i].cost
                    if i==0:
                        fig[i]=unicue()
                    else:
                        S = randint(0,1)
                        if S == 1:
                            fig[i] = Ellipse()
                        else:
                            fig[i] = Ball()
           
    for i in range(N):
        if i == 0:
            fig[i].change()
        fig[i].move(dt)
        fig[i].boost(dt,g,Ox/2,Oy/2)
        fig[i].render(screen)
        fig[i].collision(dt)



    label1=font1.render(f'Catch this fucking ball', True, 'WHITE')
    if count == 0:
        screen.blit(label1, [80,Oy/2-100])

    label2 = font2.render(f'Count: {count}', True, RED)
    if count != 0:
        screen.blit(label2, [0,0])

    pygame.display.update()
    screen.fill(BLACK)
    pygame.font.init()

pygame.quit()
