#______ Adam Ohlsén
#
#Btw do you guys do snake_case, CamelCase or kebab-case?
#Im a bit inconsistent but i will try to adjust to you guys
#I will insert the simple pygame necesseties, you should know what they are

#imports
import pygame
#map generation import
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from matplotlib.path import Path

##pygame necessities
#{
#basics --
pygame.init()
screen = pygame.display.set_mode((1920,1080),pygame.RESIZABLE)
pygame.display.set_caption("Cat-Irritation-Game")
clock = pygame.time.Clock()
DeltaTime = 0.1

#bg_loading
screen.fill((0, 0, 0))
font = pygame.font.Font(None, 74)
loading_text = font.render("Loading...", True, (255, 255, 255))
text_rect = loading_text.get_rect(center=(1920/2, 1080/2))
screen.blit(loading_text, text_rect)
pygame.display.flip()

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

#Layers__--__
PlayerLayer = []
WallLayer = []

#Camera
CameraX = 0
CameraY = 0

#}
#Global Functions
def RayCast(OriginX,OriginY,TargetX,TargetY,CollisionLayers):

    pass

def Rotate(obj):
    obj.pic = pygame.transform.rotate(obj.OriginPic, obj.PicAngle)
def Move(obj):
    obj.x += obj.xvelocity * DeltaTime
    obj.y += obj.yvelocity * DeltaTime
    obj.Hitbox = obj.OriginPic.get_rect(center= (obj.x, obj.y))


def GetExactCollidePoint(obj1,obj2):
    pass
def CollisionCheck(obj):
    if obj.Layer == "PlayerLayer":
        for object in range(len(WallLayer)):
            if obj.Hitbox.colliderect(WallLayer[object].Hitbox):
                pass

#Managing camera to hold the player always in the middle
def UpdateCamera(target, camera_smoothness=0.1):
    global CameraX, CameraY

    target_x = target.x - 1920/2
    target_y = target.y - 1080/2

    CameraX += (target_x - CameraX) * camera_smoothness
    CameraY += (target_y - CameraY) * camera_smoothness

def CorrectXPosition(obj1, obj2):
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

#BG_Gen
def Generate_Island_BG():
    SIZE = 2048

    #Spaming to the system, to prevent "No response"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #Dots Generation
    np.random.seed()
    n = 15
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    points = []
    for a in angles:
        r = 0.8 + (np.random.rand() - 0.5) * 0.25
        points.append([r * np.cos(a), r * np.sin(a)])
    points = np.array(points)

    #Making the border smooth by generating 150 extra points
    pts_closed = np.vstack([points, points[0]])
    t = np.arange(len(pts_closed))
    t_smooth = np.linspace(0, len(points)-1, 150)
    cs_x = CubicSpline(t, pts_closed[:, 0], bc_type='periodic')
    cs_y = CubicSpline(t, pts_closed[:, 1], bc_type='periodic')
    sx, sy = cs_x(t_smooth), cs_y(t_smooth)

    #Filling an island
    px = ((sx + 1) * SIZE / 2).astype(int)
    py = ((sy + 1) * SIZE / 2).astype(int)
    path = Path(np.column_stack([px, py]))
    y, x = np.mgrid[0:SIZE, 0:SIZE]
    mask = path.contains_points(np.column_stack([x.ravel(), y.ravel()]))
    mask = mask.reshape(SIZE, SIZE)

    #Creating an image
    img = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
    img[~mask] = [25, 76, 204]     #Water  (blue)
    img[mask] = [25, 153, 51]      #Ground (green)

    #Converting to an PyGame Surface
    img = np.transpose(img, (1, 0, 2))
    return pygame.surfarray.make_surface(img)

#Generating BG
IslandBackground = Generate_Island_BG()


#Misc
DefaultPlayer = Player(512,512)
tempthing = 1024

while Running == True:
    tempthing -= 1

    ##! DELETE AFTER! In a minute there will be 3600 walls!
    #Wall(tempthing, 100)

    #screen = pygame.display.set_mode((tempthing,512),pygame.RESIZABLE)
    PyEvents = pygame.event.get()
    for event in PyEvents:
        if event.type == pygame.QUIT:
            Running = False
    #______ Adam Ohlsén
    #don't put logic inside of running before this point unless you are certain
    #Scenes
    if Scene == "MainScene":
        if LoadedScene == False:
            print ("loading scene")
            LoadedScene = True
        #-
        
        DefaultPlayer.Control_Player()
        UpdateCamera(DefaultPlayer, camera_smoothness=0.15)
        screen.blit(IslandBackground, (-CameraX, -CameraY))
        for obj in Default_Objects:
            Rotate(obj)
            screen_x = obj.x - CameraX
            screen_y = obj.y - CameraY
            screen.blit(obj.pic, obj.pic.get_rect(center=(screen_x, screen_y))) 
            if obj.Layer != "WallLayer":         
                Move(obj)
            if obj.Layer != "WallLayer":
                CollisionCheck(obj)

    #______ Adam Ohlsén
    #don't put logic past this point unless you are certain
    DeltaTime = clock.tick(60) / 1000
    DeltaTime = max(0.001, min(0.1, DeltaTime))
    pygame.display.flip()


pygame.display.quit()
pygame.quit()
