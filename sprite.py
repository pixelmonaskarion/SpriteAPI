import pygame
import random
import math
#import antigravity
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_w,
    K_s,
    K_a,
    K_d,
    KEYDOWN,
    QUIT,
)

def init():
    global fontList
    global font
    pygame.init()
    fontList = pygame.font.get_fonts()
    font = pygame.font.SysFont(str(pygame.font.get_default_font), 30)

def quitWithMessage(message):
    print(message)
    exit()
def setScreen(x, y):
    global screen
    global SSizeX
    global SSizeY
    screen = pygame.display.set_mode([x, y])
    SSizeX = x
    SSizeY = y
    return screen

def getDirection(point1,point2):
    #atan2(p1.y - p2.y, p1.x - p2.x)
    return math.degrees(math.atan2(point1[1] - point2[1], point1[0] - point2[0]))

def text(text, x, y):
    Text = font.render(text, True,(0,0,0))
    screen.blit(Text,
        (x, y)
        )

def getKeys():
    return pygame.key.get_pressed()

def newColor(rgb):
    return pygame.color.Color(rgb)

def setBackground(background):
    if isinstance(background, tuple):
        screen.fill(background)
    else:
        screen.blit(pygame.transform.scale(background, (SSizeX, SSizeY)), (0,0))

def newImage(path):
    #print(path)
    image = pygame.image.load(path)
    return image

def newFont(name, size):
    global font
    pygame.font.init()
    font = pygame.font.SysFont(name, size)
    return font
    


class Sprite():
    def __init__(self, screen, color, size, x, y):
        self.screen = screen
        self.color = color
        self.size = size
        self.x = x
        self.y = y
        self.color = color
        self.image = newImage("faceWithWhite.png")
        self.show = True
    def update(self):
        pygame.draw.rect(self.screen, self.color, (self.x,self.y,self.size,self.size))
    def changePos(self,x,y):
        self.x = self.x + x
        self.y = self.y - y
    def setImage(self,path):
        self.image = newImage(path)

class Player():
    def __init__(self, screen, color, size, x, y, V, f, direction=90):
        self.direction = direction
        self.screen = screen
        self.color = color
        self.size = size
        self.x = x
        self.y = y
        self.textbubble = []
        self.isVelocity = V
        self.image = newImage("faceWithWhite.png")
        if self.isVelocity == True:
            self.Vx = 0
            self.Vy = 0
        self.f = f
    def update(self):
        self.screen.blit(pygame.transform.rotate(pygame.transform.scale(self.image, (self.size, self.size)), (self.direction-90)*-1), (self.x-(self.size/2), self.y-(self.size/2)))
        #pygame.draw.rect(self.screen, self.color, (self.x,self.y,self.size,self.size))
        if self.textbubble != []:
            self.textbubble.draw()
    
    def say(self, text):
        self.textbubble = textBubble(self, text)

    def changePos(self,x,y):
        self.x = self.x + x
        self.y = self.y - y
    def move(self, keys):
        if self.isVelocity == False:
            if keys[K_RIGHT] or keys[K_d]:
                self.changePos(10,0)
            if keys[K_LEFT] or keys[K_a]:
                self.changePos(-10,0)
            if keys[K_UP] or keys[K_w]:
                self.changePos(0,10)
            if keys[K_DOWN] or keys[K_s]:
                self.changePos(0,-10)
        else:
            if keys[K_RIGHT] or keys[K_d]:
                self.Vx = self.Vx + 10
            if keys[K_LEFT] or keys[K_a]:
                self.Vx = self.Vx - 10
            if keys[K_UP] or keys[K_w]:
                self.Vy = self.Vy + 10
            if keys[K_DOWN] or keys[K_s]:
                self.Vy = self.Vy - 10
            self.Vx = self.Vx * self.f
            self.Vy = self.Vy * self.f
            self.changePos(self.Vx, self.Vy)
    def setImage(self, path):
        self.image = newImage(path)
    
    def distanceFrom(self, point):
        return round(math.sqrt(math.pow((point[1]- self.y), 2) + math.pow((point[0] - self.x), 2)))
    
    def touching(self, thing):
        if self.distanceFrom((thing.x, thing.y)) < (thing.size + self.size)/2:
            return True
        return False

    def step(self, NumSteps):
        hy = NumSteps
        y = math.sin(math.radians(self.direction))*hy
        x = math.cos(math.radians(self.direction))*hy
        self.x = self.x - x
        self.y = self.y - y
        #print(self.direction)
        #print("X: %d, Y: %d" % (x,y))
        #print("new pos X: %d, Y: %d" % (self.x, self.y))



def run():
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitWithMessage("goodbye")

class textBubble():
    def __init__(self, sprite, text):
        self.text = text
        self.sprite = sprite

    def draw(self):
        pygame.font.init()
        pygame.draw.circle(screen, (255,255,255), (self.sprite.x + (self.sprite.size/2) + 5, self.sprite.y - (self.sprite.size/2) - 5), 5)
        pygame.draw.circle(screen, (100,100,100), (self.sprite.x + (self.sprite.size/2) + 5, self.sprite.y - (self.sprite.size/2) - 5), 5, 3)
        pygame.draw.circle(screen, (255,255,255), (self.sprite.x + (self.sprite.size/2) + 15, self.sprite.y - (self.sprite.size/2) -20), 10)
        pygame.draw.circle(screen, (100,100,100), (self.sprite.x + (self.sprite.size/2) + 15, self.sprite.y - (self.sprite.size/2) -20), 10, 3)
        text = font.render(self.text, True,(0,0,0))
        fontSize = font.size(self.text)
        if fontSize[0] > fontSize[1]:
            fontSize = fontSize[0]
        else:
            fontSize = fontSize[1]
        fontSize = fontSize * 2
        #pygame.draw.circle(screen, (255,255,255), (self.sprite.x + (self.sprite.size + (fontSize/2)/2) + 30, self.sprite.y - (self.sprite.size + (fontSize/2)/2) - 30), fontSize/2)
        #pygame.draw.circle(screen, (100,100,100), (self.sprite.x + (self.sprite.size + (fontSize/2)/2) + 30, self.sprite.y - (self.sprite.size + (fontSize/2)/2) - 30), fontSize/2,10)
        screen.blit(text,
        ((self.sprite.x + (self.sprite.size + (fontSize/2)/4) + 20, self.sprite.y - (self.sprite.size + (fontSize/2)/4) - 40))
        )