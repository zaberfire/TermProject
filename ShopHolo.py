import math
import random
from Tkinter import *
from PIL import Image, ImageTk

class ShopHolo(object):
    @staticmethod
    def init(data):
        ShopHolo.img1 = Image.open("images/shopholo1.png")
        ShopHolo.img2 = Image.open("images/shopholo2.png")
        ShopHolo.img3 = Image.open("images/shopholo3.png")
        ShopHolo.imgs = dict()
        ShopHolo.imgs[1] = ShopHolo.img1
        ShopHolo.imgs[2] = ShopHolo.img2
        ShopHolo.imgs[3] = ShopHolo.img3
        
        w = h = int(data.height*2/3.)
        for key in ShopHolo.imgs:
            img = ShopHolo.imgs[key]
            img = img.resize((w,h), Image.ANTIALIAS)
            ShopHolo.imgs[key] = img
            
        
    def __init__(self, image):
        PILimg = baseImg = ShopHolo.imgs[image]
        self.image = [PILimg, baseImg, ImageTk.PhotoImage(PILimg)]
        self.angle = 0
        self.angleSpeed = 2 * image
        if image == 2:
            self.angleSpeed *= -1
        
    def update(self):
        # rotate holo
        self.angle += self.angleSpeed
        PILimg = self.image[0]
        baseImg = self.image[1]
        PILimg = baseImg.rotate(self.angle)
        self.image = [PILimg, baseImg, ImageTk.PhotoImage(PILimg)]
        
    def draw(self, canvas, data):
        canvas.create_image(data.width/2.,data.height/2.,\
                                image = self.image[2])
        