import math
import random
from Asteroid import Asteroid
from Ship import Ship
from EnemyShip import EnemyShip
from PowerUp import PowerUp
from Tkinter import *
from PIL import Image
from PIL import ImageTk
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

def init(data):
    data.timerCalled = 0
    data.mode = "title"
    data.level = 1
    
    data.fieldSizeW = 3 * data.width
    data.fieldSizeH = 3 * data.height
    data.scrollX = data.width
    data.scrollY = data.height
    data.scrollMarginX = data.width/2.
    data.scrollMarginY = data.height/2.
    
    Asteroid.init()
    PowerUp.init()
    Ship.init()
    
    data.asteroids = []
    data.bullets = []
    data.margin = 51
    
    for i in range(5):
        x = random.randint(data.margin, data.fieldSizeW-data.margin)
        y = random.randint(data.margin, data.fieldSizeH-data.margin)
        data.asteroids.append(Asteroid(x,y,data.level))
    
    data.paused = False
    
    
    pilImg = baseImg = Image.open("images/asteroids2.png")
    data.astimage2 = [pilImg, baseImg, ImageTk.PhotoImage(pilImg)]
    data.angle = 0
    data.angleSpeed = 10
    
    data.background = Image.open("images/starryspace.png")
    data.background = data.background.resize((data.fieldSizeW, data.fieldSizeH), \
                                                Image.ANTIALIAS)
    data.background = ImageTk.PhotoImage(data.background)
    
    
    # Leap Motion
    data.cursor = (-50,-50)
    data.cursorImage = PhotoImage(file = "images/curs2v1.gif")
    data.controller = Leap.Controller()
    
    # data.controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
    # data.controller.config.set("Gesture.Swip.MinLength", 100.0)
    # data.controller.config.set("Gesture.Swip.MinVelocity", 777)
    # data.controller.config.save()
    
    data.frame = data.controller.frame()
    data.fingerNames = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    data.boneNames = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    
    # Ship
    data.ship = Ship(data.width/2., data.height/2.)
    data.reload = data.ship.fireRate
    data.invincibilityTimer = data.ship.invincibilityTimer
    
    
    
    data.enemy = EnemyShip(0,0)
    data.enemyReload = data.enemy.fireRate
    # boosts
    data.boostDuration = 500  # base level is 5 seconds
    data.boosts = []
    data.boosted = []
    data.boostTypes = ["speed", "bulletspeed"]
    data.boosts.append(PowerUp(0,0,"speed", data.boostDuration, 15))
    
    
def mousePressed(event, data):
    if data.mode == "title":
        titleMousePressed(event, data)
    elif data.mode == "shop":
        shopMousePressed(event, data)
    elif data.mode == "play":
        playMousePressed(event, data)
    elif data.mode == "help":
        helpMousePressed(event, data)

def keyPressed(event, data):
    if data.mode == "title":
        titleKeyPressed(event, data)
    elif data.mode == "shop":
        shopKeyPressed(event, data)
    elif data.mode == "play":
        playKeyPressed(event, data)
    elif data.mode == "help":
        helpKeyPressed(event, data)
        
def timerFired(data):
    data.timerCalled += 1
    updateLeapMotionData(data)
    
    # for point in data.frame.pointables:
    #     print(point)
    # print("---------")
    
    app_width = data.width
    app_height = data.height
        
    app_x, app_y = data.cursor
    hand = data.frame.hands[0]
    if hand.is_valid:
        iBox = data.frame.interaction_box
        leapPoint = hand.stabilized_palm_position
        normalizedPoint = iBox.normalize_point(leapPoint, False)
        
        app_x = normalizedPoint.x * app_width
        app_y = (1 - normalizedPoint.y) * app_height
        
    data.cursor = (app_x,app_y)
    
    if data.mode == "title":
        titleTimerFired(data)
    elif data.mode == "shop":
        shopTimerFired(data)
    elif data.mode == "play":
        playTimerFired(data)
    elif data.mode == "help":
        helpTimerFired(data)

def updateLeapMotionData(data):
    data.frame = data.controller.frame()
    
def redrawAll(canvas, data):
    canvas.create_image(0 - data.scrollX,0 - data.scrollY, anchor = NW, \
                                image = data.background)
    
    x,y = data.cursor
    canvas.create_image(x,y, image = data.cursorImage)
    if data.mode == "title":
        titleRedrawAll(canvas,data)
    elif data.mode == "shop":
        shopRedrawAll(canvas,data)
    elif data.mode == "play":
        playRedrawAll(canvas,data)
    elif data.mode == "help":
        helpRedrawAll(canvas,data)

#### title screen events

def titleMousePressed(event, data):
    pass
    
def titleKeyPressed(event, data):
    if event.keysym.lower() == "p":
        data.mode = "play"
    elif event.keysym.lower() == "h":
        data.mode = "help"
    
def titleTimerFired(data):
    data.angle += data.angleSpeed
    PILimg = data.astimage2[0]
    baseImg = data.astimage2[1]
    PILimg = baseImg.rotate(data.angle)
    data.astimage2 = [PILimg, baseImg, ImageTk.PhotoImage(PILimg)]

def titleRedrawAll(canvas, data):
    data.ship.rotateShip(3.14/2)
    canvas.create_image(data.width/3., data.height/3., image = data.ship.image[2])
    
    canvas.create_image(data.width/2.,data.height/2., image = data.astimage2[2])
    canvas.create_text(data.width/2, 0, text = "Title Screen", anchor = N, \
                            font = ("Arial bold", 77), fill = "white")

#### play screen events

def playMousePressed(event, data):
    data.mode = "shop"
    
def playKeyPressed(event, data):
    bullet = data.ship.makeBullet(data)
    print(bullet)
    data.bullets.append(bullet)

def movePlayer(dx, dy, data):
    pX, pY = data.ship.x, data.ship.y
    pX += dx
    pY += dy
    
    if ((pX + 50 > data.fieldSizeW) or \
       (pX - 50 < 0) or \
       (pY + 50 > data.fieldSizeH) or \
       (pY - 50 < 0)):
           return
    
    data.ship.x, data.ship.y = pX, pY
    # scroll to make map visible as needed
    if (pX < data.scrollX + data.scrollMarginX):
        data.scrollX = pX - data.scrollMarginX
    if (pX > data.scrollX + data.width - data.scrollMarginX):
        data.scrollX = pX - data.width + data.scrollMarginX
    if (pY < data.scrollY + data.scrollMarginY):
        data.scrollY = pY - data.scrollMarginY
    if (pY > data.scrollY - data.height + data.scrollMarginY):
        data.scrollY = pY - data.scrollMarginY
    
    data.ship.x, data.ship.y = pX, pY
    
def playTimerFired(data):
    if data.timerCalled % int(100 * (4./5)**data.level) == 0:
        x = random.randint(data.margin, data.fieldSizeW-data.margin)
        y = random.randint(data.margin, data.fieldSizeH-data.margin)
        ast = Asteroid(x,y)
        data.asteroids.append(ast)
        
        x = random.randint(data.margin, data.fieldSizeW-data.margin)
        y = random.randint(data.margin, data.fieldSizeH-data.margin)
        type = random.choice(data.boostTypes)
        boostVal = random.randint(5,20)
        data.boosts.append(PowerUp(x,y,type, data.boostDuration, boostVal))
        
        
    for ast in data.asteroids:
        ast.update(data)
    
    for bullet in data.bullets:
        bullet.update()
    
    for ast in data.asteroids:
        x0, y0 = ast.x, ast.y
        r1 = ast.r * 5./2.
        for bullet in data.bullets:
            x1, y1 = bullet.x, bullet.y
            r = r1 + 10
            dis = math.sqrt((y1-y0)**2 + (x1-x0)**2)
            if dis <= r:
                data.bullets.remove(bullet)
                
                data.asteroids.extend(ast.breakApart())
                try:
                    data.asteroids.remove(ast)
                except:
                    pass
    
    for boost in data.boosted:
        if boost.type == "speed":
            data.ship.speedBoost = boost.val
            boost.counter += 1
            if boost.counter >= boost.duration:
                data.ship.speedBoost = 0
                try:
                    data.boosted.remove(boost)
                except:
                    pass
        elif boost.type == "bulletspeed":
            data.ship.bulletSpeedBoost = boost.val
            boost.counter += 1
            if boost.counter >= boost.duration:
                data.ship.bulletSpeedBoost = 0
                try:
                    data.boosted.remove(boost)
                except:
                    pass
        
    x0,y0 = data.cursor
    x1,y1 = data.width/2., data.height/2.
        
    baseVector = (1,0)
    directionVector = (x0 - x1, y0 - y1)

    length = math.sqrt(directionVector[0] ** 2 + directionVector[1] ** 2)
        
    angle = math.acos((1 * directionVector[0])/(1.*length))
    
    dx1 = (data.ship.speed+data.ship.speedBoost)*math.cos(angle)
    dy1 = (data.ship.speed+data.ship.speedBoost)*math.sin(angle)
        
    if y1 > y0:
        dy1 *= -1
    
    if y1 < y0:
        angle *= -1
    
    data.ship.rotateShip(angle)
    data.ship.angle = angle
    
    a,b = directionVector
    
    if abs(a) > 7 or abs(b > 7):
        movePlayer(dx1, dy1, data)
    
    data.enemy.update(data)
    
    
    x0,y0 = data.width/2.,data.height/2.
    for boost in data.boosts:
        x1,y1 = boost.x-data.scrollX,boost.y-data.scrollY
        if math.sqrt((x1-x0)**2 + (y1-y0)**2) <= 50 + 25:
            data.boosted.append(boost)
            try:
                data.boosts.remove(boost)
            except:
                pass
    
    for asteroid in data.asteroids:
        x1, y1 = asteroid.x-data.scrollX, asteroid.y-data.scrollY
        
        if ((math.sqrt((x1-x0)**2 + (y1-y0)**2) <= 50 + asteroid.r*5./2) and \
           (data.invincibilityTimer == data.ship.invincibilityTimer)):
            data.invincibilityTimer = 0
            print("bam")
            if data.ship.shield > 0:
                data.ship.shield -= 10
            else:
                data.ship.health -= 10
            
            data.asteroids.extend(asteroid.breakApart())
            try:
                data.asteroids.remove(ast)
            except:
                pass
    
    if data.ship.health <= 0:
        data.ship.health = 0
        
    
    # fire bullet
    p1 = data.frame.pointables[0].tip_position
    # p2 = data.frame.pointables[1].tip_position
    # p3 = data.frame.pointables[2].tip_position
    # p4 = data.frame.pointables[3].tip_position
    p5 = data.frame.pointables[4].tip_position
    disX = p5.x - p1.x
    
    if data.reload < data.ship.fireRate:
        data.reload += 1
    
    if data.enemyReload < data.enemy.fireRate:
        data.enemyReload += 1
    
    if data.invincibilityTimer < data.ship.invincibilityTimer:
        data.invincibilityTimer += 1
        print(data.invincibilityTimer)
    
    if abs(disX) < 25:
        if data.reload == data.ship.fireRate:
            b = data.ship.makeBullet(data)
            data.bullets.append(b)
            data.reload = 0
    
    x0,y0 = data.ship.x, data.ship.y
    x1,y1 = data.enemy.x, data.enemy.y
    if math.sqrt((x1-x0)**2 + (y1-y0)**2) <= data.enemy.firingDis:
        if data.enemyReload == data.enemy.fireRate:
            data.bullets.append(data.enemy.makeBullet(data))
            data.enemyReload = 0

def playRedrawAll(canvas, data):
    
    canvas.create_rectangle(0 - data.scrollX, 0 - data.scrollY,
                            data.fieldSizeW - data.scrollX,
                            data.fieldSizeH - data.scrollY, width = 20)
    for ast in data.asteroids:
        ast.draw(canvas, data)
    
    for bullet in data.bullets:
        bullet.draw(canvas, data)
    
    for boost in data.boosts:
        boost.draw(canvas, data)
        
    data.ship.draw(canvas, data)
    data.enemy.draw(canvas, data)
    
    canvas.create_line(10,10,10+data.ship.health, 10,fill = "red", width = 10)
    canvas.create_line(10,30,10+data.ship.shield, 30,fill = "blue", width = 10)
     
    canvas.create_text(data.width/2, 0, text = "DEMO", anchor = N, \
                            font = ("Arial bold", 77), fill = "white")

#### help screen events

def helpMousePressed(event, data):
    pass
    
def helpKeyPressed(event, data):
    if event.keysym.lower() == "b":
        data.mode = "title"
    
def helpTimerFired(data):
    pass

def helpRedrawAll(canvas, data):
    canvas.create_text(data.width/2, 0, text = "Help Screen", anchor = N, \
                            font = ("Arial bold", 77), fill = "white")

#### shop screen events

def shopMousePressed(event, data):
    data.mode = "play"
    
def shopKeyPressed(event, data):
    pass
    
def shopTimerFired(data):
    pass

def shopRedrawAll(canvas, data):
    pass

#################################################################
# use the run function as-is
#################################################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(777, 777)