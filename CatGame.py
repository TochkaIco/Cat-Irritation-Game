
#imports
import pygame
import math
import numpy as np
import CatGame_BasicLogics as Log
import logging
logger = logging.getLogger(__name__)

import Classes
from AssetManager import AssetManager
from UI import UIManager

#Hey, Sasha, Maxi, Roman or Indy. Why tf is the terminal telling me no module found? Literally
# there is a module though. Im leaving this text in the background, hope one of you notices
# map generation import
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

logging.basicConfig(filename='runner.log', level=logging.INFO)
logger.info('Pygame init')
pygame.display.set_caption("Cat-Irritation-Game")
clock = pygame.time.Clock()
DeltaTime = 0.1
debug_draw = True

logger.info(f"Detected screen size: {screen.get_width()}, {screen.get_height()}")

#bg_loading
screen.fill((0, 0, 0))
font = pygame.font.Font(None, 74)
debug_font = pygame.font.Font(None, 36)
loading_text = font.render("Loading...", True, (255, 255, 255))
text_rect = loading_text.get_rect(center=(screen.get_width()/2,screen.get_height()/2))
screen.blit(loading_text, text_rect)
pygame.display.flip()

#sprites --
# cm- Roman you will be a placeholder for everything
Roman = AssetManager.get_image("Images/Roman-Verde.png")
Roman = pygame.transform.scale_by(Roman,0.3)

CatGirl = AssetManager.get_image("Images/Catgirl 15x38.png")
# UI images are now handled by UIManager
Angy_Slime = AssetManager.get_image("Images/Angry_Slime.png")
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
    logger.info(debug_iterations)
    print (debug_iterations)
    return None,None

def Rotate(obj):
    obj.pic = pygame.transform.rotate(obj.OriginPic, -obj.angle)

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
DefaultPlayer = None
TestWall = None

def Reset_Game():
    global DefaultPlayer, TestWall, Scene, LoadedScene
    Classes.Clear_All_Objects()
    
    # Redraw loading screen during reset
    screen.fill((0, 0, 0))
    screen.blit(loading_text, text_rect)
    pygame.display.flip()

    DefaultPlayer = Classes.Player(SpawnPoint[0], SpawnPoint[1], 0, CatGirl)
    TestWall = Classes.Wall(SpawnPoint[0], SpawnPoint[1]-300, 20, Roman)

    # Spawn a variety of enemies across the island
    enemy_positions = MapGenerator.Get_Island_Land_Points(IslandBackground, 30)
    for i, pos in enumerate(enemy_positions):
        # Avoid spawning enemies right on top of the player
        dist_to_player = math.sqrt((pos[0] - SpawnPoint[0])**2 + (pos[1] - SpawnPoint[1])**2)
        if dist_to_player < 500:
            continue
            
        if i % 10 == 0:
            Classes.GiantSlime(pos[0], pos[1], 0, Angy_Slime)
        elif i % 3 == 0:
            Classes.MiniSlime(pos[0], pos[1], 0, Angy_Slime)
        else:
            Classes.Slime(pos[0], pos[1], 0, Angy_Slime)
    
    Scene = "MainScene"
    LoadedScene = False
    logger.info("Game reset successfully")

#Initial spawn
Reset_Game()

ui_manager = UIManager()
tempthing = 1024

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
            
    # Check for restart command
    if Scene == "DeathScene":
        for event in PyEvents:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    Reset_Game()

    #______ Adam Ohlsén
    #don't put logic inside of running before this point unless you are certain
    #Scenes
    if Scene == "MainScene":
        if LoadedScene == False:
            logger.info('Loading scene')
            print ("loading scene")
            LoadedScene = True
        #-
        #Debug Collision Draw Toggle
        for event in PyEvents:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    debug_draw = not debug_draw
                    logger.info('Debug draw', debug_draw)
                    print("Debug Draw", debug_draw)
        
        DefaultPlayer.Control_Player(PyEvents)
        UpdateCamera(DefaultPlayer, camera_smoothness=0.15)
        screen.blit(IslandBackground, (-CameraX, -CameraY))
        Log.Obj_Logic_Handler.Knockback()

        # Check for player death
        if DefaultPlayer.Health <= 0:
            Scene = "DeathScene"
            logger.info("Player died, switching to DeathScene")

        for obj in Classes.Default_Objects:
            obj.Update_class()
            Rotate(obj)
            obj.Update_Obj_specific()
            
            screen_x = obj.Hitbox.centerx - CameraX
            screen_y = obj.Hitbox.centery - CameraY
            #No mess anymore
            Proportion_To_Scale_By = screen.get_width()  * Size_Difference / (Default_screen[1])

            

            screen.blit(obj.pic, obj.pic.get_rect(center=(screen_x,screen_y)))
            obj.Update_Hitbox()

            # The player healthbar
           

            #Debug Draw Hitboxes
            if debug_draw:
                adjusted_hitbox = obj.Hitbox.copy()
                adjusted_hitbox.x -= CameraX
                adjusted_hitbox.y -= CameraY
                #if trigger - make it red else blue, to see where the player can interact with stuff
                if obj.IsTrigger:
                    pygame.draw.rect(screen, (255, 0, 0), adjusted_hitbox)
                    pygame.draw.circle(screen, (0, 0, 255), (screen_x, screen_y), 2)
                else:
                    pygame.draw.rect(screen, (0, 0, 255), adjusted_hitbox)
                    pygame.draw.circle(screen, (255, 0, 0), (screen_x, screen_y), 2)
                if obj.angle != 0:
                    pygame.draw.circle(screen, (255,0,0), (obj.Top_left_point[0] - CameraX, obj.Top_left_point[1] - CameraY),2)
                    pygame.draw.circle(screen, (255,0,0), (obj.Top_right_point[0] - CameraX, obj.Top_right_point[1] - CameraY),2)
                    pygame.draw.circle(screen, (255,0,0), (obj.Bottom_left_point[0] - CameraX, obj.Bottom_left_point[1] - CameraY),2)
                    pygame.draw.circle(screen, (255,0,0), (obj.Bottom_right_point[0] - CameraX, obj.Bottom_right_point[1] - CameraY),2)

        # The player healthbar
        ui_manager.draw_player_ui(screen, DefaultPlayer)

    elif Scene == "DeathScene":
        # Draw the last frame of the game in the background
        screen.blit(IslandBackground, (-CameraX, -CameraY))
        for obj in Classes.Default_Objects:
            screen_x = obj.Hitbox.centerx - CameraX
            screen_y = obj.Hitbox.centery - CameraY
            screen.blit(obj.pic, obj.pic.get_rect(center=(screen_x,screen_y)))
        
        ui_manager.draw_death_screen(screen)
            
    #FPS count. Why? Idfk, i want
    #Dont's show on the menu
    if debug_draw and LoadedScene:
        current_fps = int(Log.clock.get_fps())
        #Yellow only cause we never used it
        fps_surface = debug_font.render(f"FPS: {current_fps}", True, (255, 255, 0))
        screen.blit(fps_surface, (screen.get_width() - 120, 20))
            
    #______ Adam Ohlsén
    #don't put logic past this point unless you are certain
    DeltaTime = Log.Set_DeltaTime()
    #Meow is back
    #Meow is not back
    #print("meow")
    pygame.display.flip()


pygame.display.quit()
pygame.quit()
