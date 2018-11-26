import math
import os
import random
from Tkinter import *
from PIL import Image, ImageTk

class PowerUp(object):
    @staticmethod
    def init():
        PowerUp.images = dict()
        imgDir = "images/PowerUps"
        for filename in os.listdir(imgDir):
            if filename == ".DS_Store": continue
            newFile = imgDir + "/" + filename
            img = Image.open(newFile)
            img = img.resize((50,50), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            PowerUp.images[filename[:filename.index(".")]] = img
            
    def __init__(self, x, y, type, duration, value):
        self.x = x
        self.y = y
        self.type = type
        self.duration = duration
        self.counter = 0
        self.val = value
        self.image = PowerUp.images[type]
        
    def draw(self, canvas, data):
        x = self.x - data.scrollX
        y = self.y - data.scrollY
        canvas.create_image(x,y,image = self.image)