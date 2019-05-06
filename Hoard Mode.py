import pygame, sys, random, time
from pygame.locals import *


##Initialisation
pygame.init()
pygame.display.set_caption("Hoard mode")

#Music initialise
pygame.mixer.pre_init(44100, - 16, 2, 2048)

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
screenReset = pygame.display.set_mode((width, height))

#Clock/time
clock = pygame.time.Clock()

#Font
pygame.font.init()
font = pygame.font.SysFont ("arial", 20)

####Background Variables
###Images
##Player
playerImg = pygame.image.load("playerCharacterRun1.png").convert_alpha()
playerImg = pygame.transform.scale(playerImg, (50, 40))

##Enemy
enemyImg = pygame.image.load("enemy.png")
enemyImg= pygame.transform.scale(enemyImg, (256, 256)).convert_alpha()

##Bullets
#Pistol
pistolBullet = pygame.image.load("bullet.png").convert_alpha()
pistolBullet = pygame.transform.scale(pistolBullet, (5, 5))

#Shotgun
shotgunBullet = pygame.image.load("bullet.png").convert_alpha()
shotgunBullet = pygame.transform.scale(shotgunBullet, (10, 10))

#Flamethrower
flamethrowerBullet = pygame.image.load("fire.png").convert_alpha()
flamethrowerBullet = pygame.transform.scale(flamethrowerBullet, (16, 22))

##Pickups
#Medkit
medkitImg = pygame.image.load("medkit.png").convert_alpha()
medkitImg = pygame.transform.scale(medkitImg, (64, 32))

#Shotgun
shotgunPickup = pygame.image.load("shotgunPickup.png").convert_alpha()
shotgunPickup = pygame.transform.scale(shotgunPickup, (64, 32))

#Flamethrower
flamethrowerPickup = pygame.image.load("flamethrowerPickup.png").convert_alpha()
flamethrowerPickup =pygame.transform.scale(flamethrowerPickup, (64, 32))


##Sound
#Background music
pygame.mixer.music.load('background.wav')
background = pygame.mixer.Sound("background.wav")


#Pistol
pygame.mixer.music.load("pistol.wav")
pistolSound = pygame.mixer.Sound("pistol.wav")

#Shotgun
pygame.mixer.music.load("shotgun.wav")
shotgunSound = pygame.mixer.Sound("shotgun.wav")

#Flamethrower
pygame.mixer.music.load("flamethrower.ogg")
flamethrowerSound = pygame.mixer.Sound("flamethrower.ogg")

#Pickup
pygame.mixer.music.load("pickup.wav")
pickupSound = pygame.mixer.Sound("pickup.wav")

#Enemy hit sound
pygame.mixer.music.load("enemy.wav")
enemySound = pygame.mixer.Sound("enemy.wav")

#Player hit sound
pygame.mixer.music.load("player.wav")
playerSound = pygame.mixer.Sound("player.wav")



###Classes
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

        

##Enemies
#Guard class
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
    
    
##Pickup classes
#Medkit class
class medkit(pygame.sprite.Sprite):

    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = medkitImg
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint (100, 1500)
        self.rect.centery = random.randint (100, 700)
        self.deleteTimer = time.time()

    def update(self):
        if time.time() - self.deleteTimer >= 15:
            self.kill()


#Shotgun pickup class
class shotPickup(pygame.sprite.Sprite):

    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = shotgunPickup
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint (100, 1500)
        self.rect.centery = random.randint (100, 700)
        self.deleteTimer = time.time()

    def update(self):
        if time.time() - self.deleteTimer >= 15:
            self.kill()


#Flamethrower pickup class
class flamePickup(pygame.sprite.Sprite):

    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = flamethrowerPickup
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint (100, 1500)
        self.rect.centery = random.randint (100, 700)
        self.deleteTimer = time.time()

    def update(self):
        if time.time() - self.deleteTimer >= 15:
            self.kill()
    
    

    
    
##Gun/ bullet classes
#Pistol gun class        
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

        #Destroys when leaving screen
        if self.rect.centerx < 0 or self.rect.centerx > width or self.rect.centery < 0 or self.rect.centery > height:
            self.kill()
        
#Shotgun gun class
class Shotgun(pygame.sprite.Sprite):

    def __init__ (self, x, y, spread):
        pygame.sprite.Sprite.__init__(self)
        self.image = shotgunBullet
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.mousePos = pygame.mouse.get_pos()

        #Holds degree for spreadout shotgun shots
        self.spread = spread

        #Sets up direction for shot
        from math import atan2, cos, sin
        
        angle = atan2((self.mousePos[1] - self.rect.centery), (self.mousePos[0] - self.rect.centerx))
        self.bulletDx = 10 * cos(angle + self.spread)
        self.bulletDy = 10 * sin(angle + self.spread)

    def update(self):
        self.rect.centerx += self.bulletDx
        self.rect.centery += self.bulletDy

        #Destroys when leaving screen
        if self.rect.centerx < 0 or self.rect.centerx > width or self.rect.centery < 0 or self.rect.centery > height:
            self.kill()
        
#Flamethrower gun class
class Flamethrower(pygame.sprite.Sprite):

    def __init__ (self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = flamethrowerBullet
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.mousePos = pygame.mouse.get_pos()

        #Flame destruction variable
        self.flameTime = time.time()
        

        #Sets up direction for shot
        from math import atan2, cos, sin
        
        angle = atan2((self.mousePos[1] - self.rect.centery), (self.mousePos[0] - self.rect.centerx))
        self.bulletDx = 3 * cos(angle)
        self.bulletDy = 3 * sin(angle)

    def update(self):
        self.rect.centerx += self.bulletDx
        self.rect.centery += self.bulletDy

        #Destroys when leaving screen
        if self.rect.centerx < 0 or self.rect.centerx > width or self.rect.centery < 0 or self.rect.centery > height:
            self.kill()

        #Destroys after certain amount of time
        if time.time() - self.flameTime > 1:
            self.kill()

        

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

#Waves
wave = 1
newWave = True

#Break between waves
waveBreakTime = time.time()


##Bullets/guns
bullets = pygame.sprite.Group()
bulletTime = time.time()

#Gun type variable
gunType = 1

#Ammo
shotgunAmmo = 0
flameAmmo = 0


##Pickups
#Pickup timer
pickupTime = time.time() - 10

#Medkit
medkits = pygame.sprite.Group()

#Shotguns
shotguns = pygame.sprite.Group()

#Flamethrowers
flamethrowers = pygame.sprite.Group()

##Sound
background.play(loops = -1)
background.set_volume(0.3)

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
    screenReset.fill(blue)
    all_sprites_list.draw(screen)

    #Health
    if health > 25:
        pygame.draw.rect(screen, green, Rect(5, 30, health * 2, 15), 0)
        
    elif health <= 25 and health > 0:
        pygame.draw.rect(screen, red, Rect(5, 30, health * 2, 15), 0)

    #Game end
    elif health <= 0:
        all_sprites_list.remove(player)
        screen.blit(font.render("GAME OVER", True, (90,255,255)), (350,200))
        screen.blit(font.render("SCORE: " + str(score), True, (90,255,255)), (350,250))
        screen.blit(font.render("PRESS R TO RESTART", True, (90,255,255)), (350,300))
        screen.blit(font.render("PRESS ESCAPE TO EXIT", True, (90,255,255)), (350,350))

        ##Restart game
        keystate = pygame.key.get_pressed()

        #Press r to restart
        if keystate[K_r]:

            #Sprite group resets
            all_sprites_list.empty()
            all_sprites_list.clear(screen, screenReset)

            #Resets enemies
            for i in range(6):
                g = Guard()
                enemies.add(g)
                all_sprites_list.add(g)

            

            #Variable resets
            player = Player()
            all_sprites_list.add(player)
            score = 0
            health = 100
            gunType = 1
            wave = 1

        #Press escape to quit
        if keystate[K_ESCAPE]:
            pygame.quit()





    #Score
    screen.blit(font.render("Score: " + str(score), True, (255,255,255)), (5,5))

    #Controls
    screen.blit(font.render("CONTROLS", True, (255,255,255)), (5,760))
    screen.blit(font.render("Left mouse to shoot", True, (255,255,255)), (5,790))
    screen.blit(font.render("WASD to move", True, (255,255,255)), (5,820))
    

    mouse = pygame.mouse.get_pressed()

    
    
    #Fire pistol bullets
    if mouse[0] == True and time.time() - bulletTime > 0.2 and gunType == 1:
        #Play sound
        pistolSound.set_volume(0.4)
        pistolSound.play()
        
        bullet = Pistol(player.rect.centerx, player.rect.centery)
        bullets.add(bullet)
        all_sprites_list.add(bullet)
        

        

        bulletTime = time.time()


    #Fire shotgun bullets
    elif mouse[0] == True and time.time() - bulletTime > 0.6 and gunType == 2 and shotgunAmmo > 0:
        #Play sound
        shotgunSound.play()
        
        #List for spread of additional bullets
        angleSpread = (-0.5, -0.25, 0, 0.25, 0.5)
        

        #Loop to shoot bullets at different angles
        for i in angleSpread:            
            bullet = Shotgun(player.rect.centerx, player.rect.centery, i)
            bullets.add(bullet)
            all_sprites_list.add(bullet)
        

        
        shotgunAmmo -= 1
        bulletTime = time.time()

    #Fire flamethrower
    elif mouse[0] == True and time.time() - bulletTime > 0.1 and gunType == 3 and flamethrowerAmmo > 0:
        #Play sound
        flamethrowerSound.play()

        bullet = Flamethrower(player.rect.centerx, player.rect.centery)
        bullets.add(bullet)
        all_sprites_list.add(bullet)
        

        
        flamethrowerAmmo -= 1
        bulletTime = time.time()


    #Flamethrower sound stop
    if mouse[0] == False or gunType != 3:
        flamethrowerSound.stop()
        




    ##Weapon rest
    if gunType == 2 and shotgunAmmo <= 0:
        gunType = 1

    elif gunType == 3 and flamethrowerAmmo <= 0:
        gunType = 1

    ##Ammo display
    #Shotgun
    if gunType == 2:
        screen.blit(font.render("Shotgun", True, (255,255,255)), (705,10))
        screen.blit(font.render("Ammo: " + str(shotgunAmmo), True, (255,255,255)), (700,30))

    #Flamethrower
    if gunType == 3:
        screen.blit(font.render("Flamethrower", True, (255,255,255)), (705,10))
        screen.blit(font.render("Ammo: " + str(flamethrowerAmmo), True, (255,255,255)), (700,30))

    



    ##Enemies
    #Show wave
    screen.blit(font.render("Wave: " + str(wave), True, (255,255,255)), (5,60))

    ##Spawn enemies
    if newWave == True:
        for i in range(wave*2):
            g = Guard()
            enemies.add(g)
            all_sprites_list.add(g)

        newWave = False
        

        
    #Enemy bullet collision
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True, pygame.sprite.collide_mask)
    for hit in hits:
        #Play sound
        enemySound.play()

        #Increase score
        score += 10

        #Time reset for next wave
        waveBreakTime = time.time()

    #Toggles next wave when all enemies killed
    if not enemies:
        #Displays time to the next wave
        screen.blit(font.render("Time to next wave: ", True, (255,255,255)), (700,60))
        screen.blit(font.render(str(round(5 + (waveBreakTime - time.time()), 2)), True, (255,255,255)), (740,100))
        
        #Starts new wave after break interval
        if time.time() - waveBreakTime > 5:
            wave += 1
            newWave = True
        

    ##Enemy attacks
    #Stops enemy when attacking
    attacks = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask)
    for attack in range(len(attacks)):
        attacks[attack].stopped = True

    
    #Damages player   
    if attacks and time.time() - enemyTime > 0.5:
        #Play sound
        playerSound.play()

        #Reduce health
        health -= 10
        print(health)

        #Reset attack time
        enemyTime = time.time()
    
        

    ##Player pickups
    if time.time() - pickupTime  >= 10:
        #Random int to select pickup
        p = random.randint(1, 3)

        #Medkit
        if p == 1:
            m = medkit()
            medkits.add(m)
            all_sprites_list.add(m)

        #Shotgun
        elif p == 2:
            s = shotPickup()
            shotguns.add(s)
            all_sprites_list.add(s)

        elif p == 3:
            f = flamePickup()
            flamethrowers.add(f)
            all_sprites_list.add(f)
        
        
        #Reset pickup spawn time
        pickupTime = time.time()

    #Medkit pickup/heal
    heals = pygame.sprite.spritecollide(player, medkits, True, pygame.sprite.collide_mask)
    if heals:
        #Play sound
        pickupSound.play()

        #Heal player
        health = 100


    #Shotgun pickup
    spread = pygame.sprite.spritecollide(player, shotguns, True, pygame.sprite.collide_mask)
    if spread:
        #Play sound
        pickupSound.play()
        
        #Change gun type and set ammo
        gunType = 2
        shotgunAmmo = 20

     


    #Flamethrower pickup
    fire = pygame.sprite.spritecollide(player, flamethrowers, True, pygame.sprite.collide_mask)
    if fire:
        #Play sound
        pickupSound.play()
        
        #Change gun type and set ammo
        gunType = 3
        flamethrowerAmmo = 100

        
    pygame.display.flip()











                

