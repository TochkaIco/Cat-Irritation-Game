#Ok, i finally understand git, you were both horrible teachers...

#I will insert the simple pygame necesseties, you should know what they are

#imports
import pygame

##pygame necessities
#{
#basics --
pygame.init()
screen = pygame.display.set_mode((512,512))
clock = pygame.time.Clock()
DeltaTime = 0.1
#sprites --
# cm- Roman you will be a placeholder for everything
Roman = pygame.image.load("Roman-Verde.png").convert_alpha()
#}

###LogicAspects
#Global variables

#Global Functions

#Classes

Running = True

while Running == True:
    PyEvents = pygame.event.get()
    for event in PyEvents:
        if event.type == pygame.QUIT:
            Running = False
    screen.fill((255,255,255))
    #don't put logic inside of running before this point unless you are certain
    #_<<>>
    screen.blit(Roman,(0,0))



    #don't put logic past this point unless you are certain
    DeltaTime = clock.tick(60) / 1000
    DeltaTime = max(0.001, min(0.1, DeltaTime))
    pygame.display.flip()


pygame.display.quit()
pygame.quit()
