import math
import random
from Asteroid import Asteroid
from Ship import Ship
from EnemyShip import EnemyShip
from PowerUp import PowerUp
from ShopHolo import ShopHolo
from Tkinter import *
from PIL import Image
from PIL import ImageTk
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

def init(data):
    Asteroid.init()
    PowerUp.init()
    Ship.init()
    EnemyShip.init()
    ShopHolo.init(data)
    
    data.mode = "title"
    
    data.fieldSizeW = 3 * data.width
    data.fieldSizeH = 3 * data.height
    data.scrollMarginX = data.width/2.
    data.scrollMarginY = data.height/2.
    
    data.margin = 51
    data.boostTypes = ["speed", "bulletspeed", "firerate", "dmgboost"]
    
    initializeGame(data, data.mode)
    loadImages(data)
    
    data.paused = False
    
    data.angle = 0
    data.angleSpeed = 10
    
    # shop screen holos
    holo1 = ShopHolo(1)
    holo2 = ShopHolo(2)
    holo3 = ShopHolo(3)
    data.holos = [holo1, holo2, holo3]
    
    # Leap Motion
    data.controller = Leap.Controller()
    
    data.frame = data.controller.frame()
    data.fingerNames = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    data.boneNames = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    
    data.players = dict()

def loadImages(data):
    pilImg = baseImg = Image.open("images/asteroids2.png")
    data.astimage2 = [pilImg, baseImg, ImageTk.PhotoImage(pilImg)]
    
    data.background = Image.open("images/starryspace.png")
    data.background = data.background.resize((data.fieldSizeW, data.fieldSizeH), \
                                                Image.ANTIALIAS)
    data.background = ImageTk.PhotoImage(data.background)
    
    # shop screen images
    data.shopbackground = Image.open("images/shopbackground.png")
    data.shopbackground = data.shopbackground.resize((data.width, data.height), \
                                                Image.ANTIALIAS)
    data.shopbackground = ImageTk.PhotoImage(data.shopbackground)
    
    data.cursorImage = PhotoImage(file = "images/curs2v1.gif")
    
    data.moneyIcon = Image.open("images/icons/moneyIcon.png")
    data.moneyIcon = data.moneyIcon.resize((30,30), Image.ANTIALIAS)
    data.moneyIcon = ImageTk.PhotoImage(data.moneyIcon)
    
def initializeGame(data, screen):
    
    data.level = 1
    
    data.timerCalled = 0
    
    data.scrollX = data.width
    data.scrollY = data.height
    
    data.asteroids = []
    data.bullets = []
    
    for i in range(5):
        x = random.randint(data.margin, data.fieldSizeW-data.margin)
        y = random.randint(data.margin, data.fieldSizeH-data.margin)
        data.asteroids.append(Asteroid(x,y,data.level))
    
    data.cursor = (-50,-50)
    
    # Ship
    data.ship = Ship(data.width/2., data.height/2.)
    data.reload = data.ship.fireRate
    data.invincibilityTimer = data.ship.invincibilityTimer
    
    data.boss = False
    
    # boosts
    data.boostDuration = 500  # base level is 5 seconds
    data.boosts = []
    data.boosted = []
    
    data.money = 0
    data.cost = 5
    data.canBuy = False
    data.effect = False
    
    data.mode = screen
    
    # help screen stuff
    data.boomTexts = []
    data.boomRate = 17
    data.boom = 17
    
def mousePressed(event, data):
    if data.mode == "title":
        titleMousePressed(event, data)
    elif data.mode == "shop":
        shopMousePressed(event, data)
    elif data.mode == "play":
        playMousePressed(event, data)
    elif data.mode == "help":
        helpMousePressed(event, data)
    elif data.mode == "end":
        endMousePressed(event, data)

def keyPressed(event, data):
    if data.mode == "title":
        titleKeyPressed(event, data)
    elif data.mode == "shop":
        shopKeyPressed(event, data)
    elif data.mode == "play":
        playKeyPressed(event, data)
    elif data.mode == "help":
        helpKeyPressed(event, data)
    elif data.mode == "end":
        endKeyPressed(event, data)
        
def timerFired(data):
    data.timerCalled += 1
    updateLeapMotionData(data)
    
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
    elif data.mode == "end":
        endTimerFired(data)

def updateLeapMotionData(data):
    data.frame = data.controller.frame()
    
def redrawAll(canvas, data):
    canvas.create_image(0 - data.scrollX,0 - data.scrollY, anchor = NW, \
                                image = data.background)
    
    if data.mode == "title":
        titleRedrawAll(canvas,data)
    elif data.mode == "shop":
        shopRedrawAll(canvas,data)
    elif data.mode == "play":
        playRedrawAll(canvas,data)
    elif data.mode == "help":
        helpRedrawAll(canvas,data)
    elif data.mode == "end":
        endRedrawAll(canvas, data)

#### title screen events

def titleMousePressed(event, data):
    pass

def titleHandPressed(screen,data):
    data.mode = screen
    
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
    
    p1 = data.frame.pointables[0].tip_position
    p5 = data.frame.pointables[4].tip_position
    disX = p5.x - p1.x
    
    x,y = data.cursor
    x1, y1 = data.width/2., data.height - 100
    y2 = y1 - 50
    if ((x < x1 + 50) and (x > x1 - 50) and \
        (y > y1 - 20) and (y < y1 + 20)):
            if abs(disX) <= 25:
                titleHandPressed("help",data)
            data.overHelp = True
            data.overPlay = False
    elif ((x < x1 + 50) and (x > x1 - 50) and \
        (y > y2 - 20) and (y < y2 + 20)):
            if abs(disX) <= 25:
                titleHandPressed("play",data)
            data.overPlay = True
            data.overHelp = False
    else:
        data.overPlay = False
        data.overHelp = False
    

def createButton(canvas, data,x,y, text, over):
    color = "cyan"
    if over:
        color = "yellow"
    canvas.create_rectangle(x-50,y-20,x+50,y+20, fill = color)
    canvas.create_text(x,y, text = text, fill = "black", \
                        font = ("Arial", 25))

def titleRedrawAll(canvas, data):
    
    canvas.create_image(data.width/2.,data.height/2., image = data.astimage2[2])
    canvas.create_text(data.width/2, 50, text = "Handful",  \
                            font = ("Arial bold", 77), fill = "white")
    canvas.create_text(data.width/2, 125, text = "of", \
                            font = ("Arial bold", 50), fill = "white")
    canvas.create_text(data.width/2, 200, text = "Asteroids",  \
                            font = ("Arial bold", 77), fill = "white")
    
    x = data.width/2.
    y = data.height - 100
                            
    createButton(canvas, data, x,y,"Help", data.overHelp)
    createButton(canvas, data, x, y-50,"Play", data.overPlay)
    
    x,y = data.cursor
    canvas.create_image(x,y, image = data.cursorImage)

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
    if ((data.timerCalled % int(100 * (4./5)**data.level) == 0) and \
        (len(data.asteroids) <= 15)):
            
        # create asteroids
        x = random.randint(data.margin, data.fieldSizeW-data.margin)
        y = random.randint(data.margin, data.fieldSizeH-data.margin)
        ast = Asteroid(x,y)
        data.asteroids.append(ast)
        
        # create boosts
        x = random.randint(data.margin, data.fieldSizeW-data.margin)
        y = random.randint(data.margin, data.fieldSizeH-data.margin)
        type = random.choice(data.boostTypes)
        boostVal = random.randint(5,20)
        data.boosts.append(PowerUp(x,y,type, data.boostDuration, boostVal))
    
    # create boss ship
    if data.timerCalled % 1000 == 0:
        data.boss = True
        mar = data.width/3.
        x = random.randint(mar, data.width - mar)
        y = random.randint(mar, data.height - mar)
        data.enemy = EnemyShip(x,y, data.level)
        data.enemyBullets = []
        data.enemyReload = data.enemy.fireRate
        
        
    for ast in data.asteroids:
        ast.update(data)
    
    for bullet in data.bullets:
        bullet.update()
        if bullet.distance >= bullet.range:
            data.bullets.remove(bullet)
    
    data.ship.update()
    
    # check collisions between asteroids and bullets
    for ast in data.asteroids:
        x0, y0 = ast.x, ast.y
        r1 = ast.r
        for bullet in data.bullets:
            x1, y1 = bullet.x, bullet.y
            r = r1 + 10
            dis = math.sqrt((y1-y0)**2 + (x1-x0)**2)
            if dis <= r:
                data.money = data.money + (15*data.level*2)
                data.bullets.remove(bullet)
                data.asteroids.extend(ast.breakApart())
                
                try:
                    data.asteroids.remove(ast)
                except:
                    pass
                    
        if data.boss:
            for bullet in data.enemyBullets:
                x1, y1 = bullet.x, bullet.y
                r = r1 + 10
                dis = math.sqrt((y1-y0)**2 + (x1-x0)**2)
                if dis <= r:
                    data.enemyBullets.remove(bullet)
                    data.asteroids.extend(ast.breakApart())
                    
                    try:
                        data.asteroids.remove(ast)
                    except:
                        pass
                
    
    # boost timer
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
        
        elif boost.type == "firerate":
            data.ship.fireRateBoost = boost.val
            boost.counter += 1
            if boost.counter >= boost.duration:
                data.ship.fireRateBoost = 0
                try:
                    data.boosted.remove(boost)
                except:
                    pass
        
        elif boost.type == "dmgboost":
            data.ship.dmgBoost = boost.val
            boost.counter += 1
            if boost.counter >= boost.duration:
                data.ship.dmgBoost = 0
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
    
    # pick up boost
    x0,y0 = data.ship.x, data.ship.y
    for boost in data.boosts:
        x1,y1 = boost.x, boost.y
        if math.sqrt((x1-x0)**2 + (y1-y0)**2) <= 50 + 25:
            data.boosted.append(boost)
            try:
                data.boosts.remove(boost)
            except:
                pass
    
    # hit your ship
    for asteroid in data.asteroids:
        x1, y1 = asteroid.x, asteroid.y
        
        if ((math.sqrt((x1-x0)**2 + (y1-y0)**2) <= 50 + asteroid.r) and \
           (data.invincibilityTimer == data.ship.invincibilityTimer)):
            data.invincibilityTimer = 0
            
            data.ship.hit(10 + (data.level-1)*2)
            data.asteroids.extend(asteroid.breakApart())
            try:
                data.asteroids.remove(ast)
            except:
                pass

    # fire bullet
    p1 = data.frame.pointables[0].tip_position
    p5 = data.frame.pointables[4].tip_position
    disX = p5.x - p1.x
    
    
    if data.reload < data.ship.fireRate:
        data.reload += 1
    
    if data.invincibilityTimer < data.ship.invincibilityTimer:
        data.invincibilityTimer += 1
    
    if abs(disX) < 25:
        if data.reload >= data.ship.fireRate - data.ship.fireRateBoost:
            b = data.ship.makeBullet(data)
            data.bullets.append(b)
            data.reload = 0
            
    # boss
    if data.boss:
        data.enemy.update(data)
        for bullet in data.enemyBullets:
            bullet.update()
            x, y = bullet.x, bullet.y
        
        if data.enemyReload < data.enemy.fireRate:
            data.enemyReload += 1
        
        # fire at your ship
        x0,y0 = data.ship.x, data.ship.y
        x1,y1 = data.enemy.x, data.enemy.y
        if math.sqrt((x1-x0)**2 + (y1-y0)**2) <= data.enemy.firingDis:
            if data.enemyReload == data.enemy.fireRate:
                data.enemy.goToThing(data, data.ship.x, data.ship.y)
                data.enemyBullets.append(data.enemy.makeBullet(data))
                data.enemyReload = 0
        
        # fire at asteroids
        if data.enemy.name != "Wraith":
            for asteroid in data.asteroids:
                x0, y0 = asteroid.x, asteroid.y
                if math.sqrt((x1-x0)**2 + (y1-y0)**2) <= data.enemy.safetyR*2:
                    if data.enemyReload == data.enemy.fireRate:
                        data.enemy.goToThing(data, data.ship.x, data.ship.y)
                        data.enemyBullets.append(data.enemy.makeBullet(data))
                        data.enemyReload = 0
        
        # hit enemy ship
        x0,y0 = data.enemy.x, data.enemy.y
        for bullet in data.bullets:
            x1,y1 = bullet.x, bullet.y
            if math.sqrt((x1-x0)**2 + (y1-y0)**2) <= 10 + 50:
                data.bullets.remove(bullet)
                data.enemy.health -= data.ship.dmg
        
        # ships collision
        x1,y1 = data.ship.x, data.ship.y
        if ((math.sqrt((x1-x0)**2 + (y1-y0)**2) <= 100) and \
            (data.invincibilityTimer == data.ship.invincibilityTimer)):
                
            data.invincibilityTimer = 0
            data.enemy.health -= data.ship.dmg
            data.ship.hit(data.enemy.dmg)
        
        # hit your ship
        x0, y0 = data.ship.x, data.ship.y
        for bullet in data.enemyBullets:
            x1, y1 = bullet.x, bullet.y
            if math.sqrt((x1-x0)**2 + (y1-y0)**2) <= 10 + 50:
                data.enemyBullets.remove(bullet)
                data.ship.hit(data.enemy.dmg)
        
        # hit asteroid
        x0, y0 = data.enemy.x, data.enemy.y
        for ast in data.asteroids:
            x1, y1 = ast.x, ast.y
            if math.sqrt((x1-x0)**2 + (y1-y0)**2) <= 50 + ast.r:
                data.enemy.health -= (10 + (data.level-1)*2)
                try:
                    data.asteroids.remove(ast)
                except:
                    pass
            
        if data.enemy.health <= 0:
            data.boss = False
            data.money += 100*data.level
            data.level += 1
    
    if data.ship.health <= 0:
        data.mode = "end"
            

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
    
    if data.ship.health > 0:
        data.ship.draw(canvas, data)
    
    if data.boss:
        for bullet in data.enemyBullets:
            bullet.draw(canvas, data)
        data.enemy.draw(canvas, data)
        
        x0,y0 = data.width/2., data.height - 30
        x1, y1 = x0 + data.enemy.health, y0
        canvas.create_line(x0,y0,x1,y1,fill = "red", width = 15)
        x1,y1 = data.width/2., data.height - 30
        x0, y0 = x1 - data.enemy.health, y1
        canvas.create_line(x0,y0,x1,y1,fill = "red", width = 15)
        name = data.enemy.name
        canvas.create_text(data.width/2., data.height - 50, text = name, anchor = S, \
                            font = ("Arial bold", 66), fill = "white")
        
        
    
    canvas.create_line(10,10,10+data.ship.health, 10,fill = "red", width = 10)
    canvas.create_line(10,30,10+data.ship.shield, 30,fill = "blue", width = 10)
     
    moneyStart = 10 + data.ship.health
    canvas.create_image(moneyStart + 20, 20, image = data.moneyIcon)
    canvas.create_text(moneyStart + 40, 20, text = "%d credits" % data.money, \
                        anchor = W, fill = "white")
    
    
    canvas.create_text(data.width - 10, 20, text = "Level: %d" % data.level, \
                        anchor = E,fill = "white")
    x,y = data.cursor
    canvas.create_image(x,y, image = data.cursorImage)

#### help screen events

def helpMousePressed(event, data):
    pass
    
def helpKeyPressed(event, data):
    if event.keysym.lower() == "b":
        data.mode = "title"
    elif event.keysym.lower() == "p":
        data.mode = "play"
    
def helpTimerFired(data):
    x,y = data.cursor
    p1 = data.frame.pointables[0].tip_position
    p5 = data.frame.pointables[4].tip_position
    disX = p5.x - p1.x
    
    if data.boom < data.boomRate:
        data.boom += 1
    
    if ((abs(disX) <= 25) and (data.boom == data.boomRate)):
        data.boomTexts.append((x,y,0,120))
        data.boom = 0
    
    if len(data.boomTexts) > 7:
        data.boomTexts.pop(0)
    
    for i in range(len(data.boomTexts)):
        x,y = data.boomTexts[i][0], data.boomTexts[i][1]
        t = data.boomTexts[i][2]
        dur = data.boomTexts[i][3]
        t += 1
        if t >= dur:
            data.boomTexts[i] = (-50,-50,0,0)
        else:
            data.boomTexts[i] = (x,y,t,dur)
        
    

def helpRedrawAll(canvas, data):
    canvas.create_text(data.width/2., 0, text = "Controls", anchor = N, \
                            font = ("Arial bold", 77), fill = "white")
    start = 200
    canvas.create_text(50, start, text = "Cursor is controlled by hand.", \
                    anchor = W, font = ("Arial", 30), fill = "white")
    start += 50
    canvas.create_text(50, start, text = "Fire by pinching thumb and pinky.", \
                    anchor = W, font = ("Arial", 30), fill = "white")
    start += 50
    canvas.create_text(50, start, text = "Destroy asteroids to gain credits.", \
                    anchor = W, font = ("Arial", 30), fill = "white")
    start += 50
    canvas.create_text(50, start, text = "Gather powerups:", \
                    anchor = W, font = ("Arial", 30), fill = "white")
    
    start += 50
    x = 100
    for img in PowerUp.images:
        canvas.create_image(x,start, image = PowerUp.images[img])
        x += 100
    
    start += 150
    canvas.create_text(data.width/2., start, text = "Press 'b' to back", \
                     font = ("Arial", 30), fill = "white")
    start += 50
    canvas.create_text(data.width/2., start, text = "...or 'p' to play!", \
                     font = ("Arial", 30), fill = "white")
                    
    for boom in data.boomTexts:
        x,y = boom[0],boom[1]
        canvas.create_text(x,y,text = "BOOM!", fill = "white", \
                        font = ("Arial", 50))
    x,y = data.cursor
    canvas.create_image(x,y, image = data.cursorImage)

#### shop screen events

def shopMousePressed(event, data):
    x,y = event.x, event.y
    cx,cy = data.width/2., data.height - 260
    if ((x > cx - 40) and (x < cx + 40) and \
       (y < cy + 20) and (y > cy - 20) and data.money >= data.cost):
           data.money -= data.cost
           data.cost += random.randint(data.cost, int(data.cost*1.5))
           data.ship.maxhealth += 10
           data.ship.maxshield += 10
           data.ship.health = data.ship.maxhealth
           data.ship.shield = data.ship.maxshield
           data.ship.speed += 1.12
           data.ship.bulletSpeed += 3
           data.ship.fireRate -= 3
           data.ship.basedmg += 5
           data.ship.range += 25
    
def shopKeyPressed(event, data):
    data.mode = "play"
    
def shopTimerFired(data):
    for holo in data.holos:
        holo.update()
        
    if data.money >= data.cost:
        data.canBuy = True
    else:
        data.canBuy = False
        data.effect = False
        
    if data.canBuy:
        data.effect = not data.effect
    

def drawBut(canvas, data, eff):
    color = "gray"
    if eff == True:
        color = "blue"
    
    x,y = data.width/2., data.height - 260
    x0,y0 = x-40, y-20
    x1,y1 = x+40,y+20
        
    canvas.create_rectangle(x0,y0,x1,y1, fill = color)
    canvas.create_text(x,y, text = "Upgrade: %d"%data.cost, fill = "white", font = \
                            ("Arial", 16))
    
def shopRedrawAll(canvas, data):
    margin = 35
    canvas.create_image(0,0, anchor = NW, image = data.shopbackground)
    for holo in data.holos:
        holo.draw(canvas, data)
    
    canvas.create_text(data.width/2., data.height/3., text = "Ship", font = \
                            ("Arial", 30), fill = "white")
                            
    canvas.create_text(data.width/2., data.height/3. + 10+margin, \
                        text = "Health: %d" % data.ship.maxhealth, font = \
                            ("Arial", 20), fill = "white")
                            
    canvas.create_text(data.width/2., data.height/3. + 10+margin*2, \
                        text = "Shield: %d" % data.ship.maxshield, font = \
                            ("Arial", 20), fill = "white")
    canvas.create_text(data.width/2., data.height/3. + 10+3*margin, \
                        text = "Speed: %d" % data.ship.speed, font = \
                            ("Arial", 20), fill = "white")
    canvas.create_text(data.width/2., data.height/3. + 10+4*margin, \
                        text = "Bullet speed: %d" % data.ship.bulletSpeed, font = \
                            ("Arial", 20), fill = "white")
    fireRate = data.ship.fireRate*10
    canvas.create_text(data.width/2., data.height/3. + 10+5*margin, \
                        text = "Fire rate: %d ms" % fireRate, font = \
                            ("Arial", 20), fill = "white")
    canvas.create_text(data.width/2., data.height/3. +10+ 6*margin, \
                        text = "Attack: %d" % data.ship.basedmg, font = \
                            ("Arial", 20), fill = "white")
    drawBut(canvas, data, data.effect)
    

    x,y = data.cursor
    canvas.create_image(x,y, image = data.cursorImage)
    

#### end screen events

def endMousePressed(event, data):
    pass
    
def endKeyPressed(event, data):
    if event.keysym == "p":
        initializeGame(data, "play")
    
def endTimerFired(data):
    pass

def endRedrawAll(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.height, fill = "black")
    canvas.create_text(data.width/2., 0, text = "Game Over", fill = "white", \
                        anchor = N, font = ("Arial", 100))
    
    x,y = data.cursor
    canvas.create_image(x,y, image = data.cursorImage)
   
    
    
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