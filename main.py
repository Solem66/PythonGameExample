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
PLAYER_PACE = 4
ENEMY_PACE = 2
SPAWN_INTERVAL = 3000
 
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, SPAWN_INTERVAL)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.rect = Rect(0,0,0,0)
        self.rect.center = (300, 300)
        self.rect.size = (10, 10)
 
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -PLAYER_PACE)
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, PLAYER_PACE)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-PLAYER_PACE, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(PLAYER_PACE, 0)
 
    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = Rect(0,0,0,0)
        self.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        self.rect.size = (10, 10)

    def update(self, player):
        if self.rect.centerx < player.rect.centerx:
            mx = ENEMY_PACE
        else:
            mx = -ENEMY_PACE
        if self.rect.centery < player.rect.centery:
            my = ENEMY_PACE
        else:
            my = -ENEMY_PACE
        self.rect.move_ip(mx, my)
        # self.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)
         
P1 = Player()
E1 = Enemy()
enemies = pygame.sprite.Group()
enemies.add(E1)
 
while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == ADDENEMY:
            newEnemy = Enemy()
            enemies.add(newEnemy)

    enemies.update(P1)
    P1.update()
     
    DISPLAYSURF.fill(WHITE)
    P1.draw(DISPLAYSURF)
    for anEnemy in pygame.sprite.Group.sprites(enemies):
        anEnemy.draw(DISPLAYSURF)
         
    pygame.display.update()
    FramePerSec.tick(FPS)