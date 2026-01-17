#______ Adam Ohlsén
#
#Btw do you guys do snake_case, CamelCase or kebab-case?
#Im a bit inconsistent but i will try to adjust to you guys
#I will insert the simple pygame necesseties, you should know what they are

#imports
import pygame
from math import atan2,cos,sin,radians,sqrt,pow #atan 2 hehehehehaw, grrrr, heugheugh

print(f"pygame version is: {pygame.version.ver}")
##pygame necessities
#{
#basics --
pygame.init()
screen = pygame.display.set_mode((1024,512),pygame.RESIZABLE)
clock = pygame.time.Clock()
DeltaTime = 0.1
#sprites --
# cm- Roman you will be a placeholder for everything
Roman = pygame.image.load("Images/Roman-Verde.png").convert_alpha()
Roman = pygame.transform.scale_by(Roman,0.3)
#}

###LogicAspects
#{
##Global variables
#{
Running = True

Default_Objects = []
Scene = "MainScene"
LoadedScene = False

Extra_Pixel_Margin = 2

#Layers__--__
PlayerLayer = []
WallLayer = []

#}
#Global Functions
#DONT USE THE RAYCAST YET!!! IT IS DESPICABLE!!!
def RayCast(OriginX,OriginY,TargetX,TargetY,CollisionLayers):
    direction = atan2(TargetY - OriginY, TargetX - OriginX)
    x = OriginX
    y = OriginY
    Length = sqrt(pow(OriginX - TargetX,2) + pow(OriginY - TargetY,2))
    ray_length = 0
    debug_iterations = 0
    xrate = -cos(radians(direction - 90))
    yrate = sin(radians(direction - 90))
    while ray_length < Length:
        x += 1 * xrate
        y += 1 * yrate
        for obj in range(len(CollisionLayers)):
            if pygame.Rect.collidepoint(CollisionLayers[obj].Hitbox, (x,y)):
                return x,y
        ray_length += 5
        debug_iterations += 1
    print (debug_iterations)
    return None,None


    pass

def Rotate(obj):
    obj.pic = pygame.transform.rotate(obj.OriginPic, obj.PicAngle)
def Move(obj):
    obj.x += obj.xvelocity * DeltaTime
    obj.y += obj.yvelocity * DeltaTime
    obj.Hitbox = obj.OriginPic.get_rect(center= (obj.x, obj.y))


def CollisionCheck(obj):
    for object in range(len(obj.InteractLayers)):
        if obj.Hitbox.colliderect(obj.InteractLayers[object].Hitbox):
            print (f"InteractLayers:{len(obj.InteractLayers)}")
            CorrectXPosition(obj,obj.InteractLayers[object])
            pass


def CorrectXPosition(obj1, obj2):
    width1 = obj1.OriginPic.get_width()
    height1 = obj1.OriginPic.get_height()
    width2 = obj2.OriginPic.get_width()
    height2 = obj2.OriginPic.get_height()
    XAdjustment = width2 / 2 + width1 / 2
    YAdjustment = height2 / 2 + height1 / 2

    if obj1.x > obj2.x and obj2.y + YAdjustment - Extra_Pixel_Margin * 5 > obj1.y > obj2.y - YAdjustment + Extra_Pixel_Margin * 5:
        obj1.x = obj2.x + XAdjustment
    if obj1.x < obj2.x and obj2.y + YAdjustment - Extra_Pixel_Margin * 5 > obj1.y > obj2.y - YAdjustment + Extra_Pixel_Margin * 5:
        obj1.x = obj2.x - XAdjustment
    pass

def CorrectYPosition(obj1, obj2):
    pass

#Classes
class Player:
    Player_Class_Picture = Roman
    def __init__(self,x,y):
        #______ Adam Ohlsén
        self.WalkSpeed = 100
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
        self.Layer = "PlayerLayer"
        self.InteractLayers = WallLayer
        
        #Put all __init__ logic before the append
        Default_Objects.append(self)
        PlayerLayer.append(self)

    def Control_Player(self):
        for event in PyEvents:
            #-                                      -#
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.yvelocity += -self.WalkSpeed
                if event.key == pygame.K_s:
                    self.yvelocity += self.WalkSpeed
                if event.key == pygame.K_a:
                    self.xvelocity += -self.WalkSpeed
                if event.key == pygame.K_d:
                    self.xvelocity += self.WalkSpeed
            #-                                      -#
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.yvelocity -= -self.WalkSpeed
                if event.key == pygame.K_s:
                    self.yvelocity -= self.WalkSpeed
                if event.key == pygame.K_a:
                    self.xvelocity -= -self.WalkSpeed
                if event.key == pygame.K_d:
                    self.xvelocity -= self.WalkSpeed    

class Wall:
    Wall_Class_Picture = Roman
    def __init__(self,x,y):
        #X and Y
        self.x = x
        self.y = y

        #Misc
        self.OriginPic = Wall.Wall_Class_Picture
        self.pic = self.OriginPic
        self.Hitbox = self.OriginPic.get_rect(center= (self.x,self.y))
        self.PicAngle = 0
        self.Layer = "WallLayer"

        Default_Objects.append(self)
        WallLayer.append(self)

    
    
#}


#Misc
DefaultPlayer = Player(256,256)
tempthing = 1024

while Running == True:
    #tempthing -= 1
    #screen = pygame.display.set_mode((tempthing,512),pygame.RESIZABLE)
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
            Wall(500, 100)
            LoadedScene = True
        #-
        
        DefaultPlayer.Control_Player()
        for obj in range(len(Default_Objects)):
            Rotate(Default_Objects[obj])
            screen.blit(Default_Objects[obj].pic, Default_Objects[obj].Hitbox) 
            if Default_Objects[obj].Layer != "WallLayer":         
                Move(Default_Objects[obj])
            if Default_Objects[obj].Layer != "WallLayer":
                CollisionCheck(Default_Objects[obj])

    #______ Adam Ohlsén
    #don't put logic past this point unless you are certain
    DeltaTime = clock.tick(60) / 1000
    DeltaTime = max(0.001, min(0.1, DeltaTime))
    print("meow")
    pygame.display.flip()


pygame.display.quit()
pygame.quit()
