import math
import random
from Tkinter import *
from PIL import Image, ImageTk

class Asteroid(object):
    
    @staticmethod
    def init():
        Asteroid.image = Image.open("images/asteroids2.png")
    
    maxSpeed = 7
    minSize = 2
    maxSize = 7
    
    def __init__(self, x, y, level = None):
        if level is None:
            level = random.randint(Asteroid.minSize, Asteroid.maxSize)
        self.level = level
        
        self.x = x
        self.y = y
        self.r = self.power = 7*self.level
        
        if self.r > 50: self.r = 50
            
        self.image = [Asteroid.image, ImageTk.PhotoImage(Asteroid.image)]
        
        PILimg = self.image[0]
        width = height = self.r * 3
        factor = (self.level*1.) / Asteroid.maxSize
        
        width = height = int(width * factor)
        
        PILimg = baseImg = PILimg.resize((width, height), Image.ANTIALIAS)
        self.r = width/2.
        self.image = [PILimg, baseImg, ImageTk.PhotoImage(PILimg)]
        
        self.angle = 0
        self.angleSpeed = random.randint(-10, 10)
        if self.angleSpeed == 0: self.angleSpeed += 5
        
        vx = random.randint(-Asteroid.maxSpeed, Asteroid.maxSpeed)
        vy = random.randint(-Asteroid.maxSpeed, Asteroid.maxSpeed)
        if vx == 0 and vy == 0:
            vx += 2
            vy += 2
        self.velocity = (vx, vy)
        
    def __repr__(self):
        vx, vy = self.velocity
        return "Asteroid at (%d, %d) going (%d, %d)" % (self.x, self.y, vx, vy)
    
    def update(self, data):
        # rotate asteroid
        self.angle += self.angleSpeed
        PILimg = self.image[0]
        baseImg = self.image[1]
        PILimg = baseImg.rotate(self.angle)
        self.image = [PILimg, baseImg, ImageTk.PhotoImage(PILimg)]
        
        vx, vy = self.velocity
        
        self.x += vx
        self.y += vy
        
        if ((self.x + self.r > data.fieldSizeW) or \
            (self.x - self.r < 0)):
                self.velocity = (-1 * vx, vy)
        
        if ((self.y + self.r > data.fieldSizeH) or \
            (self.y - self.r < 0)):
                self.velocity = (vx, -1 * vy)
    
    def breakApart(self):
        if self.level <= Asteroid.minSize:
            return []
        else:
            ast1 = Asteroid(self.x, self.y, self.level - 1)
            ast2 = Asteroid(self.x, self.y, self.level - 1)
            return [ast1, ast2]
            
    def draw(self, canvas, data):
        x = self.x - data.scrollX
        y = self.y - data.scrollY
        canvas.create_image(x,y,image = self.image[2])
        
        
        