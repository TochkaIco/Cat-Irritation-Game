import pygame
import math
import CatGame_BasicLogics as Log
import logging
logger = logging.getLogger(__name__)
pygame.init()


Default_Objects = []
PlayerLayer = []
EnemyLayer = []
WallLayer = []
WeaponLayer = []

class Empty_Hitboxes:
    def __init__(self,x,y,angle,width,height,LifeTime,Layer):
        self.x = x
        self.y = y
        self.IsTrigger = True
        self.Layer = Layer
        #Put parent to none if it's a standalone hitbox
        self.IsActive = True
        
        #Set lifetime to 0 to have endless, or don't call the update function
        self.CurrentTime = 0
        self.LifeTime = LifeTime
        #Can one of you change every PicAngle to angle instead? It was a mistake
        # naming it Picangle but now all of them are that way. The sooner the 
        # less work
        self.PicAngle = angle

        if self.PicAngle == 0:
            self.Hitbox = pygame.Rect(center=(x,y),width=width,height=height)
            self.Points = (self.Hitbox.topleft, self.Hitbox.topright,self.Hitbox.bottomleft, self.Hitbox.bottomright)
        else:
            self.Hitbox = pygame.Rect(center=(x,y),width=width,height=height)
            Rotate_Point = self.Hitbox.center
            Radians_angle = math.radians(self.PicAngle)
            cos_rad = math.cos(Radians_angle)
            sin_rad = math.sin(Radians_angle)
            #Top
            Top_Left_Offset_X,Top_Left_Offset_Y = (self.Hitbox.topleft[0] - Rotate_Point[0]),(self.Hitbox.topleft[1] - Rotate_Point[1])
            Top_Right_Offset_X,Top_Right_Offset_Y = (self.Hitbox.topright[0] - Rotate_Point[0]),(self.Hitbox.topright[1] - Rotate_Point[1])
            #Bottom
            Bottom_Left_Offset_X,Bottom_Left_Offset_Y = (self.Hitbox.bottomleft[0] - Rotate_Point[0]), (self.Hitbox.bottomleft[1] - Rotate_Point[1])
            Bottom_Right_Offset_X,Bottom_Right_Offset_Y = (self.Hitbox.bottomright[0] - Rotate_Point[0]),(self.Hitbox.bottomright[1] - Rotate_Point[1])
            #Points
            self.Top_left_point = ((Rotate_Point[0] + cos_rad * Top_Left_Offset_X) - sin_rad * Top_Left_Offset_Y, 
                                   (Rotate_Point[1] + sin_rad * Top_Left_Offset_X) + cos_rad * Top_Left_Offset_Y)
            self.Top_right_point = ((Rotate_Point[0] + cos_rad * Top_Right_Offset_X) - sin_rad * Top_Right_Offset_Y, 
                                   (Rotate_Point[1] + sin_rad * Top_Right_Offset_X) + cos_rad * Top_Right_Offset_Y)
            self.Bottom_left_point = ((Rotate_Point[0] + cos_rad * Bottom_Left_Offset_X) - sin_rad * Bottom_Left_Offset_Y, 
                                   (Rotate_Point[1] + sin_rad * Bottom_Left_Offset_X) + cos_rad * Bottom_Left_Offset_Y)
            self.Bottom_right_point = ((Rotate_Point[0] + cos_rad * Bottom_Right_Offset_X) - sin_rad * Bottom_Right_Offset_Y, 
                                   (Rotate_Point[1] + sin_rad * Bottom_Right_Offset_X) + cos_rad * Bottom_Right_Offset_Y)
            self.Points = (self.Top_left_point,self.Top_right_point, self.Bottom_left_point,self.Bottom_right_point)
            logger.info(f"Empty hitboxes initialized")
    def Update_Hitbox(self):
        Log.Update_hitbox_dimension_based(self)
        Times_up = Log.Timer(self,self.LifeTime,self.CurrentTime)
        if Times_up == True:
            self.IsActive = False




class Default_Object:
    def __init__(self,x,y,angle,RootPic,MaxHealth,WalkSpeed,Damage,KnockBack,KnockBackTime):
        self.MaxHealth = MaxHealth
        self.Health = self.MaxHealth
        self.Damage = Damage
        self.KnockBack = KnockBack
        self.KnockBackTime = KnockBackTime
        self.IsCluster = False
        #Don't change, ask me first what it does
        self.IsActive = True
        #X
        self.AbleToMove = True
        self.WalkSpeed = WalkSpeed
        self.x = x
        self.xvelocity = 0
        #Y
        self.y = y
        self.yvelocity = 0
        #Misc
        self.RootPic = RootPic
        self.RootPic = pygame.transform.scale_by(self.RootPic,2)
        self.OriginPic = self.RootPic
        self.pic = self.OriginPic

        self.I_frames = 0.7 #(Measured in seconds)
        self.Sex_offenders_list = []

        # (list of miscellaneous functions to start every frame)
        self.StartFunctions = []
        #Hitbox
        self.Hitbox = self.OriginPic.get_rect(center= (self.x,self.y))
        self.Points = (self.Hitbox.topleft, self.Hitbox.topright,self.Hitbox.bottomleft, self.Hitbox.bottomright)
        self.height = self.OriginPic.get_height()
        self.width = self.OriginPic.get_width()

        self.PicAngle = angle
        
        #Put all __init__ logic before the append
        Default_Objects.append(self)
        logger.info("Default object initialized")
    def Update_class(self):
        self.Update_i_frame()

    #idk what i was doing here, i guess it looks better
    def Update_i_frame(self):
        for Counter in self.Sex_offenders_list:
            Counter.Update_time()
    
    def Update_Hitbox(self):
        #This may seem stupid and redundant but we need it, just trust me
        Log.Update_hitbox_image_based(self)
    




        

#---__---
class Player(Default_Object):
    def __init__(self,x,y,angle,RootPic):
        #Btw in this case damage would be if you give the player minecraft thorns enchantment
        super().__init__(x,y,angle,RootPic,MaxHealth=100,WalkSpeed=300,Damage=0,KnockBack=0,KnockBackTime=0)
        #______ Adam Ohlsén
        self.Damage_multi = 1


        self.Layer = "PlayerLayer"
        self.InteractLayers = WallLayer + EnemyLayer
        self.ApplySpeed = False
        self.temp_xvel = 0
        self.temp_yvel = 0 
        
        #Put all __init__ logic before the append
        self.IsTrigger = True
        PlayerLayer.append(self)
        logger.info(f"Player initialized")
    def Update_Obj_specific(self):
        self.InteractLayers = WallLayer + EnemyLayer
        print(self.InteractLayers)
        
        def On_collision(obj,object2):
            if object2.IsTrigger:
                Log.Damage(obj,object2)

        Log.Move_and_Collide_preset(self,On_collision)


    def Control_Player(self,PyEvents):
        for event in PyEvents:
            #-                                   -#
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.temp_yvel += -self.WalkSpeed
                if event.key == pygame.K_s:
                    self.temp_yvel += self.WalkSpeed
                if event.key == pygame.K_a:
                    self.temp_xvel += -self.WalkSpeed
                if event.key == pygame.K_d:
                    self.temp_xvel += self.WalkSpeed
            #-                                      -#
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.temp_yvel -= -self.WalkSpeed
                if event.key == pygame.K_s:
                    self.temp_yvel -= self.WalkSpeed
                if event.key == pygame.K_a:
                    self.temp_xvel -= -self.WalkSpeed
                if event.key == pygame.K_d:
                    self.temp_xvel -= self.WalkSpeed  
        self.xvelocity = 0
        self.yvelocity = 0
        if self.AbleToMove == True:
            self.xvelocity += self.temp_xvel
            self.yvelocity += self.temp_yvel


class Slime(Default_Object):
    def __init__(self,x,y,angle,RootPic):
        super().__init__(x,y,angle,RootPic, MaxHealth=200,Damage=20,WalkSpeed=200,KnockBack=0.5,KnockBackTime=0.04)
        self.Layer = "SlimeLayer"
        self.InteractLayers = WallLayer + WeaponLayer
        EnemyLayer.append(self)
        self.IsTrigger = True
        logger.info("Slime initialized")
    
    def Update_Obj_specific(self):
        self.InteractLayers = WallLayer + PlayerLayer

        def On_Collision(obj,object2):
            if object2.IsTrigger:
                Log.Damage(obj,object2)

        Log.Move_and_Collide_preset(self,On_Collision)

class Wall:
    def __init__(self,x,y,angle,RootPic):
        #X and Y
        self.x = x
        self.y = y

        self.IsActive = True
        self.IsCluster = False
        #Misc
        self.RootPic = RootPic
        self.RootPic = pygame.transform.scale_by(self.RootPic,2)
        self.OriginPic = self.RootPic
        self.pic = self.OriginPic
        self.PicAngle = angle
        self.Layer = "WallLayer"
        self.height = self.OriginPic.get_height()
        print (f"height: {self.height}")
        self.width = self.OriginPic.get_width()
        print (f"width: {self.width}")
        if self.PicAngle != 0:
            self.Hitbox = self.OriginPic.get_rect(center= (self.x,self.y))
            #New Hitbox
            #Points
            Rotate_Point = self.Hitbox.center
            #Maths
            Radians_angle = math.radians(self.PicAngle)
            cos_rad = math.cos(Radians_angle)
            sin_rad = math.sin(Radians_angle)
            #Top
            #Roman, Fedor, If you're looking at this code and wondering why i put the variables in (), IT MAKES IT PRETTIER!! SHUT
            Top_Left_Offset_X,Top_Left_Offset_Y = (self.Hitbox.topleft[0] - Rotate_Point[0]),(self.Hitbox.topleft[1] - Rotate_Point[1])
            Top_Right_Offset_X,Top_Right_Offset_Y = (self.Hitbox.topright[0] - Rotate_Point[0]),(self.Hitbox.topright[1] - Rotate_Point[1])
            #Bottom
            Bottom_Left_Offset_X,Bottom_Left_Offset_Y = (self.Hitbox.bottomleft[0] - Rotate_Point[0]), (self.Hitbox.bottomleft[1] - Rotate_Point[1])
            Bottom_Right_Offset_X,Bottom_Right_Offset_Y = (self.Hitbox.bottomright[0] - Rotate_Point[0]),(self.Hitbox.bottomright[1] - Rotate_Point[1])

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

        self.IsTrigger = False
        Default_Objects.append(self)
        WallLayer.append(self)
        logger.info("Wall initialized")
    def Update_Hitbox(self):
        Log.Update_hitbox_image_based(self)
         
    def Update_Obj_specific(self):
        pass
    
    def Update_class(self):
        pass

class Grid:
    def __init__(self, start_x, start_y, width, height, cell_size):
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.array = []

        for x in range(0, self.width, self.cell_size):
            for y in range(0, self.height, self.cell_size):
                self.array.append((x,y))
        logger.info("Grid initialized")

    def get_cell(self, x, y):
        if x>=0 & y>=0 & x<self.array[-1][0] & y<self.array[-1][1]:
            random_iter = 0
            for unit in self.array:
                if unit == (x,y):
                    return random_iter
                random_iter+=1
        else:
            raise "Incorrect cell x, y given..."




#--__--
class Weapons:
    def __init__(self,x,y,angle,damage,Hitbox_cluster,KnockBack,KnockBackTime):
        self.x = x
        self.y = y
        self.angle = angle
        self.damage = damage
        self.KnockBack = KnockBack
        self.KnockBackTime = KnockBackTime

        self.IsActive = True
        self.Hitbox_active = False
        self.IsCluster = True

        self.Hitbox_cluster = Hitbox_cluster
        self.Layer = "WeaponLayer"
        logger.info("Weapon initialized")

    def Summon_weapon(self):
        WeaponLayer.append(self)
        self.IsActive = True
        for hitbox in self.hitbox_cluster:
            hitbox.IsActive = True
            hitbox.CurrentTime = 0


class Swipe(Weapons):
    def __init__(self, x, y, angle,player):
        #Prefixes
        MiddleHitbox = Empty_Hitboxes(x,y,angle,width=100,height=40,LifeTime=1,Layer=WeaponLayer)
        LeftHitbox = Empty_Hitboxes(x - MiddleHitbox.Hitbox.width,y,angle,width=40,height=20,LifeTime=1.1,Layer=WeaponLayer)
        RightHitbox = Empty_Hitboxes(x + MiddleHitbox.Hitbox.width,y,angle,width=40,height=20,LifeTime=0.9,Layer=WeaponLayer)
        
        Hitbox_cluster = [MiddleHitbox,LeftHitbox,RightHitbox]
        super().__init__(x, y, angle, damage=20 * player.Damage_multi, Hitbox_cluster=Hitbox_cluster,KnockBack=100,KnockBackTime=0.2)
        logger.info("Weapon swipe initialized")