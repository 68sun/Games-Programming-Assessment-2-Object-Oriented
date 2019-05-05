import pygame, sys, random, time
from pygame.locals import *


##Initialisation
pygame.init()
pygame.display.set_caption("Hoard mode")

#Colours
black = (0, 0, 0)
white = (255, 255, 255)
blue = (50, 50, 255)
green = (128, 249, 22)
red = (249, 25, 21)


#Screen
width = 1600
height = 900
screen = pygame.display.set_mode((width, height))

#Clock/time
clock = pygame.time.Clock()

#Font
pygame.font.init()
font = pygame.font.SysFont ("arial", 20)

##Background Variables
#Images
playerImg = pygame.image.load("playerCharacterRun1.png").convert_alpha()
playerImg = pygame.transform.scale(playerImg, (50, 40))

enemyImg = pygame.image.load("enemy.png")
enemyImg= pygame.transform.scale(enemyImg, (256, 256)).convert_alpha()

pistolBullet = pygame.image.load("pistol.png").convert_alpha()
pistolBullet = pygame.transform.scale(pistolBullet, (5, 5))

medkitImg = pygame.image.load("medkit.png").convert_alpha()
medkitImg = pygame.transform.scale(medkitImg, (64, 32))



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
        self.stopped = False
        

    def update (self):
        #Movement
        targetX = player.rect.centerx
        targetY = player.rect.centery

        from math import atan2, cos, sin, degrees

        if self.stopped == False:
            
            angle = atan2((targetY - self.rect.centery), (targetX - self.rect.centerx))
            moveDx = 2 * cos(angle)
            moveDy = 2 * sin(angle)

            self.rect.centerx += moveDx
            self.rect.centery += moveDy

        #Rotation
        rotateAngle = atan2(-(targetY - self.rect.centery), (targetX - self.rect.centerx))
        deg = degrees(rotateAngle)
        
        if rotateAngle != deg:
            self.image = pygame.transform.rotate(enemyImg, deg)
            
            rotateAngle = deg


        self.stopped = False
    
    

class medkit(pygame.sprite.Sprite):

    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = medkitImg
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint (0, 1600)
        self.rect.centery = random.randint (0, 900)
        self.deleteTimer = time.time()

    def update(self):
        if time.time() - self.deleteTimer >= 15:
            self.kill()

    
    

    
    
            
        
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
        

    
        



        

####Frontend variables
#Health
health = 100
enemyTime = bulletTime = time.time() - 0.5

#Score
score = 0

###Sprite lists
all_sprites_list = pygame.sprite.Group()


##Player
player = Player()
all_sprites_list.add(player)

##Enemies
enemies = pygame.sprite.Group()

for i in range(6):
        g = Guard()
        enemies.add(g)
        all_sprites_list.add(g)

##Bullets/guns
bullets = pygame.sprite.Group()
bulletTime = time.time()


##Pickups
#Pickup timer
pickupTime = time.time() - 0.5

#Medkit
medkits = pygame.sprite.Group()


####Game loop
while True:

    clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit

    #Sprites list updates
    all_sprites_list.update()

    #Draw
    screen.fill(blue)
    all_sprites_list.draw(screen)

    #Health
    if health > 25:
        pygame.draw.rect(screen, green, Rect(5, 30, health * 2, 15), 0)
        
    elif health <= 25 and health > 0:
        pygame.draw.rect(screen, red, Rect(5, 30, health * 2, 15), 0)

    elif health <= 0:
        all_sprites_list.remove(player)
        screen.blit(font.render("GAME OVER", True, (90,255,255)), (350,200))
        screen.blit(font.render("SCORE: " + str(score), True, (90,255,255)), (350,250))

    #Score
    screen.blit(font.render("Score: " + str(score), True, (255,255,255)), (5,5))
    

    mouse = pygame.mouse.get_pressed()

    
    
    #Fire pistol bullets
    if mouse[0] == True and time.time() - bulletTime > 0.2:
        bullet = Pistol(player.rect.centerx, player.rect.centery)
        bullets.add(bullet)
        all_sprites_list.add(bullet)
        

        

        bulletTime = time.time()


    
        
        
    #Enemy bullet collision
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True, pygame.sprite.collide_mask)
    for hit in hits:
        g = Guard()
        enemies.add(g)
        all_sprites_list.add(g)
        score += 10

    

    ##Enemy attacks
    #Stops enemy when attacking
    attacks = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask)
    for attack in range(len(attacks)):
        attacks[attack].stopped = True

    
    #Damages player   
    if attacks and time.time() - enemyTime > 0.5:
        health -= 10
        print(health)
        
        enemyTime = time.time()
    
        

    ##Player pickups
    if time.time() - pickupTime  >= 10:
        p = medkit()
        medkits.add(p)
        all_sprites_list.add(p)

        pickupTime = time.time()

    #Medkit pickup/heal
    heals = pygame.sprite.spritecollide(player, medkits, True, pygame.sprite.collide_mask)
    if heals:
        health = 100


        
    pygame.display.flip()











                

