import math

class Bullet(object):
    def __init__(self, x, y, angle, speed, range):
        self.x = x
        self.y = y

        vx = speed * math.cos(angle)
        vy = -speed * math.sin(angle)
        
        self.velocity = (vx,vy)
        
        self.distance = 0
        self.range = range
    
    def __repr__(self):
        x,y = self.velocity
        return "Bullet at (%d,%d) going (%d,%d)" % (self.x,self.y,x,y)
        
    def update(self):
        vx,vy = self.velocity
        
        self.x += vx
        self.y += vy
        
        dis = math.sqrt(vy**2 + vx**2)
        self.distance += self.distance
    
    def draw(self, canvas, data):
        x = self.x - data.scrollX
        y = self.y - data.scrollY
        canvas.create_oval(x-10, y-10, x+10,y+10, fill = "red")
        