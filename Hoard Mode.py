import pygame, sys, random, time
from pygame.locals import *


##Initialisation
pygame.init()
pygame.display.set_caption("Hoard mode")

#Colours
black = (0, 0, 0)
white = (255, 255, 255)
blue = (50, 50, 255)

#Screen
width = 1600
height = 900
screen = pygame.display.set_mode((width, height))

#Clock/time
clock = pygame.time.Clock()

#Font
pygame.font.init()

##Background Variables
#Images
playerImg = pygame.image.load("playerCharacterRun1.png")
playerImg = pygame.transform.scale(playerImg, (50, 40))

enemyImg = pygame.image.load("enemy.png")

pistolBullet = pygame.image.load("pistol.png")
pistolBullet = pygame.transform.scale(pistolBullet, (5, 5))



##Classes
#Player
class Player(pygame.sprite.Sprite):

    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerImg
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.centery = height / 2
        self.speedx = 0
        self.speedy = 0

        self.angle = 0

    def update (self):
        #Movement
        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()
        
        if keystate[K_a]:
                self.speedx = -3
        if keystate[K_d]:
                self.speedx = 3
        if keystate[K_w]:
                self.speedy = -3
        if keystate[K_s]:
                self.speedy = 3

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > width:
                self.rect.right = width
        if self.rect.left < 0:
                self.rect.left = 0

        if self.rect.bottom > height:
                self.rect.bottom = height
        if self.rect.top < 0:
                self.rect.top = 0

        #Rotation
        from math import atan2, degrees
        
        mousePos = pygame.mouse.get_pos()
        dx = self.rect.centerx - mousePos[0]
        dy = self.rect.centery - mousePos[1]
        deg = degrees(atan2(-dy,dx))
        
        if self.angle != deg:
            self.image = pygame.transform.rotate(playerImg, deg + 180)
            
            self.angle = deg

        


class Guard(pygame.sprite.Sprite):

    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemyImg
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint (0, 1600)
        self.rect.centery = random.randint (0, 900)
        

    def update (self):
        #Movement
        targetX = player.rect.centerx
        targetY = player.rect.centery

        from math import atan2, cos, sin
        
        angle = atan2((targetY - self.rect.centery), (targetX - self.rect.centerx))
        moveDx = 2 * cos(angle)
        moveDy = 2 * sin(angle)

        self.rect.centerx += moveDx
        self.rect.centery += moveDy
        

        
    
    


    
    
            
        
class Pistol(pygame.sprite.Sprite):

    def __init__ (self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pistolBullet
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.mousePos = pygame.mouse.get_pos()
        

        #Sets up direction for shot
        from math import atan2, cos, sin
        
        angle = atan2((self.mousePos[1] - self.rect.centery), (self.mousePos[0] - self.rect.centerx))
        self.bulletDx = 10 * cos(angle)
        self.bulletDy = 10 * sin(angle)

    def update(self):
        self.rect.centerx += self.bulletDx
        self.rect.centery += self.bulletDy
        

    
        



        

##Frontend variables
#Sprite lists
all_sprites_list = pygame.sprite.Group()


#Player
player = Player()
all_sprites_list.add(player)

#Enemies
enemies = pygame.sprite.Group()

for i in range(6):
        g = Guard()
        enemies.add(g)
        all_sprites_list.add(g)

#Bullets/guns
bullets = pygame.sprite.Group()
bulletTime = time.time() - 0.5

##Game loop
while True:

    clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit

    #Sprites list updates
    all_sprites_list.update()

    #Draw
    screen.fill(black)
    all_sprites_list.draw(screen)


    
    mouse = pygame.mouse.get_pressed()
    
    #Fire pistol bullets
    if mouse[0] == True and time.time() - bulletTime > 0.2:
        bullet = Pistol(player.rect.centerx, player.rect.centery)
        bullets.add(bullet)
        all_sprites_list.add(bullet)

        

        bulletTime = time.time()


    
        
        

    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        g = Guard()
        enemies.add(g)
        all_sprites_list.add(g)
        
        




        
    pygame.display.flip()











                

