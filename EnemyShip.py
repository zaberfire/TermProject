import math
import random
from Tkinter import *
from PIL import Image, ImageTk
from Asteroid import Asteroid
from Bullet import Bullet

class EnemyShip(object):
    
    @staticmethod
    def init():
        EnemyShip.image = Image.open("images/enemy.png")
    
    bosses = ["Type 1", "TesterWrester", "LMAO"]
        
    def __init__(self, x, y, level):
        self.x = x
        self.y = y
        self.name = EnemyShip.bosses[level-1]
        self.image = [EnemyShip.image, ImageTk.PhotoImage(EnemyShip.image)]
        
        PILimg = self.image[0]
        PILimg = baseImg = PILimg.resize((100,100),Image.ANTIALIAS)
        self.image = [PILimg, baseImg, ImageTk.PhotoImage(PILimg)]
        
        self.speed = 3
        self.angle = 0
        
        self.size = 50
        self.saftyR = 200
        self.firingDis = 350
        
        self.health = 100*level
        self.shield = 100
        
        self.bulletSpeed = 10 * (level/2.)
        
        self.dmg = 15 * level
        self.fireRate = 20 - (3*level)

    def update(self, data):
        x0,y0 = self.x,self.y
        for ast in data.asteroids:
            x1,y1 = ast.x, ast.y
            if math.sqrt((y1-y0)**2 + (x1-x0)**2) <= self.saftyR:
                self.avoidThing(data, x1, y1)
                
                
        x1, y1 = data.ship.x, data.ship.y
        if math.sqrt((x1-x0)**2 + (y1-y0)**2) <= self.saftyR:
            self.avoidThing(data, x1, y1)
        elif math.sqrt((x1-x0)**2 + (y1-y0)**2) > self.firingDis:
            self.goToThing(data, x1, y1)
       
            
    def makeBullet(self, data):
        angle = self.angle
        disX = 50*math.cos(angle)
        disY = 50*math.sin(angle)
        speed = self.bulletSpeed
        return Bullet(self.x+disX, self.y-disY, angle, speed, 1)
    
    def avoidThing(self, data, x1, y1):
        x0,y0 = self.x, self.y
        
        directionVector = (x0 - x1, y0 - y1)
        length = math.sqrt(directionVector[0] ** 2 + directionVector[1] ** 2)
        
        angle = math.acos((1 * directionVector[0])/(1.*length))
        self.angle = angle
        
        # if length <= self.saftyR:
        #     angle *= -1
        # # elif length > self.saftyR and length <= self.firingDis:
        # #     angle += math.pi/2.
        
        dx1 = (self.speed)*math.cos(angle)
        dy1 = (self.speed)*math.sin(angle)
            
        if y1 > y0:
            dy1 *= -1
        
        if y1 < y0:
            angle *= -1
            self.angle *= -1
        
        PILimg = self.image[0]
        baseImg = self.image[1]
        PILimg = baseImg.rotate(math.degrees(angle))
        self.image = [PILimg, baseImg, ImageTk.PhotoImage(PILimg)]
        
        self.x += dx1
        self.y += dy1
    
    def goToThing(self, data, x0, y0):
        x1,y1 = self.x, self.y
        
        directionVector = (x0 - x1, y0 - y1)
        length = math.sqrt(directionVector[0] ** 2 + directionVector[1] ** 2)
        
        angle = math.acos((1 * directionVector[0])/(1.*length))
        self.angle = angle
        
        dx1 = (self.speed)*math.cos(angle)
        dy1 = (self.speed)*math.sin(angle)
            
        if y1 > y0:
            dy1 *= -1
        
        if y1 < y0:
            angle *= -1
            self.angle *= -1
        
        PILimg = self.image[0]
        baseImg = self.image[1]
        PILimg = baseImg.rotate(math.degrees(angle))
        self.image = [PILimg, baseImg, ImageTk.PhotoImage(PILimg)]
        
        self.x += dx1
        self.y += dy1
        
    
    def draw(self, canvas, data):
        x,y = self.x-data.scrollX, self.y-data.scrollY
        canvas.create_image(x,y, image = self.image[2])
        
        
        