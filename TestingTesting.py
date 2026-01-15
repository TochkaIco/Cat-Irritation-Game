#______ Adam Ohlsén
#
#Btw do you guys do snake_case, CamelCase or kebab-case?
#Im a bit inconsistent but i will try to adjust to you guys
#I will insert the simple pygame necesseties, you should know what they are

#imports
import pygame

##pygame necessities
#{
#basics --
pygame.init()
screen = pygame.display.set_mode((1024,512))
clock = pygame.time.Clock()
DeltaTime = 0.1
#sprites --
# cm- Roman you will be a placeholder for everything
Roman = pygame.image.load("Roman-Verde.png").convert_alpha()
#}

###LogicAspects
#Global variables
Running = True

Default_Objects = []
Scene = "MainScene"
LoadedScene = False

#Global Functions
def Rotate(obj):
    obj.pic = pygame.transform.rotate(obj.OriginPic, obj.PicAngle)

#Classes
class Player:
    Player_Class_Picture = Roman
    def __init__(self,x,y):
        #______ Adam Ohlsén
        #Do you guys want to use a tuple instead of a seperate x and y?
        #X
        self.x = x
        self.xvelocity = 0
        #Y
        self.y = y
        self.yvelocity = 0
        #Misc
        self.OriginPic = Player.Player_Class_Picture
        self.pic = self.OriginPic
        self.Hitbox = self.OriginPic.get_rect(center= (self.x,self.y))
        self.PicAngle = 0
        #do last
        Default_Objects.append(self)

        

#Misc
DefaultPlayer = Player(256,256)

while Running == True:
    PyEvents = pygame.event.get()
    for event in PyEvents:
        if event.type == pygame.QUIT:
            Running = False
    screen.fill((255,255,255))
    #______ Adam Ohlsén
    #don't put logic inside of running before this point unless you are certain
    #Scenes
    if Scene == "MainScene":
        if LoadedScene == False:
            print ("loading scene")
            LoadedScene = True
        
        #______ Adam Ohlsén
        #Do you guys want to instantiate Default_objects and have all the logic
        #run through global functions instead of class functions?
        # Like this:
        for obj in range(len(Default_Objects)):
            Rotate(Default_Objects[obj])
            screen.blit(Default_Objects[obj].pic, Default_Objects[obj].Hitbox )

    #______ Adam Ohlsén
    #don't put logic past this point unless you are certain
    DeltaTime = clock.tick(60) / 1000
    DeltaTime = max(0.001, min(0.1, DeltaTime))
    pygame.display.flip()


pygame.display.quit()
pygame.quit()
