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
        self.fireRateBoost = 0
        self.invincibilityTimer = 30
        self.speedBoost = 0
        self.bulletSpeedBoost = 0
        self.range = 350
        
        self.basedmg = 20
        self.dmgBoost = 0
        self.dmg = self.basedmg + self.dmgBoost
        
        self.maxhealth = 100
        self.health = self.maxhealth
        self.maxshield = 100
        self.shield = self.maxshield
        self.hpregen = self.maxhealth/1000.
        self.shieldregen = self.maxshield/100.
        self.bulletSpeed = 6
    
    def hit(self, dmg):
        if self.shield - dmg <= 0:
            self.shield = 0
            overflow = abs(self.shield - dmg)
            self.health -= overflow
        
        else:
            self.shield -= dmg
    
    def update(self):
        self.hpregen = self.maxhealth/1000.
        self.shieldregen = self.maxshield/100.
        if ((self.shield < self.maxshield) and (self.health == self.maxhealth)):
            self.shield += self.shieldregen
        
        if self.health < self.maxhealth:
            self.health += self.hpregen
        
        self.dmg = self.basedmg + self.dmgBoost
        
    def levelUP(self):
        self.speed += 3
        self.bulletSpeed += 3
        self.range += 50
        self.fireRate -= 2
        self.maxhealth += 15
        self.maxshield += 15
        self.hpregen = self.maxhealth/1000.
        self.shieldregen = self.maxshield/100.
        self.basedmg += 7
    
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
        range = self.range
        return Bullet(self.x+disX, self.y-disY, angle, speed, range)
    
    def draw(self, canvas, data):
        
        x,y = self.x - data.scrollX, self.y - data.scrollY
        canvas.create_image(x,y,image = self.image[2])
        
        
        