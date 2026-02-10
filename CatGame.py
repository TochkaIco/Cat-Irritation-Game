
#imports
import pygame
import math
import numpy as np
import CatGame_BasicLogics as Log

import Classes
#Hey, sasha, Maxi, Roman or Indy. Why tf is the terminal telling me no module found? Literally
# there is a module though. Im leaving this text in the background, hope one of you notices
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

def Rotate(obj):
    obj.pic = pygame.transform.rotate(obj.OriginPic, -obj.PicAngle)

#Managing camera to hold the player always in the middle
def UpdateCamera(target, camera_smoothness=0.1):
    global CameraX, CameraY

    target_x = target.Hitbox.x - screen.get_width()/2
    target_y = target.Hitbox.y - screen.get_height()/2

    CameraX += (target_x - CameraX) * camera_smoothness
    CameraY += (target_y - CameraY) * camera_smoothness

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
        Log.Obj_Logic_Handler.Knockback()

        for obj in Classes.Default_Objects:
            Rotate(obj)
            obj.Update_Obj_specific()
            
            screen_x = obj.Hitbox.centerx - CameraX
            screen_y = obj.Hitbox.centery - CameraY
            #No mess anymore
            Proportion_To_Scale_By = screen.get_width()  * Size_Difference / (Default_screen[1])

            

            screen.blit(obj.pic, obj.pic.get_rect(center=(screen_x,screen_y)))
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

        #The player healthbar, maybeeee i should've made a ui class but it's like 24:00
        print (f"Screen = {screen.get_width(), screen.get_height()} OriginalScreen = {Default_screen} Scale Proportion = {Proportion_To_Scale_By} Size Diff = {Size_Difference}")

        #Wait wtf? why is that genuinely just not working?
        screen.blit(HealthBar, (20,20))
        print(f"Healthbar: ", HealthBar.get_width(), HealthBar.get_height())
            
            
    #______ Adam Ohlsén
    #don't put logic past this point unless you are certain
    DeltaTime = Log.Get_DeltaTime()
    #Meow is back
    #print("meow")
    pygame.display.flip()


pygame.display.quit()
pygame.quit()
