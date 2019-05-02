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
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))

#Clock/time
clock = pygame.time.Clock()

#Font
pygame.font.init()

##Background Variables
#Images
playerImg = pygame.image.load("playerCharacterRun1.png")
playerImg.set_colorkey((255,255,255))


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
                self.speedx = -5
        if keystate[K_d]:
                self.speedx = 5
        if keystate[K_w]:
                self.speedy = -5
        if keystate[K_s]:
                self.speedy = 5

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
            self.image = pygame.transform.rotate(playerImg, deg + 90)
            self.angle = deg
            
        
class Pistol():

    def __init__ (self, x, y):
        self.x = x
        self.y = y
        self.mousePos = pygame.mouse.get_pos()

        #Sets up direction for shot
        from math import atan2, cos, sin
        
        angle = atan2((self.mousePos[1] - self.y), (self.mousePos[0] - self.x))
        self.bulletDx = 10 * cos(angle)
        self.bulletDy = 10 * sin(angle)

    def draw (self):
        pygame.draw.rect (screen, (255,255,255), Rect(self.x, self.y, 10, 10), 0)
        

    def move (self):
        self.x += self.bulletDx
        self.y += self.bulletDy
        

##Frontend variables
#Sprite lists
all_sprites_list = pygame.sprite.Group()


#Player
player = Player()
all_sprites_list.add(player)

#Bullets/guns
bullets = []
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


    
    
    
    #Fire pistol bullets
    if event.type == pygame.MOUSEBUTTONDOWN and time.time() - bulletTime > 0.5:
        bullets.append(Pistol(player.rect.centerx, player.rect.centery))

        

        bulletTime = time.time()

    b = 0
    while b < len(bullets):
        bullets[b].draw()

        bullets[b].move()

        b += 1




        
    pygame.display.flip()











                

