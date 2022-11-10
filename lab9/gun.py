import pygame as pg
import numpy as np
from pygame.draw import *
from random import randint
from random import choice

FPS = 30

RED = 0xFF4500
BLUE = 0x00FFFF
YELLOW = 0xFFC91F
GREEN = 0x00FA9A
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

VARGREEN2=0x228B22
VARGREEN1=0x9ACD32
VARBLACK=0x4B0082
VARPING=0xFF69B4


OX = 800
OY = 600

def turn(point,ang):
    t=np.dot(np.array(point),np.array([[np.cos(ang),-np.sin(ang)],[np.sin(ang),np.cos(ang)]]))
    return t

class Ball:
    def __init__(self, screen: pg.Surface, x=60, y=450, ):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 10
        self.vy = 10
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.count = 1

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

    def collision(self, dt):
        if not (OX - self.r > self.x + self.vx * dt > self.r):
            self.count += 1
            self.vx = - self.vx/self.count
        if not (500 - self.r > self.y + self.vy * dt > self.r):
            self.count += 1
            self.vy = - self.vy/self.count

    def hittest(self, obj):
        '''(obj.x-self.x)**2+(obj.y-selfy)**2 <= r**2
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.'''
        #global bullet
        #font = pg.font.SysFont('Comic Sans MS', 30)
        #label = font.render(f'Вы уничтожили цель за {bullet} выстрелов', True, 'BLACK')
        #screen.blit(label, [50, OY/2-100])
        #bullet = 0
        return (obj.x-self.x)**2+(obj.y-self.y)**2 <= obj.r**2 + self.r**2


class Gun:
    def __init__(self, screen, x=60, y=450, COLOR=GREY):
        self.screen = screen
        self.x = x
        self.y = y
        self.a = 0
        self.color = COLOR
        self.f2_power = 30
        self.f2_on = 0

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen,self.x,self.y)
        new_ball.r += 5
        self.a = - np.arctan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * np.cos(self.a)
        new_ball.vy = - self.f2_power * np.sin(self.a)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 30

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.a = - np.arctan2((event.pos[1]-self.y), (event.pos[0]-self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        gun_w = 10
        gun_l=self.f2_power

        p1=np.array([self.x,self.y])
        p2=np.array([self.x,self.y]) + turn([gun_l,0],self.a)
        p3=np.array([self.x,self.y]) + turn([gun_l,-gun_w],self.a)
        p4=np.array([self.x,self.y]) + turn([0,-gun_w],self.a)

        pg.draw.polygon(self.screen, self.color, [p1,p2,p3,p4])
 
    def draw_body(self,r=10,h=30,base1=70,base2=30, color_tank=VARGREEN1):
        base=np.array([self.x,self.y])

        p1=np.array([-3/5*base1,h])+base
        p2=np.array([2/5*base1,h])+base
        p3=np.array([2/5*base2,0])+base
        p4=np.array([-3/5*base2,0])+base

        pg.draw.polygon(self.screen, color_tank, [p1,p2,p3,p4])

        pg.draw.circle(self.screen, VARBLACK, (self.x, self.y), r)

        center1=np.array([3/10*base1,h])+base
        center2=np.array([-6/10*base1,h])+base
        center3=np.array([-15/100*base1,h])+base
        point=[center1,center2,center3]

        for i in point:
            pg.draw.circle(self.screen, VARGREEN2, i, r)
            pg.draw.circle(self.screen, VARBLACK, i, r,int(r/5))
            pg.draw.circle(self.screen, VARBLACK, i, int(r/5))

        lin11=np.array([3/10*base1,h-r])+base
        lin12=np.array([-6/10*base1,h-r])+base

        lin21=np.array([3/10*base1,h+r])+base
        lin22=np.array([-6/10*base1,h+r])+base

        pg.draw.lines(self.screen, VARBLACK, False,[lin11, lin12])
        pg.draw.lines(self.screen, VARBLACK, False,[lin21, lin22])




    def move_body(self,step=2):
        keys=pg.key.get_pressed()
        if keys[pg.K_d] and (self.x < 600):
            self.x+=step
        if keys[pg.K_a] and (0 < self.x):
            self.x-=step
        if keys[pg.K_w] and (0 < self.y):
            self.y-=step
        if keys[pg.K_s] and (self.y < 500):
            self.y+=step
        if self.x==600:
            self.x=50



    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = VARPING
        else:
            self.color = VARBLACK

class Target:
    def __init__(self, screen, vx_lim=(-10, 10), vy_lim=(-10, 10)):
        self.screen = screen
        self.a = 1
        self.color = GAME_COLORS[randint(0, len(GAME_COLORS)-1)]
        self.points = 0
        self.live = 1
        self.vy = randint(vy_lim[0], vy_lim[1])
        self.vx = randint(vx_lim[0], vx_lim[1])
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(600, 780)
        self.y = randint(300, 500)
        self.r = randint(20, 40)
        self.color = GAME_COLORS[randint(0, len(GAME_COLORS)-1)]

    def change_color(self):
        self.color = GAME_COLORS[randint(0, len(GAME_COLORS)-1)]

    def hit(self, point=1):
        """Попадание шарика в цель."""
        self.points += point

    def move(self, dt):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600)."""
        self.x += self.vx * dt
        self.y += self.vy * dt

    def boost(self, g, dt):
        self.vy += g * dt
        self.vx += g * dt

    def draw(self):
        circle(self.screen, self.color, (self.x, self.y), self.r)

    def correction(self,vx_lim=(-10, 10), vy_lim=(-10, 10)):
        if self.vx >= 20 or self.vx <= -20:
            self.vx = randint(vx_lim[0], vx_lim[1])
        if self.vy >= 20 or self.vy <= -20:
            self.vy = randint(vy_lim[0], vy_lim[1])

    def collision(self, dt):
        if not (OX - self.r > self.x + self.vx * dt > self.r):
            self.vx = - self.vx
        if not (500 - self.r > self.y + self.vy * dt > self.r):
            self.vy = - self.vy


pg.init()
screen = pg.display.set_mode((OX, OY))
bullet, g, dt = 0, 1, 1
N = 2
balls, target = [], []

clock = pg.time.Clock()
gun = Gun(screen)

for i in range(N):
    target += [Target(screen)]

finished = False
index = False

pg.display.set_caption("Gun")
font1 = pg.font.SysFont('Comic Sans MS', 100)
font2 = pg.font.SysFont('Comic Sans MS', 30)

def display(sum_points):
    '''функция выводит базовые надписи на экран'''
    font1 = pg.font.SysFont('Comic Sans MS', 100)
    font2 = pg.font.SysFont('Comic Sans MS', 30)

    label11 = font1.render(f'Hit this fucking', True, 'BLACK')
    label12 = font1.render(f'target', True, 'BLACK')
    if not (sum_points):
        screen.blit(label11, [50, OY/2-100])
        screen.blit(label12, [OX/2-120, OY/2])

    label2 = font2.render(f'Count: {sum_points}', True, 'RED')
    if sum_points:
        screen.blit(label2, [0, 0])

def sum(target):
    s=0
    for t in target:
        s += t.points
    return s

while not finished:
    screen.fill([240, 255, 255])
    gun.draw_body()
    gun.draw()
    gun.move_body(3)

    for t in target:
        t.draw()
        t.change_color()

    for b in balls:
        b.draw()

    sum0=sum(target)
    display(sum0)

    pg.display.update()
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True    
        elif event.type == pg.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pg.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pg.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        if b.live > 0:
            b.stop(dt)
            b.move(dt)
            b.boost(g, dt)
            b.collision(dt)
            b.live -= 0.1
        for t in target:
            t.collision(dt)
            t.correction()
            t.move(dt/len(balls))
            t.boost(g/4, dt/len(balls))
            if b.hittest(t) and t.live:
                b.live = 0
                t.hit()
                t.new_target()
                t.draw()

    balls = [i for i in balls if b.live > 0]

    gun.power_up()
    pg.font.init()


pg.quit()
