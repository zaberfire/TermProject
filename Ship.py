import math
import random
from Tkinter import *
from PIL import Image, ImageTk

class Ship(object):
    
    @staticmethod
    def init():
        Ship.image = Image.open("images/spaceship.png")
    
    def __init__(self, x, y):
       
        self.x = x
        self.y = y
            
        self.image = [Ship.image, ImageTk.PhotoImage(Ship.image)]
        
        PILimg = self.image[0]
        PILimg = baseImg = PILimg.resize((130,90),Image.ANTIALIAS)
        self.image = [PILimg, baseImg, ImageTk.PhotoImage(PILimg)]
        
        self.speed = 3
        
    def levelUP(self):
        self.speed += 1
    
    def rotateShip(self,angle):
        PILimg = self.image[0]
        baseImg = self.image[1]
        PILimg = baseImg.rotate(math.degrees(angle))
        self.image = [PILimg, baseImg, ImageTk.PhotoImage(PILimg)]
    
    def draw(self, canvas,data):
        x,y = data.width/2., data.height/2.
        canvas.create_image(x,y,image = self.image[2])
        
        
        