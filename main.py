import pygame
import random
import math as mt
from pygame import *


pygame.init()

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
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

'''Main window'''
window = display.set_mode((1400, 1000))
display.set_caption('Ball')

class Ball:
    def __init__(self, x, y, radius, speed_x, speed_y, gravity=0.2):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.gravity = gravity
        self.elasticity = 0.8
        
    def update(self, circle):
        self.speed_y += self.gravity
        self.x += self.speed_x
        self.y += self.speed_y
        
        dx = self.x - circle.x
        dy = self.y - circle.y
        distance = mt.sqrt(dx**2 + dy**2)
        
        if distance > (circle.radius - self.radius):
            nx = dx / distance
            ny = dy / distance
            self.x = circle.x + nx * (circle.radius - self.radius)
            self.y = circle.y + ny * (circle.radius - self.radius)
            dot_product = self.speed_x * nx + self.speed_y * ny
            self.speed_x = self.elasticity * (self.speed_x - 2 * dot_product * nx)
            self.speed_y = self.elasticity * (self.speed_y - 2 * dot_product * ny)
    
    def draw(self, surface):
        pygame.draw.circle(surface, white, (int(self.x), int(self.y)), self.radius)

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.original_radius = radius
        self.radius = radius
        self.shrink_speed = 0.5
        self.breaking = False
        self.broken = False
        self.color = random.choice(colors)
        self.particles = []
        
    def update(self):
        if not self.broken and self.radius > 50:  
            self.radius -= self.shrink_speed
        elif not self.broken:
            self.breaking = True
            self.create_particles()
            self.broken = True
            
    def create_particles(self):
        for _ in range(30):
            angle = random.uniform(0, mt.pi*2)
            speed = random.uniform(1, 5)
            self.particles.append({
                'x': self.x,
                'y': self.y,
                'dx': mt.cos(angle) * speed,
                'dy': mt.sin(angle) * speed,
                'size': random.randint(2, 5),
                'life': 60
            })
    
    def update_particles(self):
        for p in self.particles[:]:
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['life'] -= 1
            if p['life'] <= 0:
                self.particles.remove(p)
    
    def draw(self, surface):
        if not self.broken:
            pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius, 3)
        else:
            for p in self.particles:
                pygame.draw.circle(surface, self.color, (int(p['x']), int(p['y'])), p['size'])


circle = Circle(700, 500, 200)
ball = Ball(700, 400, 15, 3, 0)
circles = [circle]


running = True
while running:
    window.fill(black)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    ball.update(circle)
    circle.update()
    
    if circle.broken and len(circle.particles) == 0:
        circle = Circle(700, 500, 200)
        circles.append(circle)
    if circle.breaking:
        circle.update_particles()
    circle.draw(window)
    ball.draw(window)
    
    display.update()
    clock.tick(fps)

pygame.quit()
