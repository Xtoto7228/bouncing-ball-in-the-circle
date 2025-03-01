import time as pyt
import math as mt
from pygame import*

init()

clock = time.Clock()
fps = 60


'''MAIN COLORS'''
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
lime = 0, 255, 0
blue = 0, 0, 255
yellow = 255, 255, 0
cyan = 0, 255, 255
magenta = 255, 0, 255
gray = 128, 128, 128
darkgray = 40, 40, 40
lightgray = 211, 211, 211
orange = 255, 165, 0
green = 0, 128, 0
darkgreen = 0, 100, 0
purple = 128, 0, 128

'''Main window'''
window = display.set_mode((0, 0), FULLSCREEN)
display.set_caption('BOUNCING BALL')
window.fill(black)



class Ball(sprite.Sprite):
    def __init__(self, x, y, ball_radius, speed, gravity):
        self.x = x
        self.y = y
        self.radius = ball_radius
        self.gravity = gravity
        self.speed = speed

    def reset(self):
        draw.circle(window, white, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.speed
        self.y += (self.speed+self.gravity)
    
    def bounce(self, circle_x, circle_y, radius, inner_radius):
        dx = self.x - circle_x
        dy = self.y - circle_y
        distance = (dx**2 + dy**2) ** 0.5

        if distance + self.radius > radius:
            self.speed *= -1
        elif distance - self.radius < inner_radius:
            self.speed *= -1
    
    def update(self):
        self.move()
        self.reset()
    

class Circle(sprite.Sprite):
    def __init__(self, circle_x, circle_y, speed, radius, inner_radius, width, height):
        super().__init__()
        self.x = circle_x
        self.y = circle_y
        self.speed = speed
        self.radius = radius
        self.inner_radius = inner_radius
        self.color = red
        self.width = width
        self.height = height
        self.angle = 0
        self.line = 100
        


    def reset(self):
        draw.circle(window, red, (self.x, self.y), self.radius, 3)
        draw.circle(window, black, (self.x, self.y), self.inner_radius)

        '''Fucking coordinats of fucking line'''
        start_x = self.x + self.radius * mt.cos(mt.radians(self.angle))
        start_y = self.y + self.radius * mt.sin(mt.radians(self.angle))
        end_x = self.x + self.inner_radius * mt.cos(mt.radians(self.angle))
        end_y = self.y + self.inner_radius * mt.sin(mt.radians(self.angle))

        draw.line(window, black, (start_x, start_y), (end_x, end_y), self.line)

    def rotate(self):
        self.angle += self.speed
        self.angle %= 360

    def update(self):
        self.rotate()
        self.reset()

        

circle1 = Circle(700, 700, 1, 200, 100,  500, 500)
ball = Ball(750, 750, 5, 2, 1)

game = True
while game:
    circle1.update()
    ball.update()
    ball.bounce(circle1.x, circle1.y, circle1.radius, circle1.inner_radius)

    
    for e in event.get():
        if e.type == QUIT:
            game = False
    

    display.update()
    clock.tick(fps)