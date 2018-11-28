import math
import random
from Tkinter import *
from PIL import Image, ImageTk
from Bullet import Bullet

class EnemyShip(object):
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.speed = 3
        self.angle = 0
        
        self.size = 50
        self.saftyR = 100
        self.firingDis = 300
        
        self.health = 100
        self.shield = 100
        self.hpregen = self.health/1000.
        self.shieldregen = self.shield/100.
        self.bulletSpeed = 10
        
        self.fireRate = 10

    def update(self, data):
        x0,y0 = self.x,self.y
        for ast in data.asteroids:
            x1,y1 = ast.x, ast.y
            
        x0,y0 = data.ship.x, data.ship.y
        x1,y1 = self.x, self.y
        
        baseVector = (1,0)
        directionVector = (x0 - x1, y0 - y1)
    
        length = math.sqrt(directionVector[0] ** 2 + directionVector[1] ** 2)
        
            
        angle = math.acos((1 * directionVector[0])/(1.*length))
        self.angle = angle
        
        if length <= self.firingDis:
            angle += math.pi/2.
        
        dx1 = (self.speed)*math.cos(angle)
        dy1 = (self.speed)*math.sin(angle)
            
        if y1 > y0:
            dy1 *= -1
        
        if y1 < y0:
            angle *= -1
            self.angle *= -1
            
        
        self.x += dx1
        self.y += dy1
    
    def makeBullet(self, data):

        angle = self.angle
        speed = self.bulletSpeed
        return Bullet(self.x, self.y, angle, speed, 1)
        
    
    def draw(self, canvas, data):
        x,y = self.x-data.scrollX, self.y-data.scrollY
        r = self.size
        canvas.create_oval(x-r,y-r,x+r,y+r, fill = "white")
        
        
        