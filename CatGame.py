
#imports
import pygame
import math
import numpy as np
from shapely import Point
from shapely import LineString
#map generation import
import MapGenerator

##pygame necessities
#{
#basics --
pygame.init()
screen = pygame.display.set_mode((1920,1080),pygame.RESIZABLE)
pygame.display.set_caption("Cat-Irritation-Game")
clock = pygame.time.Clock()
DeltaTime = 0.1
debug_draw = True

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

CatGirl = pygame.image.load("Images/Catgirl 15x38.png").convert_alpha()
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
SpawnPoint = (MapGenerator.IslandSize/2,MapGenerator.IslandSize/2)

#Camera
CameraX = 0
CameraY = 0

#}
#Global Functions
def RayCast(OriginX,OriginY,TargetX,TargetY,CollisionLayers):
    direction = math.atan2(TargetY - OriginY, TargetX - OriginX)
    x = OriginX
    y = OriginY
    Length = math.sqrt(pow(OriginX - TargetX,2) + pow(OriginY - TargetY,2))
    ray_length = 0
    debug_iterations = 0
    xrate = -math.cos(math.radians(direction - 90))
    yrate = math.sin(math.radians(direction - 90))
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
def CheckObbCollisions(obj1,obj2):
    Collided = False
    Dist = 50 #put it at anything positive
    pointslist = obj1.Points + obj2.Points
    CurrentIterration = 0
    for axis in range(6):
        if CurrentIterration == 3:
            CurrentIterration = 4
        point1 = (pointslist[CurrentIterration])
        
        point2 = (pointslist[CurrentIterration + 1])
        # Do point[0] to access the x and point[1] to acces y

        ax = point1[0]-point2[0]
        ay = point1[1]-point2[1]
        length = math.sqrt(ax**2+ay**2)
        ux, uy = ax / length, ay / length
        #max points

        obj1_min_x = obj2_min_x = math.inf
        obj1_min_point = obj1_max_point = obj2_min_point = obj2_max_point = (0,0)
        obj1_max_x = obj2_max_x = -math.inf

        for points in obj1.Points:
            if ax != 0:
                dist = (points[0]) * ux + (points[1] * uy)
                targetx = dist * ux
                targety = dist * uy
            else:
                targetx = points[0]
                targety = points[1]
            if targetx < obj1_min_x:
                obj1_min_x = targetx
                obj1_min_y = targety
            if targetx > obj1_max_x:
                obj1_max_x = targetx
                obj1_max_y = targety
        if debug_draw:
            pygame.draw.circle(screen,(255,0,0),(obj1_min_x - CameraX, obj1_min_y - CameraY) ,2)
            pygame.draw.circle(screen,(255,0,0),(obj1_max_x - CameraX, obj1_max_y - CameraY),2)

        for points in obj2.Points:
            if ax != 0:
                dist = (points[0]) * ux + (points[1] * uy)
                targetx = dist * ux
                targety = dist * uy
            else:
                targetx = points[0]
                targety = points[1]
            if targetx < obj2_min_x:
                obj2_min_x = targetx
                obj2_min_y = targety
            if targetx > obj2_max_x:
                obj2_max_x = targetx 
                obj2_max_y = targety      
        if debug_draw:
            pygame.draw.circle(screen,(255,255,0),(obj2_min_x - CameraX, obj2_min_y - CameraY) ,2)
            pygame.draw.circle(screen,(255,255,0),(obj2_max_x - CameraX, obj2_max_y - CameraY),2)
        
        if ax != 0:
            if obj2_min_x < obj1_min_x < obj2_max_x or obj2_min_x < obj1_max_x < obj2_max_x:
                Collided = True
            else:
                Collided = False
                break
        else:
            if obj2_min_y < obj1_min_y < obj2_max_y or obj2_min_y < obj1_max_y < obj2_max_y:
                Collided = True
            else:
                Collided = False
                break
        CurrentIterration += 1

    return Collided


def MoveAndHandleCollisionCheck(obj):
    velocity_magnitute = math.sqrt(obj.xvelocity**2 + obj.yvelocity**2)
    for object2 in obj.InteractLayers:
        if obj.Hitbox.centery < object2.Hitbox.centery:
            YDirection = -1
        else:
            YDirection = 1
        if obj.Hitbox.centerx > object2.Hitbox.centerx:
            XDirection = -1
        else:
            XDirection = 1
        #Remember the y axis is inverted in pygame
        if object2.Points[0][1] > object2.Points[1][1]:
            TopYPoint = object2.Points[0][1]
        else:
            TopYPoint = object2.Points[1][1]
        if object2.Points[2][1] < object2.Points[3][1]:
            BottomYPoint = object2.Points[2][1]
        else:
            BottomYPoint = object2.Points[3][1]

        #top
        #Ok, i will first if it's below or above, then if it's actually within points
        if obj.Hitbox.centery < TopYPoint and obj.Points[0][0] < object2.Points[1][0] and obj.Points[1][0] > object2.Points[0][0] and obj.yvelocity >= 0:
            if CheckObbCollisions(obj,object2) == True:
                O_height = object2.height / 2
                dist = obj.Hitbox.centerx - object2.Hitbox.centerx
                #tan v
                Ex_height = dist * math.radians(-object2.PicAngle) * -YDirection
                obj.Hitbox.centery = object2.Hitbox.centery + (O_height + Ex_height + obj.height / 2) * YDirection
                obj.y = obj.Hitbox.center[1]
        #bottom
        if obj.Hitbox.centery > BottomYPoint and obj.Points[2][0] < object2.Points[3][0] and obj.Points[3][0] > object2.Points[2][0] and obj.yvelocity <= 0:
            if CheckObbCollisions(obj,object2) == True:
                O_height = object2.height / 2
                dist = obj.Hitbox.centerx - object2.Hitbox.centerx
                #tan v
                Ex_height = dist * math.radians(-object2.PicAngle) * -YDirection
                obj.Hitbox.centery = object2.Hitbox.centery + O_height + Ex_height + obj.height / 2
                obj.y = obj.Hitbox.center[1]
        #______________________________________________________________________________


    #Checking X collisions
    if velocity_magnitute > 0:
        normalized_x = (obj.xvelocity / velocity_magnitute) * obj.WalkSpeed
        obj.Hitbox.x += normalized_x * DeltaTime
    #Checks if it's even moving
    if obj.xvelocity != 0:
        for object2 in obj.InteractLayers:
            #Checking if it's a slope
            if object2.PicAngle == 0:
                if CheckObbCollisions(obj,object2) == True:
                    if obj.xvelocity > 0:
                        obj.Hitbox.right = object2.Hitbox.left
                    if obj.xvelocity < 0:
                        obj.Hitbox.left = object2.Hitbox.right
                    obj.x = obj.Hitbox.center[0]
            else:
                #Slopped objects x collision logic
                #______________________________________________________________________________
                pass

    #-
    #Checking Y collisions
    if velocity_magnitute > 0:  
        normalized_y = (obj.yvelocity / velocity_magnitute) * obj.WalkSpeed
        obj.Hitbox.centery += normalized_y * DeltaTime
    if obj.yvelocity != 0:
        for object2 in obj.InteractLayers:
            if object2.PicAngle == 0:
                if obj.Hitbox.colliderect(object2.Hitbox):
                    if obj.yvelocity > 0:
                        obj.Hitbox.bottom = object2.Hitbox.top
                    if obj.yvelocity < 0:
                        obj.Hitbox.top = object2.Hitbox.bottom
                    obj.y = obj.Hitbox.center[1]
            else:
                #slopped objects, y collision logic
                #______________________________________________________________________________
                pass

                #_______________________________________________________________________________
def Rotate(obj):
    obj.pic = pygame.transform.rotate(obj.OriginPic, -obj.PicAngle)

#Managing camera to hold the player always in the middle
def UpdateCamera(target, camera_smoothness=0.1):
    global CameraX, CameraY

    target_x = target.Hitbox.x - 1920/2
    target_y = target.Hitbox.y - 1080/2

    CameraX += (target_x - CameraX) * camera_smoothness
    CameraY += (target_y - CameraY) * camera_smoothness

#Classes
class Player:
    Player_Class_Picture = CatGirl
    def __init__(self,x,y):
        #______ Adam Ohlsén
        self.WalkSpeed = 200
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
        self.Points = (self.Hitbox.topleft, self.Hitbox.topright,self.Hitbox.bottomleft, self.Hitbox.bottomright)
        self.height = self.OriginPic.get_height()
        self.width = self.OriginPic.get_width()
        self.PicAngle = 0
        self.Layer = "PlayerLayer"
        self.InteractLayers = WallLayer
        
        #Put all __init__ logic before the append
        Default_Objects.append(self)
        PlayerLayer.append(self)
    def Update_Hitbox(self):
        self.Points = (self.Hitbox.topleft, self.Hitbox.topright,self.Hitbox.bottomleft, self.Hitbox.bottomright)


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
    def __init__(self,x,y,angle):
        #X and Y
        self.x = x
        self.y = y

        #Misc
        self.OriginPic = Wall.Wall_Class_Picture
        self.pic = self.OriginPic
        self.PicAngle = angle
        self.Layer = "WallLayer"
        self.height = self.OriginPic.get_height()
        self.height = self.height
        print (f"height: {self.height}")
        self.width = self.OriginPic.get_width()
        self.width = self.width
        print (f"width: {self.width}")
        if self.PicAngle != 0:
            self.Hitbox = self.OriginPic.get_rect(center= (self.x,self.y))
            #New Hitbox
            #Points
            Rotate_Point = self.Hitbox.center
            Original_Top_left = (self.Hitbox.topleft)
            Original_Top_right = (self.Hitbox.topright)
            Original_Bottom_left = (self.Hitbox.bottomleft)
            Original_Bottom_right = (self.Hitbox.bottomright)
            #Maths
            Radians_angle = math.radians(self.PicAngle)
            cos_rad = math.cos(Radians_angle)
            sin_rad = math.sin(Radians_angle)
            #Top
            Top_Left_Offset_X = (Original_Top_left[0] - Rotate_Point[0])
            Top_Left_Offset_Y = (Original_Top_left[1] - Rotate_Point[1])
            Top_Right_Offset_X = (Original_Top_right[0] - Rotate_Point[0])
            Top_Right_Offset_Y = (Original_Top_right[1] - Rotate_Point[1])
            #Bottom
            Bottom_Left_Offset_X = (Original_Bottom_left[0] - Rotate_Point[0])
            Bottom_Left_Offset_Y = (Original_Bottom_left[1] - Rotate_Point[1])
            Bottom_Right_Offset_X = (Original_Bottom_right[0] - Rotate_Point[0])
            Bottom_Right_Offset_Y = (Original_Bottom_right[1] - Rotate_Point[1])

            #Calculating points
            self.Top_left_point = ((Rotate_Point[0] + cos_rad * Top_Left_Offset_X) - sin_rad * Top_Left_Offset_Y, 
                                   (Rotate_Point[1] + sin_rad * Top_Left_Offset_X) + cos_rad * Top_Left_Offset_Y)
            self.Top_right_point = ((Rotate_Point[0] + cos_rad * Top_Right_Offset_X) - sin_rad * Top_Right_Offset_Y, 
                                   (Rotate_Point[1] + sin_rad * Top_Right_Offset_X) + cos_rad * Top_Right_Offset_Y)
            self.Bottom_left_point = ((Rotate_Point[0] + cos_rad * Bottom_Left_Offset_X) - sin_rad * Bottom_Left_Offset_Y, 
                                   (Rotate_Point[1] + sin_rad * Bottom_Left_Offset_X) + cos_rad * Bottom_Left_Offset_Y)
            self.Bottom_right_point = ((Rotate_Point[0] + cos_rad * Bottom_Right_Offset_X) - sin_rad * Bottom_Right_Offset_Y, 
                                   (Rotate_Point[1] + sin_rad * Bottom_Right_Offset_X) + cos_rad * Bottom_Right_Offset_Y)
            
            self.Points = (self.Top_left_point,self.Top_right_point, self.Bottom_left_point,self.Bottom_right_point)
                        
        else:
            self.Hitbox = self.OriginPic.get_rect(center= (self.x,self.y))
            self.Points = (self.Hitbox.topleft, self.Hitbox.topright,self.Hitbox.bottomleft, self.Hitbox.bottomright)

        Default_Objects.append(self)
        WallLayer.append(self)  
    def Update_Hitbox(self):
        if self.PicAngle != 0:
            self.Hitbox = self.OriginPic.get_rect(center= (self.x,self.y))
            #New Hitbox
            #Points
            Rotate_Point = self.Hitbox.center
            Original_Top_left = (self.Hitbox.topleft)
            Original_Top_right = (self.Hitbox.topright)
            Original_Bottom_left = (self.Hitbox.bottomleft)
            Original_Bottom_right = (self.Hitbox.bottomright)
            #Maths
            Radians_angle = math.radians(self.PicAngle)
            cos_rad = math.cos(Radians_angle)
            sin_rad = math.sin(Radians_angle)
            #Top
            Top_Left_Offset_X = (Original_Top_left[0] - Rotate_Point[0])
            Top_Left_Offset_Y = (Original_Top_left[1] - Rotate_Point[1])
            Top_Right_Offset_X = (Original_Top_right[0] - Rotate_Point[0])
            Top_Right_Offset_Y = (Original_Top_right[1] - Rotate_Point[1])
            #Bottom
            Bottom_Left_Offset_X = (Original_Bottom_left[0] - Rotate_Point[0])
            Bottom_Left_Offset_Y = (Original_Bottom_left[1] - Rotate_Point[1])
            Bottom_Right_Offset_X = (Original_Bottom_right[0] - Rotate_Point[0])
            Bottom_Right_Offset_Y = (Original_Bottom_right[1] - Rotate_Point[1])

            #Calculating points
            self.Top_left_point = ((Rotate_Point[0] + cos_rad * Top_Left_Offset_X) - sin_rad * Top_Left_Offset_Y, 
                                (Rotate_Point[1] + sin_rad * Top_Left_Offset_X) + cos_rad * Top_Left_Offset_Y)
            self.Top_right_point = ((Rotate_Point[0] + cos_rad * Top_Right_Offset_X) - sin_rad * Top_Right_Offset_Y, 
                                (Rotate_Point[1] + sin_rad * Top_Right_Offset_X) + cos_rad * Top_Right_Offset_Y)
            self.Bottom_left_point = ((Rotate_Point[0] + cos_rad * Bottom_Left_Offset_X) - sin_rad * Bottom_Left_Offset_Y, 
                                (Rotate_Point[1] + sin_rad * Bottom_Left_Offset_X) + cos_rad * Bottom_Left_Offset_Y)
            self.Bottom_right_point = ((Rotate_Point[0] + cos_rad * Bottom_Right_Offset_X) - sin_rad * Bottom_Right_Offset_Y, 
                                (Rotate_Point[1] + sin_rad * Bottom_Right_Offset_X) + cos_rad * Bottom_Right_Offset_Y)
            
            self.Points = (self.Top_left_point,self.Top_right_point, self.Bottom_left_point,self.Bottom_right_point)
                        
        else:
            self.Hitbox = self.OriginPic.get_rect(center= (self.x,self.y))
            self.Points = (self.Hitbox.topleft, self.Hitbox.topright,self.Hitbox.bottomleft, self.Hitbox.bottomright)  
#}

#Generating BG
IslandBackground = MapGenerator.Generate_Island_BG()

#Misc
DefaultPlayer = Player(SpawnPoint[0],SpawnPoint[1])
tempthing = 1024
TestWall = Wall(SpawnPoint[0], SpawnPoint[1]-300, 20)

while Running == True:
    tempthing -= 1
    #Glitch fix
    screen.fill((25, 76, 204))

    ##! DELETE AFTER! In a minute there will be 3600 walls!
    #Wall(tempthing, 100,20)
    
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
        #Debug Collision Draw Toggle
        for event in PyEvents:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    debug_draw = not debug_draw
                    print("Debug Draw", debug_draw)
        
        DefaultPlayer.Control_Player()
        UpdateCamera(DefaultPlayer, camera_smoothness=0.15)
        screen.blit(IslandBackground, (-CameraX, -CameraY))
        for obj in Default_Objects:
            Rotate(obj)
            
            screen_x = obj.Hitbox.centerx - CameraX
            screen_y = obj.Hitbox.centery - CameraY
            #No mess anymore
            screen.blit(obj.pic, obj.pic.get_rect(center=(screen_x,screen_y))) 
            if obj.Layer != "WallLayer":         
                MoveAndHandleCollisionCheck(obj)

            DefaultPlayer.Update_Hitbox()
            TestWall.Update_Hitbox()
            
            
            #Debugging my hitboxes
           

            #Debug Draw Hitboxes
            if debug_draw:
                adjusted_hitbox = obj.Hitbox.copy()
                adjusted_hitbox.x -= CameraX
                adjusted_hitbox.y -= CameraY
                #pygame.draw.rect(screen, (0, 0, 255), adjusted_hitbox)
                pygame.draw.circle(screen, (255, 0, 0), (screen_x, screen_y), 2)
                if obj.PicAngle != 0:
                    pygame.draw.circle(screen, (255,0,0), (obj.Top_left_point[0] - CameraX, obj.Top_left_point[1] - CameraY),2)
                    pygame.draw.circle(screen, (255,0,0), (obj.Top_right_point[0] - CameraX, obj.Top_right_point[1] - CameraY),2)
                    pygame.draw.circle(screen, (255,0,0), (obj.Bottom_left_point[0] - CameraX, obj.Bottom_left_point[1] - CameraY),2)
                    pygame.draw.circle(screen, (255,0,0), (obj.Bottom_right_point[0] - CameraX, obj.Bottom_right_point[1] - CameraY),2)
                if CheckObbCollisions(DefaultPlayer,TestWall) == True:
                    pygame.draw.circle(screen, (255, 0, 0), (screen_x, screen_y), 10)
            

    #______ Adam Ohlsén
    #don't put logic past this point unless you are certain
    DeltaTime = clock.tick(60) / 1000
    DeltaTime = max(0.001, min(0.1, DeltaTime))
    #Meow is back
    #print("meow")
    pygame.display.flip()


pygame.display.quit()
pygame.quit()
