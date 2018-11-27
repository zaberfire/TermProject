import math
import random
from Tkinter import *
from PIL import Image, ImageTk
from Bullet import Bullet

class Ship(object):
    
    @staticmethod
    def init():
        Ship.image = Image.open("images/spaceshipv2.png")
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
            
        self.image = [Ship.image, ImageTk.PhotoImage(Ship.image)]
        
        PILimg = self.image[0]
        PILimg = baseImg = PILimg.resize((100,100),Image.ANTIALIAS)
        self.image = [PILimg, baseImg, ImageTk.PhotoImage(PILimg)]
        
        self.speed = 3
        self.angle = 0
        
        self.fireRate = 70
        self.invincibilityTimer = 30
        self.speedBoost = 0
        self.bulletSpeedBoost = 0
        
        self.health = 100
        self.shield = 100
        self.hpregen = self.health/1000.
        self.shieldregen = self.shield/100.
        self.bulletSpeed = 6
        
    def levelUP(self):
        self.speed += 1
    
    def rotateShip(self,angle):
        PILimg = self.image[0]
        baseImg = self.image[1]
        PILimg = baseImg.rotate(math.degrees(angle))
        self.image = [PILimg, baseImg, ImageTk.PhotoImage(PILimg)]
    
    def makeBullet(self, data):
        angle = self.angle
        disX = 50*math.cos(angle)
        disY = 50*math.sin(angle)
        speed = self.bulletSpeed + self.bulletSpeedBoost
        return Bullet(self.x+disX, self.y-disY, angle, speed, data.level)
    
    def draw(self, canvas, data):
        x,y = data.width/2., data.height/2.
        canvas.create_image(x,y,image = self.image[2])
        
        
        