'''
pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
use this code in your term project if you want
- CITE IT
- you can modify it to your liking
  - BUT STILL CITE IT
- you should remove the print calls from any function you aren't using
- you might want to move the pygame.display.flip() to your redrawAll function,
    in case you don't need to update the entire display every frame (then you
    should use pygame.display.update(Rect) instead)
'''
# import module_manager
# module_manager.review()
import pygame
import math
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class PygameGame(object):
    
    def init(self):
        self.pos = (-1,-1)
        self.size = 20
        self.controller = Leap.Controller()
        self.frame = self.controller.frame()
        self.fingerNames = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        self.boneNames = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
        
        self.folPos = (self.width/2, self.height/2)
        self.speed = 1
        
        self.dX = 0
        self.dY = 0
        self.color = (255,0,0)
    
        
    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        tup = (keyCode, modifier)
        if tup == (119,1024):
            pygame.quit()
            exit()

    def keyReleased(self, keyCode, modifier):
        pass
        
    def updateLeapMotionData(self):
        self.frame = self.controller.frame()
        frame = self.frame
        if len(frame.hands) > 0:
            self.pause = False
        else:
            self.pause = True
            
    def timerFired(self, dt):
        self.updateLeapMotionData()
        
        app_width = 777
        app_height = 777
        
        app_x = app_y = -1
        hand = self.frame.hands[0]
        if hand.is_valid:
            iBox = self.frame.interaction_box
            leapPoint = hand.stabilized_palm_position
            normalizedPoint = iBox.normalize_point(leapPoint, False)
            
            app_x = normalizedPoint.x * app_width
            app_y = (1 - normalizedPoint.y) * app_height
        
        self.pos = (app_x,app_y)
            
   
        # x,y = self.pos

       ##   xLeap = self.frame.hands[0].palm_position[0]
        # yLeap = self.frame.hands[0].palm_position[1]
        # 
        # xApp = (xLeap + 120) * (self.width/240.) + 0
        # yApp = (self.height - yLeap) * (self.height/300.) - self.height/2.
    
   #    #   xApp = self.width/2. - 1
        # self.pos = (xApp,yApp)
        
        
        
        x0,y0 = self.pos
        x1,y1 = self.folPos
        
        baseVector = (1,0)
        directionVector = (x0 - x1, y0 - y1)
        
        length = math.sqrt(directionVector[0] ** 2 + directionVector[1] ** 2)
        
        angle = math.acos((1 * directionVector[0])/(1.*length))
        dx1 = self.speed*math.cos(angle)
        dy1 = self.speed*math.sin(angle)
        
        if y1 > y0:
            dy1 *= -1
        
        print(dy1)
        
        a,b = directionVector
        if abs(a) > 7 or abs(b > 7):
            self.folPos = (x1+dx1, y1+dy1)
        
        

    def redrawAll(self, screen):
        x,y = self.pos
        x -= self.size
        y -= self.size
        
        x1,y1 = self.folPos
        x1 -= self.size
        y1 -= self.size
        
        Rect = (x,y,self.size*2,self.size*2)
        pygame.draw.rect(screen, self.color, Rect, 0)
        
        Rect = (x1,y1,self.size*2, self.size*2)
        pygame.draw.rect(screen, (0,0,255), Rect,0)

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=777, height=777, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()
        exit()

def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()