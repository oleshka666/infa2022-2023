import pygame
import numpy as np
from pygame.draw import *
from random import randint
import math
from random import choice

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450, ):
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

    def move(self, dt):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        self.x += self.vx * dt
        self.y += self.vy * dt
    
    def stop(self,dt):
        if self.y+self.vy * dt >= 500:
            self.vy = 0
            self.y = 500

    def boost(self,g,dt):
        self.vy += g * dt
    
    def draw(self):
        circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        '''
        (obj.x-self.x)**2+(obj.y-selfy)**2 <= r**2
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        '''

        return (obj.x-self.x)**2+(obj.y-self.y)**2 <= obj.r**2 + self.r**2


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.a = 1
        self.color = GREY
        self.targ=[(10,450),(60,450),(60,430),(10,430)]

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.a = np.arctan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * np.cos(self.a)
        new_ball.vy = self.f2_power * np.sin(self.a)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.a = np.arctan2((event.pos[1]-450) , (event.pos[0]-20))
            #rot=[50*np.cos(a)-20*np.sin(a),50*np.sin(a)+20*np.cos(a)]
            #self.te

        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        polygon(self.screen, self.color, self.targ)
        #rect(self.screen, self.color, [10,460,10,40])


    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.a = 1
        self.color = GREY
        self.points = 0
        self.live = 1
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(2, 50)
        self.color = RED

    def hit(self, point=1):
        """Попадание шарика в цель."""
        self.points += point

    def draw(self):
        circle(self.screen, self.color, (self.x,self.y), self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet,g,dt = 0,1,1
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()

    for b in balls:
        b.draw()
    
    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
 

    for b in balls:
        b.stop(dt)
        b.move(dt)
        b.boost(g, dt)
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
            target.draw()
    gun.power_up()
    pygame.font.init()


pygame.quit()
