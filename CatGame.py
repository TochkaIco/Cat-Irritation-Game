
#imports
import pygame
import math
import numpy as np

import Classes
#map generation import
import MapGenerator

##pygame necessities
#{
#basics --
pygame.init()
display_info = pygame.display.Info()

screen = pygame.display.set_mode((display_info.current_w,display_info.current_h),pygame.RESIZABLE)
#Roman, you can't add RESIZABLE without having the original screen width and height
Size_Difference = screen.get_height() / screen.get_width()
# For some reason a 1920 x 1080 screen will give you 1280, 800. Just remember that
Default_screen = 1280,800

pygame.display.set_caption("Cat-Irritation-Game")
clock = pygame.time.Clock()
DeltaTime = 0.1
debug_draw = True

#bg_loading
screen.fill((0, 0, 0))
font = pygame.font.Font(None, 74)
loading_text = font.render("Loading...", True, (255, 255, 255))
text_rect = loading_text.get_rect(center=(screen.get_width()/2,screen.get_height()/2))
screen.blit(loading_text, text_rect)
pygame.display.flip()

#sprites --
# cm- Roman you will be a placeholder for everything
Roman = pygame.image.load("Images/Roman-Verde.png").convert_alpha()
Roman = pygame.transform.scale_by(Roman,0.3)

CatGirl = pygame.image.load("Images/Catgirl 15x38.png").convert_alpha()
HealthBar = pygame.image.load("Images/Cat_health_bar.png").convert_alpha()
Angy_Slime = pygame.image.load("Images/Angry_Slime.png").convert_alpha()
#}

###LogicAspects
#{
##Global variables
#{
Running = True

Scene = "MainScene"
LoadedScene = False

#Layers__--__
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
        if object2.IsTrigger == False:
            if object2.PicAngle != 0:
                obj.Update_Hitbox()
                object2.Update_Hitbox()
                if obj.Hitbox.centery < object2.Hitbox.centery: YDirection = -1 
                else: YDirection = 1
                if obj.Hitbox.centerx > object2.Hitbox.centerx: XDirection = 1
                else: XDirection = -1
                #Getting the points to compare pos to
                if object2.Points[0][1] > object2.Points[1][1]: TopYPoint, BottomYPoint, LeftXPoint, RightXPoint, ObjPIndex = object2.Points[1][0] = object2.Points[0][1], object2.Points[3][1], object2.Points[2][0], 1
                else: TopYPoint, BottomYPoint, LeftXPoint, RightXPoint, ObjPIndex = object2.Points[1][1], object2.Points[2][1], object2.Points[0][0], object2.Points[3][0], 0     

                #tan v
                RadAngle = math.radians(object2.PicAngle)
                Xadd = object2.width / 2 + (object2.width / 2 * math.tan(RadAngle)) * math.tan(RadAngle/2)
                Yadd = object2.height / 2 + (object2.height / 2 * math.tan(RadAngle)) * math.tan(RadAngle/2)
                print(f"Xadd ={Xadd}")
                Ey_height = (obj.Hitbox.centerx - object2.Hitbox.centerx) * math.tan(RadAngle) * YDirection
                Ex_height = (obj.Hitbox.centery - object2.Hitbox.centery) * math.tan(RadAngle) * -XDirection
                #top
                #Eye of rahh checks if the obj is below or above (might be redundant)
                CollidedOnY = False
                if CheckObbCollisions(obj,object2) == True:
                    if obj.Hitbox.centery < TopYPoint and obj.Points[0][0] < object2.Points[1][0] and obj.Points[1][0] > object2.Points[0][0]:
                        if obj.yvelocity > 0 or (abs(obj.xvelocity) > 0 and obj.yvelocity == 0):
                            obj.Hitbox.bottom = object2.Hitbox.centery + (Yadd + Ey_height + (obj.width / 2 * math.tan(RadAngle))-1) * YDirection
                        CollidedOnY = True
                    #bottom
                    if obj.Hitbox.centery > BottomYPoint and obj.Points[2][0] < object2.Points[3][0] and obj.Points[3][0] > object2.Points[2][0]: 
                        if obj.yvelocity < 0 or (abs(obj.xvelocity) > 0 and obj.yvelocity == 0):
                            obj.Hitbox.top = object2.Hitbox.centery + (Yadd + Ey_height + (obj.width / 2 * math.tan(RadAngle))-1) * YDirection
                        CollidedOnY = True
                    #______________________________________________________________________________
                    #Note to future me: since we know it did or didn't collide on Y axis we can give permission to collide on x axis
                    if obj.Hitbox.centerx < LeftXPoint and CollidedOnY == False and obj.xvelocity >= 0:
                        obj.Hitbox.right = object2.Hitbox.centerx + (Xadd + Ex_height + (obj.height / 2 * math.tan(RadAngle))-1) * XDirection
                    if obj.Hitbox.centerx > RightXPoint and CollidedOnY == False and obj.xvelocity <= 0:
                        obj.Hitbox.left = object2.Hitbox.centerx + (Xadd + Ex_height + (obj.height / 2 * math.tan(RadAngle))-1) * XDirection
            obj.Update_Hitbox()
            object2.Update_Hitbox()

    #Checking X collisions
    if velocity_magnitute > 0:
        normalized_x = (obj.xvelocity / velocity_magnitute) * obj.WalkSpeed
        obj.Hitbox.x += normalized_x * DeltaTime
    #Checks if it's even moving
    if obj.xvelocity != 0:
        for object2 in obj.InteractLayers:
            if obj.IsTrigger == False and object2.IsTrigger == False:
                #Checking if it's a slope
                if object2.PicAngle == 0:
                    if obj.Hitbox.colliderect(object2.Hitbox):
                        if obj.xvelocity > 0:
                            obj.Hitbox.right = object2.Hitbox.left
                        if obj.xvelocity < 0:
                            obj.Hitbox.left = object2.Hitbox.right
                        obj.x = obj.Hitbox.center[0]

    #-
    #Checking Y collisions
    if velocity_magnitute > 0:  
        normalized_y = (obj.yvelocity / velocity_magnitute) * obj.WalkSpeed
        obj.Hitbox.centery += normalized_y * DeltaTime

    if obj.yvelocity != 0:
        for object2 in obj.InteractLayers:
            if obj.IsTrigger == False and object2.IsTrigger == False:
                if object2.PicAngle == 0:
                    if obj.Hitbox.colliderect(object2.Hitbox):
                        if obj.yvelocity > 0:
                            obj.Hitbox.bottom = object2.Hitbox.top
                        if obj.yvelocity < 0:
                            obj.Hitbox.top = object2.Hitbox.bottom
                        obj.y = obj.Hitbox.center[1]

                #_______________________________________________________________________________
def Rotate(obj):
    obj.pic = pygame.transform.rotate(obj.OriginPic, -obj.PicAngle)

#Managing camera to hold the player always in the middle
def UpdateCamera(target, camera_smoothness=0.1):
    global CameraX, CameraY

    target_x = target.Hitbox.x - screen.get_width()/2
    target_y = target.Hitbox.y - screen.get_height()/2

    CameraX += (target_x - CameraX) * camera_smoothness
    CameraY += (target_y - CameraY) * camera_smoothness

#Classes



#}

#Generating BG
IslandBackground = MapGenerator.Generate_Island_BG()
#Somehow scaling by 2 messes up the Island? Wtf? Im not going to bother..
IslandBackground = pygame.transform.scale_by(IslandBackground,1)

#Misc
DefaultPlayer = Classes.Player(SpawnPoint[0],SpawnPoint[1],0,CatGirl)
tempthing = 1024
TestWall = Classes.Wall(SpawnPoint[0], SpawnPoint[1]-300, 20,Roman)
TestSlime = Classes.Slime(SpawnPoint[0] - 300, SpawnPoint[1] - 200,0,Angy_Slime)

while Running == True:
    tempthing -= 1
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
        
        DefaultPlayer.Control_Player(PyEvents)
        UpdateCamera(DefaultPlayer, camera_smoothness=0.15)
        screen.blit(IslandBackground, (-CameraX, -CameraY))

        for obj in Classes.Default_Objects:
            Rotate(obj)
            if obj.Layer != "WallLayer":
                obj.Update_Obj_specific()
            
            screen_x = obj.Hitbox.centerx - CameraX
            screen_y = obj.Hitbox.centery - CameraY
            #No mess anymore
            Proportion_To_Scale_By = screen.get_width()  * Size_Difference / (Default_screen[1])

            

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
                pygame.draw.rect(screen, (0, 0, 255), adjusted_hitbox)
                pygame.draw.circle(screen, (255, 0, 0), (screen_x, screen_y), 2)
                if obj.PicAngle != 0:
                    pygame.draw.circle(screen, (255,0,0), (obj.Top_left_point[0] - CameraX, obj.Top_left_point[1] - CameraY),2)
                    pygame.draw.circle(screen, (255,0,0), (obj.Top_right_point[0] - CameraX, obj.Top_right_point[1] - CameraY),2)
                    pygame.draw.circle(screen, (255,0,0), (obj.Bottom_left_point[0] - CameraX, obj.Bottom_left_point[1] - CameraY),2)
                    pygame.draw.circle(screen, (255,0,0), (obj.Bottom_right_point[0] - CameraX, obj.Bottom_right_point[1] - CameraY),2)
                if CheckObbCollisions(DefaultPlayer,TestWall) == True:
                    pygame.draw.circle(screen, (255, 0, 0), (screen_x, screen_y), 10)

        #The player healthbar, maybeeee i should've made a ui class but it's like 24:00
        print (f"Screen = {screen.get_width(), screen.get_height()} OriginalScreen = {Default_screen} Scale Proportion = {Proportion_To_Scale_By} Size Diff = {Size_Difference}")

        #Wait wtf? why is that genuinely just not working?
        screen.blit(HealthBar, (20,20))
        print(f"Healthbar: ", HealthBar.get_width(), HealthBar.get_height())
            
            
    #______ Adam Ohlsén
    #don't put logic past this point unless you are certain
    DeltaTime = clock.tick(60) / 1000
    DeltaTime = max(0.001, min(0.1, DeltaTime))
    #Meow is back
    #print("meow")
    pygame.display.flip()


pygame.display.quit()
pygame.quit()
