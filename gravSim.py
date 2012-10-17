#gravSim.py

import pygame
import math

frame_count = -1
WIDTH=640
HEIGHT=480
Quit = False

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Gravity Sim')
objects_group = pygame.sprite.Group()
clock = pygame.time.Clock()

class Object(): #where the magic happens. Ideally there need only be one class for all of the objects in the game; saves code and makes things MUCH more simple.
    def __init__(self,location = [0,0]):
        self.mass = 10
        self.location = location
        self.velocityX = 0.0
        self.velocityY = 0.0
        self.forceX = 0.0
        self.forceY = 0.0
        self.size = (10,10)
        self.downward_gravity = 1
        self.makeSprite()
    
    def checkLocation(self):
        if self.sprite.rect.left < 0 or self.sprite.rect.right > WIDTH:
            self.velocityX *= -1
        if self.sprite.rect.top < 0 or self.sprite.rect.bottom > HEIGHT:
            self.velocityY *= -1
        
        
    def makeSprite(self):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load('purple_circle.gif')
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.left = self.location[0]
        self.sprite.rect.top = self.location[1]
        #pygame.transform.scale(self.sprite.image,self.size)
        objects_group.add(self.sprite)
        
    def tick(self):
        self.checkLocation()                 #Check Location, adjust force if needed.
        self.forceY += self.downward_gravity #Add downward gravity to force.
        #Calculate Velocity from force.
        #v = u + at ==> v = u + F/m
        self.velocityX = self.velocityX + (self.forceX / self.mass)
        self.velocityY = self.velocityY + (self.forceY / self.mass)
        
        #Move Object
        self.sprite.rect.left += self.velocityX * delta_time/10
        self.sprite.rect.top += self.velocityY * delta_time/10
        
        #Reset Force
        self.forceX = 0.0
        self.forceY = 0.0
    def poke(self,force,angle):
        print "Poke!"
        #Adds a force to the object.
        if angle <0:
            return
        elif angle == 0:
            self.forceY += force * -1
        elif angle < 90:
            self.forceY += math.cos(math.radians(angle))
            self.forceX += math.sin(math.radians(angle))
        elif angle == 90:
            self.forceX += force
        elif angle <180:
            self.forceX += math.cos(math.radians(angle-90))
            self.forceY += math.sin(math.radians(angle-90))
        elif angle == 180:
            self.forceY += force
        elif angle <270:
            self.forceY += math.cos(math.radians(angle-180)) * -1
            self.forceX += math.sin(math.radians(angle-180)) * -1
        elif angle == 270:
            self.forceX += force * -1
        elif angle <360:
            self.forceX += math.cos(math.radians(angle-270)) * -1
            self.forceY += math.sin(math.radians(angle-270)) * -1
        else:
            return

        
ball = Object([10,400])
while Quit != True:
    delta_time = clock.tick_busy_loop(100)
    frame_count += 1
    #QUIT SEQUENCE
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            Quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.poke(10,0)
            if event.key == pygame.K_DOWN:
                ball.poke(10,180)
            if event.key == pygame.K_RIGHT:
                ball.poke(10,90)
            if event.key == pygame.K_LEFT:
                ball.poke(10,270)
    
    #ACTION SEQUENCE
    ball.tick()
    
    #DRAW SEQUENCE
    if frame_count % 20 == 0:
        text_image = pygame.font.Font(None,20).render(str(int(clock.get_fps())), True, (0,0,0))
        text_rect = text_image.get_rect(right = WIDTH - 5,centery=10)
    
    screen.blit(text_image,text_rect)
    objects_group.draw(screen)
    pygame.display.update()
    screen.fill((200,200,200))
