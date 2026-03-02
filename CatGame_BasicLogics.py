import math
from pygame import time
from pygame import rect 
# Use 'Rect' for class, 'rect' for module functions
from pygame import Rect
import logging
logger = logging.getLogger(__name__)
clock = time.Clock()
DeltaTime = 0.1
# Collision logic
#
#--
#Regular player preset for collision and other logic, change as necessary
def Move_and_Collide_preset(obj, On_Collision):
    #- Xvalue
    velocity_magnitute = math.sqrt(obj.xvelocity**2 + obj.yvelocity**2)
    if velocity_magnitute > 0:
        normalized_x = (obj.xvelocity / velocity_magnitute) * obj.WalkSpeed
        obj.Hitbox.x += normalized_x * DeltaTime   
    #_-_
    for object2 in obj.InteractLayers:
        if object2.IsActive == True:
            if object2.IsCluster == True:
                for hitbox in object2.Hitbox_cluster:
                    Collided, Func = Check_Collisions(obj,hitbox,"X")
                    if Collided == True:
                        Func(obj,object2)
            else:
                Collided, Func = Check_Collisions(obj,object2,"X")
                if Collided == True:
                    Func(obj,object2)

    #- Yvalue
    if velocity_magnitute > 0:  
        normalized_y = (obj.yvelocity / velocity_magnitute) * obj.WalkSpeed
        obj.Hitbox.centery += normalized_y * DeltaTime
    #_-_
    for object2 in obj.InteractLayers:
        if object2.IsActive == True:
            if object2.IsCluster == True:
                for hitbox in object2.Hitbox_cluster:
                    Collided, Func = Check_Collisions(obj,object2,"Y")
                    if Collided == True:
                        Func(obj,object2)
                        if On_Collision != None:
                            On_Collision(obj,object2)
                        break
            else:
                Collided, Func = Check_Collisions(obj,object2,"Y")
                if Collided == True:
                    Func(obj,object2)
                    if On_Collision != None:
                        On_Collision(obj,object2)



#Quick note to the rest of you, if you look at the code then yes, we could put
# the damage inside of the Func() of Check_Collisions, but what if we
# don't want every obj to damage? maybe one attack freezes instead?
#
# We could give every object a Func, that would fix it and make the code better
# I will do it later, or one of you can do it.
        
def Timer(self,LifeTime,CurrentTime):
    if self.LifeTime != 0:
        if CurrentTime < LifeTime:
            self.CurrentTime += DeltaTime
            return False
        if CurrentTime > LifeTime:
            return True
    else:
        return False


def Nothing(*_):
    pass



#--
def CheckObbCollisions(obj1, obj2):
    """Checks for collision between two objects using the Separating Axis Theorem (SAT)."""
    # Potential axes to check: the normals to the edges of both boxes.
    # For rectangles, this is just the local X and Y axes of each box.
    
    def get_axes(obj):
        # We need two perpendicular axes for each object.
        # Since these are rectangles, we can use the vectors from point 0 to 1 and 0 to 2.
        p0 = obj.Points[0]
        p1 = obj.Points[1]
        p2 = obj.Points[2]
        
        axis1 = (p1[0] - p0[0], p1[1] - p0[1])
        axis2 = (p2[0] - p0[0], p2[1] - p0[1])
        
        # Normalize
        len1 = math.sqrt(axis1[0]**2 + axis1[1]**2)
        len2 = math.sqrt(axis2[0]**2 + axis2[1]**2)
        
        if len1 == 0 or len2 == 0:
            return []
            
        return [(axis1[0]/len1, axis1[1]/len1), (axis2[0]/len2, axis2[1]/len2)]

    axes = get_axes(obj1) + get_axes(obj2)
    
    for axis in axes:
        # Project both objects onto the axis
        def project(obj, axis):
            min_proj = math.inf
            max_proj = -math.inf
            for p in obj.Points:
                proj = p[0] * axis[0] + p[1] * axis[1]
                if proj < min_proj: min_proj = proj
                if proj > max_proj: max_proj = proj
            return min_proj, max_proj
        
        min1, max1 = project(obj1, axis)
        min2, max2 = project(obj2, axis)
        
        # Check for separation
        if max1 < min2 or max2 < min1:
            return False # Found a separating axis, no collision
            
    return True # No separating axis found, they are colliding

def Check_Collisions(obj,object2,MoveAxis):
    Collided = False
    Func = Nothing

    if obj.angle != 0 or object2.angle != 0:
        Collided = CheckObbCollisions(obj,object2)
        if object2.IsTrigger == False:
            Func = Angled_Collision_React
    else:
        Collided = obj.Hitbox.colliderect(object2.Hitbox)
        #print(f"{obj} and {object2} collided")
        if object2.IsTrigger == False:
            if MoveAxis == "X":
                Func = XCollision_React_0
            elif MoveAxis == "Y":
                Func = YCollision_React_0
    return Collided, Func


def Angled_Collision_React(obj,object2):
    obj.Update_Hitbox()
    object2.Update_Hitbox()
    #-_
    if obj.Hitbox.centery < object2.Hitbox.centery: YDirection = -1 
    else: YDirection = 1
    if obj.Hitbox.centerx > object2.Hitbox.centerx: XDirection = 1
    else: XDirection = -1
    if object2.angle < 0:
        YDirection *= -1
        XDirection *= -1
    #Getting the points to compare pos to
    if object2.Points[0][1] > object2.Points[1][1]: TopYPoint, BottomYPoint, LeftXPoint, RightXPoint, ObjPIndex = object2.Points[1][0], object2.Points[0][1], object2.Points[3][1], object2.Points[2][0], 1
    else: TopYPoint, BottomYPoint, LeftXPoint, RightXPoint, ObjPIndex = object2.Points[1][1], object2.Points[2][1], object2.Points[0][0], object2.Points[3][0], 0     

    #tan v
    RadAngle = math.radians(object2.angle)
    Xadd = (object2.width / 2 + (object2.width / 2 * math.tan(RadAngle)) * math.tan(RadAngle/2))
    Yadd = (object2.height / 2 + (object2.height / 2 * math.tan(RadAngle)) * math.tan(RadAngle/2))
    Ey_height = (obj.Hitbox.centerx - object2.Hitbox.centerx) * math.tan(RadAngle) * YDirection
    Ex_height = (obj.Hitbox.centery - object2.Hitbox.centery) * math.tan(RadAngle) * -XDirection
    #top
    #Eye of rahh checks if the obj is below or above (might be redundant)
    CollidedOnY = False
    #---__---
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

def Get_Points(obj,object2):
    if object2.Points[0][1] > object2.Points[1][1]: 
        TopYPoint, BottomYPoint, LeftXPoint, RightXPoint, ObjPIndex = object2.Points[1][0], object2.Points[0][1], object2.Points[3][1], object2.Points[2][0], 1
    else: 
        TopYPoint, BottomYPoint, LeftXPoint, RightXPoint, ObjPIndex = object2.Points[1][1], object2.Points[2][1], object2.Points[0][0], object2.Points[3][0], 0

    
    pass


def XCollision_React_0(obj,object2):
    if obj.Hitbox.colliderect(object2.Hitbox):
        if obj.xvelocity > 0:
            obj.Hitbox.right = object2.Hitbox.left
        if obj.xvelocity < 0:
            obj.Hitbox.left = object2.Hitbox.right
        obj.x = obj.Hitbox.center[0]

def YCollision_React_0(obj,object2):
    if obj.Hitbox.colliderect(object2.Hitbox):
        if obj.yvelocity > 0:
            obj.Hitbox.bottom = object2.Hitbox.top
        if obj.yvelocity < 0:
            obj.Hitbox.top = object2.Hitbox.bottom
        obj.y = obj.Hitbox.center[1]

#Knockback
#
def Damage(obj,object2):
    #Checks if obj1 has already been damaged by object2
    for i_frame_tracker in object2.IFrame_Trackers:
        #print(f"Victim: {i_frame_tracker.victim}")
        #print(f"obj: {obj}")
        if i_frame_tracker.victim == obj:
            print("stopped hit")
            return None
    obj.Health -= object2.Damage
    direction = math.atan2(obj.Hitbox.centery - object2.Hitbox.centery,obj.Hitbox.centerx - object2.Hitbox.centerx)
    Obj_Logic_Handler.Apply_knockback(obj,object2.KnockBack,direction,knockbacktime=object2.KnockBackTime,Should_stun=False)
    #print(f"Obj health ={obj.Health}")
    IFrameTracker(object2,obj)
    
def Update_hitbox_image_based(self):
    if self.angle == 0:
        self.Hitbox = self.OriginPic.get_rect(center= (self.x, self.y))
        #
        self.Points = (self.Hitbox.topleft, self.Hitbox.topright,self.Hitbox.bottomleft, self.Hitbox.bottomright)
        self.height = self.OriginPic.get_height()
        self.width = self.OriginPic.get_width()
    else:
        self.Hitbox = self.OriginPic.get_rect(center= (self.x,self.y))
        #New Hitbox
        #Points
        Rotate_Point = self.Hitbox.center
        #Maths
        Radians_angle = math.radians(self.angle)
        cos_rad = math.cos(Radians_angle)
        sin_rad = math.sin(self.angle)
        # Calculate vertices of the rotated rectangle
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


def Update_hitbox_dimension_based(self):
    if self.angle == 0:
        self.Hitbox = Rect(center=(self.x, self.y),width=self.width,height=self.height)
        self.Points = (self.Hitbox.topleft, self.Hitbox.topright,self.Hitbox.bottomleft, self.Hitbox.bottomright)
    else:
        self.Hitbox = Rect(center=(self.x, self.y),width=self.width,height=self.height)
        Rotate_Point = self.Hitbox.center
        Radians_angle = math.radians(self.angle)
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

#- TrackList

class IFrameTracker:
    def __init__(self,attacker,victim):
        self.time_since_hit = 0
        self.attacker = attacker
        self.victim = victim
        print(self.victim)
        #Adds a iframe tracker object
        attacker.IFrame_Trackers.append(self)
    
    def Update_time(self):
        self.time_since_hit += DeltaTime
        if self.time_since_hit > self.victim.I_frames:
            self.attacker.IFrame_Trackers.remove(self)
            del self
        
class Inventory:
    def __init__(self,parent,space):
        self.parent = parent
        self.space = space
        

class Kn_log:
    objlist = []
    powerlist = []
    directionlist = []
    knockback_time = []
    current_time = [] 
    Added = []
    Should_Stun = []
    def remove_ob(ob_num):
        Kn_log.objlist.pop(ob_num)
        Kn_log.powerlist.pop(ob_num)
        Kn_log.directionlist.pop(ob_num)
        Kn_log.knockback_time.pop(ob_num)
        Kn_log.current_time.pop(ob_num)
        Kn_log.Added.pop(ob_num)
        Kn_log.Should_Stun.pop(ob_num)

#Bigger Logic Handler
class Obj_Logic_Handler:

    #Knockback in logic handler
    #-_-
    def Apply_knockback(obj,power,direction,knockbacktime,Should_stun):
        Kn_log.objlist.append(obj)
        Kn_log.powerlist.append(power)
        Kn_log.directionlist.append(direction)
        Kn_log.knockback_time.append(knockbacktime)
        Kn_log.current_time.append(0)
        Kn_log.Added.append(False)
        Kn_log.Should_Stun.append(Should_stun)

    def Knockback():
        ob_num = 0
        for obj in Kn_log.objlist:

            if Kn_log.current_time[ob_num] < Kn_log.knockback_time[ob_num]:
                Kn_log.current_time[ob_num] += DeltaTime
                obj.xvelocity += Kn_log.powerlist[ob_num] * math.cos(Kn_log.directionlist[ob_num])
                obj.yvelocity += Kn_log.powerlist[ob_num] * math.sin(Kn_log.directionlist[ob_num])
                if Kn_log.Should_Stun[ob_num] == True:
                    obj.AbleToMove = False
            else:
                obj.xvelocity = 0
                obj.yvelocity = 0
                if Kn_log.Should_Stun[ob_num] == True:
                    obj.AbleToMove = True
                Kn_log.remove_ob(ob_num)

            ob_num += 1




#Delta Time
#
def Set_DeltaTime():
    global DeltaTime
    DeltaTime = clock.tick(60) / 1000
    DeltaTime = max(0.001, min(0.1, DeltaTime))
    return DeltaTime

def Get_DeltaTime():
    global DeltaTime
    return DeltaTime

