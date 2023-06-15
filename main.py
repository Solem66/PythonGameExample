import pygame, sys
from pygame.locals import *
import random
 
pygame.init()
 
FPS = 60
FramePerSec = pygame.time.Clock()
 
# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Screen information
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Movement configuration
PLAYERPACE = 4
ENEMYPACE = 2
 
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.rect = Rect(0,0,0,0)
        self.rect.center = (300, 300)
        self.rect.size = (10, 10)
 
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -PLAYERPACE)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, PLAYERPACE)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-PLAYERPACE, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(PLAYERPACE, 0)
 
    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.rect = Rect(0,0,0,0)
        self.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        self.rect.size = (10, 10)

    def move(self, player):
        if self.rect.centerx < player.rect.centerx:
            mx = ENEMYPACE
        else:
            mx = -ENEMYPACE
        if self.rect.centery < player.rect.centery:
            my = ENEMYPACE
        else:
            my = -ENEMYPACE
        self.rect.move_ip(mx, my)
        # self.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)
         
P1 = Player()
E1 = Enemy()
 
while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    E1.move(P1)
    P1.update()
     
    DISPLAYSURF.fill(WHITE)
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)
         
    pygame.display.update()
    FramePerSec.tick(FPS)