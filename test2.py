import math
import random
from Tkinter import *
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

def init(data):
   
    #ImageTk.PhotoImage(cursPIL)
    data.controller = Leap.Controller()
    
    data.controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
    data.controller.config.set("Gesture.Swip.MinLength", 100.0)
    data.controller.config.set("Gesture.Swip.MinVelocity", 777)
    data.controller.config.save()
    
    data.frame = data.controller.frame()
    data.fingerNames = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    data.boneNames = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    
    
def mousePressed(event, data):
    pass

def keyPressed(event, data):
    updateLeapMotionData(data)
    
    p = data.frame.hands[0].palm_position
    palmPos = (p.x, p.y, p.z)
    
    p1 = data.frame.pointables[0].tip_position
    pos1 = (p1.x, p1.y, p1.z)
    p2 = data.frame.pointables[1].tip_position
    pos2 = (p2.x, p2.y, p2.z)
    p3 = data.frame.pointables[2].tip_position
    pos3 = (p3.x, p3.y, p3.z)
    p4 = data.frame.pointables[3].tip_position
    pos4 = (p4.x, p4.y, p4.z)
    p5 = data.frame.pointables[4].tip_position
    pos5 = (p5.x, p5.y, p5.z)
    
    print("palm: ", palmPos)
    print("p1: ", pos1)
    print("p2: ", pos2)
    print("p3: ", pos3)
    print("p4: ", pos4)
    print("p5: ", pos5)
    print(pos5[0] - pos1[0])
    print("---------")
    
def timerFired(data):
    pass

def updateLeapMotionData(data):
    data.frame = data.controller.frame()
    
def redrawAll(canvas, data):
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