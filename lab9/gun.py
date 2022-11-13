import pygame as pg
import numpy as np
from pygame.draw import *
from random import randint
from random import choice

FPS = 30

RED = 0xFF4500
BLUE = 0x00FFFF
VARYELLOW = 0xFFC91F
GREEN = 0x00FA9A
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = (192, 192, 192)
VARGREY=(105, 105, 105)
GAME_COLORS = [RED, BLUE, VARYELLOW, GREEN, MAGENTA, CYAN]

YELLOW = 0xffff00
VARGREEN2 = 0x228B22
VARGREEN1 = 0x9ACD32
VARBLACK = [75, 0, 130]
VARPING = 0xFF69B4
PURPLE = [128, 0, 128]

ORANGERED = [255, 69, 0]
ORANGE = [255, 165, 0]
Gold=[255, 215, 0]
Crimson = [220, 20, 60]
Salmon=(250, 128, 114)
HotPink=[255, 105, 180]
MediumVioletRed=(199, 21, 133)
GreenYellow=[173, 255, 47]
MediumSpringGreen = [127, 255, 212]
Aquamarine=(127, 255, 212)

VARCOLORS = [ORANGERED, ORANGE,Gold,Crimson,Salmon,HotPink,MediumVioletRed,GreenYellow,MediumSpringGreen,Aquamarine]
YKRAINE=[BLUE,YELLOW]

OX = 800
OY = 600


def turn(point, ang):
    t = np.dot(np.array(point), np.array(
        [[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]]))
    return t


class Ball:
    def __init__(self, x=60, y=450, vx=10, vy=10, r=10,colors=VARCOLORS):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали"""
        self.screen = screen
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = choice(colors)
        self.live = 30
        self.count = 1
        self.width = r

    def move(self, dt):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600)."""
        self.x += self.vx * dt
        self.y += self.vy * dt

    def stop(self, dt):
        if self.y + self.vy * dt >= 500:
            self.vy = 0
            self.y = 500

    def boost(self, g, dt):
        self.vy += g * dt

    def draw(self):
        circle(self.screen,
               self.color,
               (self.x, self.y),
               self.r)

    def draw_away(self):
        circle(self.screen, self.color, (self.x, self.y),
               self.r, int(round(self.width, 0)))
        self.width -= self.r/30

    def collision(self, dt, delta = 0.5):
        if not (OX - self.r > self.x + self.vx * dt > self.r):
            self.count += delta
            self.vx = - self.vx/self.count
        if not (500 - self.r > self.y + self.vy * dt > self.r):
            self.count += delta
            self.vy = - self.vy/self.count

    def hittest(self, obj):
        '''(obj.x-self.x)**2+(obj.y-selfy)**2 <= r**2
        Args:   obj: Обьект, с которым проверяется столкновение.
        Returns:    Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.'''
        return (obj.x-self.x)**2+(obj.y-self.y)**2 <= obj.r**2 + self.r**2

    def hittest_gun(self, obj, r=10, h=70, base1=90, base2=30):
        if ( -45 < self.x-obj.x < 32) and (0 < self.y-obj.y < h+r):
            return True


class Gun:
    def __init__(self, screen, surface, x=60, y=460, COLOR=GREY):
        self.screen = screen
        self.surface = surface
        self.x = x
        self.y = y
        self.a = 0
        self.color = COLOR
        self.f2_power = 30
        self.f2_on = 0
        self.shift = True

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        gun_l = self.f2_power
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.x + 5 + turn([gun_l + 15, 0], self.a)[0], self.y + 12 + turn([gun_l + 15, 0], self.a)[1])
        new_ball.r += 5
        self.a = - \
            np.arctan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * np.cos(self.a)
        new_ball.vy = - self.f2_power * np.sin(self.a)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 30

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.a = - np.arctan2((event.pos[1]-self.y), (event.pos[0]-self.x))

    def draw(self):
        gun_w = 10
        gun_l = self.f2_power

        p1 = np.array([self.x + 5, self.y + 12]) + turn([0, 0.5 * gun_w], self.a)
        p2 = np.array([self.x + 5, self.y + 12]) + turn([gun_l, 0.5 * gun_w], self.a)
        p3 = np.array([self.x + 5, self.y + 12]) + turn([gun_l, - 0.5 * gun_w], self.a)
        p4 = np.array([self.x + 5, self.y + 12]) + turn([0, - 0.5 * gun_w], self.a)

        pg.draw.polygon(self.screen, self.color, [p1, p2, p3, p4])

        if self.shift:
            pg.draw.line(self.screen, VARGREY, p2+(p3-p2)*1/4, p1+(p4-p1)*1/4, round(gun_w/4))
            pg.draw.line(self.screen, VARGREY, p2+(p3-p2)*3/4, p1+(p4-p1)*3/4, round(gun_w/4))
        else:
            pg.draw.line(self.screen, VARGREY, p2+(p3-p2)*2/4, p1+(p4-p1)*2/4, round(gun_w/4))
            pg.draw.line(self.screen, VARGREY, p2+(p3-p2)*4/4, p1+(p4-p1)*4/4, round(gun_w/4))

        pg.draw.circle(self.screen, [139, 0, 0], [self.x + 5, self.y + 12], 5)

    def draw_body(self, r=10, h=50, base1=110, color_body=VARGREEN1):
        base = np.array([self.x, self.y])
        self.surface.fill([240, 255, 255])
        pg.draw.circle(self.surface, BLUE, [70, 28], 18)
        pg.draw.circle(self.surface, [0, 0, 255], [70, 28], 18, 2)
        pg.draw.polygon(self.surface, [240, 255, 255], [
            [50, 10],
            [70, 10],
            [70, 46],
            [50, 46]
        ])
        pg.draw.polygon(self.surface, VARPING, [
            [50, 10],
            [70, 10],
            [70, 20],
            [50, 20]
        ])
        pg.draw.polygon(self.surface, [139, 0, 0], [
            [50, 10],
            [70, 10],
            [70, 20],
            [50, 20]
        ],2)
        pg.draw.polygon(self.surface, VARPING, [
            [50, 10],
            [50, 46],
            [9, 25]
        ])
        pg.draw.polygon(self.surface, VARPING, [
            [70, 30],
            [86, 30],
            [86, 26],
            [70, 26]
        ])
        if self.shift:
            col1 = "BLUE"
            col2 = "YELLOW"
            self.shift = False
        else:
            col1 = "YELLOW"
            col2 = "BLUE"
            self.shift = True
        pg.draw.polygon(self.surface, col1, [
            [10, 0],
            [10, 5],
            [60, 5],
            [60, 3]
        ])
        pg.draw.polygon(self.surface, col2, [
            [110, 0],
            [110, 5],
            [60, 5],
            [60, 3]
        ])
        pg.draw.polygon(self.surface, YELLOW, [
            [32, 28],
            [50, 28],
            [50, 21],
            [32, 21]
        ])
        pg.draw.polygon(self.surface, [0, 0, 255], [
            [32, 35],
            [50, 35],
            [50, 28],
            [32, 28]
        ])
        pg.draw.polygon(self.surface, [139, 0, 0], [
            [50, 10],
            [70, 10],
            [70, 46],
            [50, 46]
        ],2)

        pg.draw.line(self.surface, [139, 0, 0], [55, 44], [55, 50], 2)
        pg.draw.line(self.surface, [139, 0, 0], [65, 44], [65, 50], 2)
        pg.draw.line(self.surface, [139, 0, 0], [40, 50], [80, 50], 2)
        pg.draw.line(self.surface, VARBLACK, [60, 10], [60, 5], 2)
        pg.draw.circle(self.surface, HotPink, [9, 23], 9)
        #pg.draw.circle(self.surface, [139, 0, 0], [9, 23], 9,2)
        pg.draw.circle(self.surface, [139, 0, 0], [9, 23], 2)

        pg.draw.polygon(self.surface, col1, [
            [0, 25],
            [18, 21],
            [18, 25],
            [0, 21]
        ])
        pg.draw.polygon(self.surface, col2, [
            [7, 14],
            [11, 32],
            [7, 32],
            [11, 14]
        ])
        screen.blit(self.surface, [self.x - 55, self.y - 25])

    def vardraw_body(self, r=10, h=30, base1=90, base2=30, color_tank=VARGREEN1):
        base = np.array([self.x, self.y])
        varbase = np.array([self.x, self.y, 0, 0])

        p1 = np.array([-3/5*base1, h])+base
        p2 = np.array([2/5*base1, h])+base
        p3 = np.array([2/5*base2, 0])+base
        p4 = np.array([-3/5*base2, 0])+base

        pg.draw.polygon(self.screen, color_tank, [p1, p2, p3, p4])

        pg.draw.circle(self.screen, VARBLACK, (self.x, self.y), r)

        center1 = np.array([3/10*base1, h])+base
        center2 = np.array([-6/10*base1, h])+base
        center3 = np.array([-15/100*base1, h])+base
        point = [center1, center2, center3]

        for i in point:
            pg.draw.circle(self.screen, VARGREEN2, i, r)
            pg.draw.circle(self.screen, VARBLACK, i, r, int(r/5))
            pg.draw.circle(self.screen, VARBLACK, i, int(r/5))

        lin1 = np.array([-6/10*base1, h+r-2])+base
        lin2 = np.array([-6/10*base1, h-r+2])+base
        lin3 = np.array([-7/10*base1, h-r-6])+base

        pg.draw.rect(self.screen, VARBLACK, [lin1, [int(9/10*base1), 2]])
        pg.draw.rect(self.screen, VARBLACK, [lin2, [int(9/10*base1), 2]])

        pg.draw.rect(self.screen, VARBLACK, [lin3, [int(12/10*base1), 6]])

    def move_body(self, step=2):
        keys = pg.key.get_pressed()
        if self.x == 600:
            self.x = 50
        if self.y <= 100:
            self.y = 500
        if keys[pg.K_d] and (self.x <= 600):
            self.x += step
        if keys[pg.K_a] and (55 <= self.x):
            self.x -= step
        if keys[pg.K_w] and (40 <= self.y):
            self.y -= step
        if keys[pg.K_s] and (self.y < 500-40):
            self.y += step

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 80:
                self.f2_power += 1
        else:
            self.color = GREY

    def new_coords(self):
        self.x = 60
        self.y = randint(200, 460)


class Target:
    def __init__(self, screen, cst = 2, vx_lim=(-10, 10), vy_lim=(-10, 10)):
        self.screen = screen
        self.a = 1
        self.color = GAME_COLORS[randint(0, len(GAME_COLORS)-1)]
        self.points = 0
        self.cost = cst
        self.live = 1
        self.vy = randint(vy_lim[0], vy_lim[1])
        self.vx = randint(vx_lim[0], vx_lim[1])
        self.new_target()

    def new_target(self, vx_lim=(-10, 10), vy_lim=(-10, 10)):
        """ Инициализация новой цели. """
        self.x = randint(600, 780)
        self.y = randint(10, 450)
        self.r = randint(20, 40)
        self.vy = randint(vy_lim[0], vy_lim[1])
        self.vx = randint(vx_lim[0], vx_lim[1])
        self.color = GAME_COLORS[randint(0, len(GAME_COLORS)-1)]

    def change_color(self):
        self.color = GAME_COLORS[randint(0, len(GAME_COLORS)-1)]

    def hit(self):
        """Попадание шарика в цель."""
        self.points += self.cost

    def move(self, dt):
        """Переместить мяч по прошествии единицы времени.
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600)."""
        self.x += self.vx * dt
        self.y += self.vy * dt

    def boost(self, g, dt):
        self.vy += g * dt
        self.vx += g * dt

    def create_text(self):
        global txt
        txt += [Text(self.x, self.y, self.cost)]

    def draw(self):
        circle(self.screen, self.color, (self.x, self.y), self.r)

    def correction(self, vx_lim=(-10, 10), vy_lim=(-10, 10)):
        if self.vx >= 20 or self.vx <= -20:
            self.vx = randint(vx_lim[0], vx_lim[1])
        if self.vy >= 20 or self.vy <= -20:
            self.vy = randint(vy_lim[0], vy_lim[1])

    def collision(self, dt):
        if self.x + self.vx * dt > 780 - self.r and self.vx > 0:
            self.vx = - self.vx
        if self.x + self.vx * dt < 600 + self.r and self.vx < 0:
            self.vx = - self.vx
        if self.y + self.vy * dt > 450 - self.r and self.vy > 0:
            self.vy = - self.vy
        if self.y + self.vy * dt < 0 + self.r and self.vy < 0:
            self.vy = - self.vy


class bomb:
    def __init__(self,colors=YKRAINE):
        self.x = randint(5, 600)
        self.y = randint(5, 300)
        self.vx = randint(10, 20)
        self.vy = 0
        self.colors=colors
        self.r = randint(20, 30)
        self.count = randint(0, 30)

    def move(self, dt):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600)."""
        self.x += self.vx * dt

    def collision(self, dt):
        if self.x + self.vx*dt >= 600:
            self.x = 5
        if self.x+self.vx * dt <= 0:
            self.x = 595

    def draw(self, rise=1):
        base = np.array([self.x, self.y])
        rise = 2  # (200, 175)
        r = np.array([100, 5, 30, 20, 15, 10])/rise
        beg = np.array([[-50, -25], [50, -25]])/rise+base
        width = np.array([25, 15, 5])/rise
        coord = np.array([[-7, -40], [-115, -101], [32, -43],
                         [106, -85], [-38, 59], [29, 59]])/rise+base
        coord = np.around(coord).astype(int)
        width = np.around(width).astype(int)

        color=self.colors[randint(0,len(self.colors)-1)]
        circle(screen, color, base, r[0])
        circle(screen, (0, 0, 0), base, r[0], width[2])

        circle(screen, (255, 0, 255), beg[0], r[2])
        circle(screen, (255, 0, 255), beg[1], r[3])
        circle(screen, (25, 25, 112), beg[0], r[2], width[2])
        circle(screen, (25, 25, 112), beg[1], r[3], width[2])

        circle(screen, (25, 25, 112), beg[1], r[5])
        circle(screen, (25, 25, 112), beg[0], r[4])

        polygon(screen, (0, 0, 255), [coord[0], coord[1]], width[0])
        polygon(screen, (0, 0, 255), [coord[2], coord[3]], width[1])
        polygon(screen, (0, 0, 255), [coord[4], coord[5]], width[0])

    def fire(self):
        if self.count == 0:
            global ball2
            ball2 += [Ball(self.x, self.y, 0, randint(10, 20), 10, ['RED'])]

    def cunt(self):
        if self.count == 30:
            self.count = 0
        else:
            self.count += 1


class Land:
    def __init__(self, N=10):
        self.width = OX
        self.y = 500
        self.h = OY/6/N
        self.zero = 0
        self.colors = [VARPING, VARPING, BLUE,  BLUE, YELLOW, YELLOW]

    def draw(self):
        for i in range(int((OY-500)/self.h)):
            ind = (i+self.zero) % 6
            coord = np.array([0, self.h*i])+np.array([0, 500])
            pg.draw.rect(screen, self.colors[ind], [
                         coord, [self.width, self.h]])

    def shift(self):
        keys = pg.key.get_pressed()
        if (keys[pg.K_d] or keys[pg.K_s]) or (keys[pg.K_a] or keys[pg.K_w]):
            self.zero += 1
        else:
            self.zero = 0


class Text:
    def __init__(self, x, y, cst=4):
        self.live = 15
        self.y = y
        self.x = x
        self.cost = cst
        self.colors = PURPLE

    def draw_text(self):
        font = pg.font.SysFont('Comic Sans MS', 30)
        label = font.render(f'+{self.cost}', True, self.colors)
        screen.blit(label, [self.x, self.y])

class Cursor:
    def __init__(self, x = 0, y = 0):
        self.y = y
        self.x = x

    def cursor_change_pos(self, event):
        self.x,self.y=event.pos[0],event.pos[1]

    def draw_cursor(self, r = 10):
        center=np.array([self.x,self.y])
        circle(screen, Crimson, center, r, round(r/5))
        circle(screen, BLACK, center, 2)

        p1,p2=np.array([r/2,0])+center, np.array([1.5*r,0])+center
        pg.draw.line(screen, Crimson, p1, p2, 3)

        c1,c2=np.array([-r/2,0])+center, np.array([-1.5*r,0])+center
        pg.draw.line(screen, Crimson, c1, c2, 3)

        b1,b2=np.array([0,r/2])+center, np.array([0,1.5*r])+center
        pg.draw.line(screen, Crimson, b1, b2, 3)

        d1,d2=np.array([0,-r/2])+center, np.array([0,-1.5*r])+center
        pg.draw.line(screen, Crimson, d1, d2, 3)


def display_text(sum_points):
    '''функция выводит базовые надписи на экран'''
    if not (sum_points):
        font1 = pg.font.SysFont('Comic Sans MS', 100)
        label11 = font1.render(f'Hit this fucking', True, PURPLE)
        label12 = font1.render(f'target', True, PURPLE)
        screen.blit(label11, [50, OY/2-100])
        screen.blit(label12, [OX/2-120, OY/2])

    if sum_points:
        font2 = pg.font.SysFont('Comic Sans MS', 30)
        label2 = font2.render(f'Count: {sum_points}', True, [255, 20, 147])
        screen.blit(label2, [0, 0])

    if sum_points < 0:
        font3 = pg.font.SysFont('Comic Sans MS', 70)
        label3 = font3.render(f'U are fck Loser LOL', True, PURPLE)
        screen.blit(label3, [60, 0])


def sum(target):
    s = 0
    for t in target:
        s += t.points
    return s

pg.init()
screen = pg.display.set_mode((OX, OY))
body_surface = pg.surface.Surface([110, 55])
bullet, g, dt = 0, 1, 1
N, N_bomb = 2, 5
balls, target, bimb, ball2, txt = [], [], [], [], []

clock = pg.time.Clock()
gun = Gun(screen, body_surface)
lnd = Land()
curs=Cursor()

finished = False
index = False

pg.display.set_caption("Gun")

pg.mixer.music.load("lab9/Helicopter.mp3")
pg.mixer.music.play(-1)
flPause = False
vol=1.0

for i in range(N):
    target += [Target(screen, 1)]

for i in range(N_bomb):
    bimb += [bomb()]
    
pg.mouse.set_visible(False)

while not finished:
    screen.fill([240, 255, 255])
    clock.tick(FPS)
    lnd.shift()
    lnd.draw()
    

    gun.draw_body()
    gun.draw()
    gun.move_body(10)

    for bo in bimb:
        bo.draw()
        bo.move(dt)
        bo.collision(dt)
        bo.fire()
        bo.cunt()

    for i in txt:
        if i.live > 0:
            i.draw_text()
            i.live -= 0.5
        else:
            txt.remove(i)

    for b in ball2:
        if b.live > 0:
            b.draw()
            b.move(dt)
            b.live -= 0.25
            if b.hittest_gun(gun):
                gun.new_coords()
                target[0].points -= 5
                ball2.remove(b)
        else:
            ball2.remove(b)

    display_text(sum(target))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pg.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pg.MOUSEMOTION:
            gun.targetting(event)
            curs.cursor_change_pos(event)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                flPause = not flPause
                if flPause:
                    pg.mixer.music.pause()
                else:
                    pg.mixer.music.unpause()
            elif event.key == pg.K_LEFT:
                    vol -= 0.1
                    pg.mixer.music.set_volume(vol)
                    print( pg.mixer.music.get_volume() )
            elif event.key == pg.K_RIGHT:
                vol += 0.1
                pg.mixer.music.set_volume(vol)
                print( pg.mixer.music.get_volume() )

    
    for b in balls:
        b.draw()
        b.stop(dt)
        b.move(dt)
        b.boost(g, dt)
        b.collision(dt)
        b.live -= 0.25
    
    for t in target:
        t.draw()
        t.collision(dt)
        t.correction()
        t.move(dt)
        t.boost(g/4, dt)
        t.change_color()
        t.draw()


    for t in target:
        hit_n = False
        for b in balls:
            if b.live > 0:
                if b.hittest(t) and t.live:
                    b.live = 0
                    hit_n = True       
            elif b.width > 0:
                b.draw_away()
            else:
                balls.remove(b)
        if hit_n:
            t.hit()
            t.create_text()
            t.new_target()

    curs.draw_cursor()
    gun.power_up()
    pg.font.init()
    pg.display.update()


pg.quit()
