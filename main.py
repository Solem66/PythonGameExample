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

# Game configuration
PLAYER_PACE = 4
ENEMY_PACE = 2
SPAWN_INTERVAL = 3000

# Other variables
SCORE = 0
RUNNING = True

# Set up game board
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Create a custom event for adding a new enemy
ADD_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, SPAWN_INTERVAL)

# Create a custom event for score update
UPDATE_SCORE = ADD_ENEMY + 1
pygame.time.set_timer(UPDATE_SCORE, 200)

# Set up Fonts
font = pygame.font.SysFont("Georgia", 60)
font_score = pygame.font.SysFont("Georgia", 20)
game_over = font.render("Game Over", True, BLACK)

# Object classes
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

# Initialize game
player = Player()
E1 = Enemy()
enemies = pygame.sprite.Group()
enemies.add(E1)

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                RUNNING = not(RUNNING)
        
        if RUNNING:
            if event.type == ADD_ENEMY:
                numToAdd = SCORE // 50 + 1
                for i in range(numToAdd):
                    newEnemy = Enemy()
                    enemies.add(newEnemy)
            elif event.type == UPDATE_SCORE:
                SCORE += 1

    if RUNNING:
        # Move objects
        enemies.update(player)
        player.update()

        # Playser is caught - reset the game and pause
        if pygame.sprite.spritecollideany(player, enemies):
            DISPLAYSURF.blit(game_over, (150, 150))
            for anEnemy in enemies:
                anEnemy.kill()
            player.rect.center = (300, 300)
            E1 = Enemy()
            enemies.add(E1)
            SCORE = 0
            RUNNING = False
            pygame.display.update()
            continue
        
        # Draw everything
        DISPLAYSURF.fill(WHITE)
        player.draw(DISPLAYSURF)
        for anEnemy in enemies:
            anEnemy.draw(DISPLAYSURF)
        scores = font_score.render(str(SCORE), True, BLACK)
        DISPLAYSURF.blit(scores, (10, 10))
        pygame.display.update()

    # Wait util next frame
    FramePerSec.tick(FPS)