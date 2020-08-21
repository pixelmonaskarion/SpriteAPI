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
    KEYDOWN,
    QUIT,
)

def init():
    global fontList
    global font
    pygame.init()
    fontList = pygame.font.get_fonts()
    font = pygame.font.SysFont(fontList[random.randint(0,len(fontList))],10)

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
    


class Sprite():
    def __init__(self, screen, color, size, x, y):
        self.screen = screen
        self.color = color
        self.size = size
        self.x = x
        self.y = y
        self.color = color
        self.image = newImage("face.png")
    def update(self):
        pygame.draw.rect(self.screen, self.color, (self.x,self.y,self.size,self.size))
    def changePos(self,x,y):
        self.x = self.x + x
        self.y = self.y - y
    def setImage(self,path):
        self.image = newImage(path)

class Player():
    def __init__(self, screen, color, size, x, y, V, f):
        self.screen = screen
        self.color = color
        self.size = size
        self.x = x
        self.y = y
        self.textbubble = []
        self.isVelocity = V
        self.image = newImage("face.png")
        if self.isVelocity == True:
            self.Vx = 0
            self.Vy = 0
        self.f = f
    def update(self):
        self.screen.blit(pygame.transform.scale(self.image, (self.size, self.size)), (self.x-(self.size/2), self.y-(self.size/2)))
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
            if keys[K_RIGHT]:
                self.changePos(10,0)
            if keys[K_LEFT]:
                self.changePos(-10,0)
            if keys[K_UP]:
                self.changePos(0,10)
            if keys[K_DOWN]:
                self.changePos(0,-10)
        else:
            if keys[K_RIGHT]:
                self.Vx = self.Vx + 10
            if keys[K_LEFT]:
                self.Vx = self.Vx - 10
            if keys[K_UP]:
                self.Vy = self.Vy + 10
            if keys[K_DOWN]:
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
        fontSize = font.size(self.text)
        if fontSize[0] > fontSize[1]:
            fontSize = fontSize[0]
        else:
            fontSize = fontSize[1]
        fontSize = fontSize * 2
        pygame.draw.circle(screen, (255,255,255), (self.sprite.x + (self.sprite.size + (fontSize/2)/2) + 30, self.sprite.y - (self.sprite.size + (fontSize/2)/2) - 30), fontSize)
        pygame.draw.circle(screen, (100,100,100), (self.sprite.x + (self.sprite.size + (fontSize/2)/2) + 30, self.sprite.y - (self.sprite.size + (fontSize/2)/2) - 30), fontSize,10)
        font.render(self.text, 10,(0,0,0))







