import pygame as pg
from pygame.draw import *
from random import randint
pg.init()

# параметры системы
FPS = 60
Oy = 900
Ox = 1200
screen = pg.display.set_mode((Ox, Oy))

RED = (255, 0, 0)
AQUA = (0, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PINK = (255, 0, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
COLORS = [RED, AQUA, YELLOW, GREEN, PINK, BLUE]
COLORSYCRAINE = [[0, 0, 255], [255, 255, 0]]

ORANGERED = [255, 69, 0]
ORANGE = [255, 165, 0]
Gold = [255, 215, 0]
Crimson = [220, 20, 60]
Salmon = (250, 128, 114)
HotPink = [255, 105, 180]
MediumVioletRed = (199, 21, 133)
GreenYellow = [173, 255, 47]
MediumSpringGreen = [127, 255, 212]

VARCOLORS = [ORANGERED, ORANGE, Gold, Crimson, Salmon,
             HotPink, MediumVioletRed, GreenYellow, MediumSpringGreen]

fill = [255, 0, 255]

# создаем еллипс


class Ellipse:
    def __init__(self, gravity=1, x_lim=(100, 1000), y_lim=(100, 800), vx_lim=(-10, 10), vy_lim=(-10, 10), r_lim=(70, 120), colors=VARCOLORS, cost=1):
        self.cost = cost
        self.x = randint(x_lim[0], x_lim[1])
        self.y = randint(y_lim[0], y_lim[1])
        self.a = randint(r_lim[0], r_lim[1])
        self.b = randint(r_lim[0], r_lim[1])
        self.vy = randint(vy_lim[0], vy_lim[1])
        self.vx = randint(vx_lim[0], vx_lim[1])
        self.color = colors[randint(0, len(colors) - 1)]
        self.gravity = gravity

    def render(self, surface):
        ellipse(surface, self.color, (self.x, self.y, self.a, self.b))

    def boost(self, dt, g):
        self.vy += g * dt

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def collision(self, dt):
        if Ox - self.a < self.x + self.vx * dt and self.vx > 0:
            self.vx = - self.vx
            self.a, self.b = self.b, self.a
        if self.a > self.x + self.vx * dt and self.vx < 0:
            self.vx = - self.vx
            self.a, self.b = self.b, self.a
        if Oy - self.b < self.y + self.vy * dt > self.b and self.vy > 0:
            self.vy = - self.vy
            self.a, self.b = self.b, self.a
        if self.y + self.vy * dt < self.b and self.vy < 0:
            self.vy = - self.vy
            self.a, self.b = self.b, self.a

    def correction(self, vx_lim=(-10, 10), vy_lim=(-10, 10)):
        if self.vx >= 40 or self.vx <= -40:
            self.vx = randint(vx_lim[0], vx_lim[1])
        if self.vy >= 40 or self.vy <= -40:
            self.vy = randint(vy_lim[0], vy_lim[1])

    def hittest(self, event):
        return (event.pos[0]-self.x)**2/(self.a**2)+(self.y-event.pos[1])**2/(self.b**2) <= 1

# делаем уникальный шарик


class Unique:
    def __init__(self, x_lim=(200, 1000), y_lim=(200, 700), vx_lim=(-5, 5), vy_lim=(-5, 5), r_lim=(50, 200), colors=COLORS, cost_lim=(5, 10)):
        self.cost = randint(cost_lim[0], cost_lim[1])
        self.x = randint(x_lim[0], x_lim[1])
        self.y = randint(y_lim[0], y_lim[1])
        self.a = randint(r_lim[0], r_lim[1])
        self.b = randint(r_lim[0], r_lim[1])
        self.vy = randint(vy_lim[0], vy_lim[1])
        self.vx = randint(vx_lim[0], vx_lim[1])
        self.color = colors[randint(0, len(colors) - 1)]
        self.gravity = 1

    def render(self, surface):
        ellipse(surface, self.color, (self.x, self.y, self.a, self.b))

    def boost(self, dt, g):
        self.vy += g * dt
        self.vx += g * dt

    def change(self, r_lim=(50, 200), colors=COLORS):
        self.color = colors[randint(0, len(colors) - 1)]
        self.a = randint(r_lim[0], r_lim[1])
        self.b = randint(r_lim[0], r_lim[1])

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def collision(self, dt):
        if Ox - self.a < self.x + self.vx * dt and self.vx > 0:
            self.vx = - self.vx
        if self.a > self.x + self.vx * dt and self.vx < 0:
            self.vx = - self.vx
        if Oy - self.b < self.y + self.vy * dt > self.b and self.vy > 0:
            self.vy = - self.vy
        if self.y + self.vy * dt < self.b and self.vy < 0:
            self.vy = - self.vy

    def correction(self, vx_lim=(-20, 20), vy_lim=(-20, 20)):
        if self.vx >= 50 or self.vx <= -50:
            self.vx = randint(vx_lim[0], vx_lim[1])
        if self.vy >= 50 or self.vy <= -50:
            self.vy = randint(vy_lim[0], vy_lim[1])

    def hittest(self, event):
        if event:
            return (event.pos[0]-fig[i].x)**2/(fig[i].a**2)+(fig[i].y-event.pos[1])**2/(fig[i].b**2) <= 1


class Text:
    def __init__(self, x, y, cost):
        self.live = 15
        self.y = y
        self.x = x
        self.cost = cost
        self.color = BLACK

    def draw_text(self):
        font = pg.font.SysFont('Comic Sans MS', 30)
        label = font.render(f'+{self.cost}', True, self.color)
        screen.blit(label, [self.x, self.y])


N, fig = 10, [Unique()]
for i in range(1, N):
    S = randint(0, 1)
    fig += [Ellipse(S)]

clock = pg.time.Clock()
finished = False

pg.display.set_caption("My program")


def display_text(count):
    '''функция выводит базовые надписи на экран'''
    if count == 0:
        font1 = pg.font.SysFont('Comic Sans MS', 100)
        label1 = font1.render(f'Catch this fucking ball', True, fill)
        screen.blit(label1, [80, Oy/2-100])

    if count != 0:
        font2 = pg.font.SysFont('Comic Sans MS', 30)
        label2 = font2.render(f'Count: {count}', True, fill)
        screen.blit(label2, [0, 0])


dt, g, count, txt = 1, 1, 0, []

while not finished:
    screen.fill([240, 255, 255])
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            for i in range(N):
                if fig[i].hittest(event):
                    txt += [Text(fig[i].x, fig[i].y, fig[i].cost,)]
                    count += fig[i].cost
                    if i == 0:
                        fig[i] = Unique()
                    else:
                        S = randint(0, 1)
                        fig[i] = Ellipse(S)
    for i in txt:
        if i.live > 0:
            i.draw_text()
            i.live -= 0.5
        else:
            txt.remove(i)

    for i in range(N):
        if i == 0:
            fig[i].change()
        if fig[i].gravity:
            fig[i].move(dt)
            fig[i].boost(dt, g)
        else:
            fig[i].move(2*dt)
        fig[i].render(screen)
        fig[i].collision(dt)
        fig[i].correction()

    display_text(count)

    pg.display.update()
    pg.font.init()

pg.quit()
