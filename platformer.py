#Imports 
import pygame,sys
from pygame.locals import *
import random
import time
 
pygame.init()

#colors
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
white = (255,255,255)
black = (0,0,0)

#fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)


#consistant variables
vec = pygame.math.Vector2  # 2 for two dimensional
SCREEN_HEIGHT = 450
SCREEN_WIDTH = 400
#movement variables
ACC = 0.7
FRIC = -0.15
#Sets up fps 
FPS = 60
CLOCK = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("platformer_Player_Amazon1.png") 
        self.rect = self.surf.get_rect()
        
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
        self.score = 0

    def move(self):
        self.acc = vec(0,0.5)
 
        pressed_keys = pygame.key.get_pressed()
        #Key press and result
        if pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_d]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #boundaries
        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH
            
        self.rect.midbottom = self.pos

    #finally an easy way to program jumping
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15
            
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if P1.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:
                        hits[0].point = False
                        self.score +=1            
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
                

#platform class
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100),12))
        self.surf.fill(red)
        self.rect = self.surf.get_rect(center = (random.randint(0,SCREEN_WIDTH-10),random.randint(0, SCREEN_HEIGHT-30)))
        self.moving = True
        self.point= True
        self.speed = random.randint(-1, 1)

    #for if and when the platforms move?
    def move(self):
         if self.moving == True:  
            self.rect.move_ip(self.speed,0)
            if self.speed > 0 and self.rect.left > SCREEN_WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = SCREEN_WIDTH

#groupies are to store all the platforms
def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False

def plat_gen():
    while len(platforms) < 7 :
        width = random.randrange(50,100)
        p  = platform() 
        C = True
        while C:
            p= platform()            
            p.rect.center = (random.randrange(0, SCREEN_WIDTH - width),random.randrange(-43, 0))
            C = check(p, platforms)

        platforms.add(p)
        all_sprites.add(p)


#allows for class calling
PT1 = platform()
P1 = Player()

#more platforms!
PT1.surf = pygame.Surface((SCREEN_WIDTH, 20))
PT1.surf.fill((red))
PT1.rect = PT1.surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT - 10))

#adds and helps create all sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

#adds and helps creats all platform sprites
platforms = pygame.sprite.Group()
platforms.add(PT1)

#platforms and moving
PT1.moving = False
PT1.point = False


#creates platforms out side of game loop 
for x in range(random.randint(5, 6)): #added 5,6 for more variation
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)

#game loop
while True:
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                P1.cancel_jump()

        if P1.rect.top > SCREEN_HEIGHT:
            for entity in all_sprites:
                entity.kill()
                time.sleep(1)
                displaysurface.fill(red)
                displaysurface.blit(g, (SCREEN_WIDTH/2, 10))

                pygame.display.update()
                time.sleep(1)
                pygame.quit()
                sys.exit()


    
    #creates endless platforms
    if P1.rect.top <= SCREEN_HEIGHT / 3: #generates platforms above the player
        P1.pos.y += abs(P1.vel.y) 
        for plat in platforms: #updates the player position
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= SCREEN_HEIGHT: #destroys past platforms
                plat.kill()
    displaysurface.fill(black)
    f = pygame.font.SysFont("Verdana", 20)
    g  = f.render(str(P1.score), True, white)
    displaysurface.blit(g, (SCREEN_WIDTH/2, 10))

    #updates before next frame
    plat_gen()
    P1.move()

    #movement and character image adding
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move
 
    pygame.display.update()
    CLOCK.tick(FPS)