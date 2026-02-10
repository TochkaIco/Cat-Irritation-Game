import math
from pygame import time
from pygame import rect
clock = time.Clock()
DeltaTime = 0.1

def Move_and_Collide_preset(obj):
    #- Xvalue
    velocity_magnitute = math.sqrt(obj.xvelocity**2 + obj.yvelocity**2)
    if velocity_magnitute > 0:
        normalized_x = (obj.xvelocity / velocity_magnitute) * obj.WalkSpeed
        obj.Hitbox.x += normalized_x * DeltaTime   
    for object2 in obj.InteractLayers:
        Collided, Func = Check_Collisions(obj,object2,"X")
        if Collided == True and Func != None:
            Func(obj,object2)
    #- Yvalue
    if velocity_magnitute > 0:  
        normalized_y = (obj.yvelocity / velocity_magnitute) * obj.WalkSpeed
        obj.Hitbox.centery += normalized_y * DeltaTime
    for object2 in obj.InteractLayers:
        Collided, Func = Check_Collisions(obj,object2,"Y")
        if Collided == True and Func != None:
            Func(obj,object2)

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

def Check_Collisions(obj,object2,MoveAxis):
    Collided = False
    Func = None
    if obj.PicAngle != 0 or object2.PicAngle != 0:
        Collided = CheckObbCollisions(obj,object2)
        Func = Angled_Collision_React
    else:
        Collided = obj.Hitbox.colliderect(object2.Hitbox)
        if MoveAxis == "X".lower():
            Func = XCollision_React_0
        elif MoveAxis == "Y".lower():
            Func = YCollision_React_0
    return Collided, Func


def Angled_Collision_React(obj,object2):
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


def Get_DeltaTime():
    global DeltaTime
    DeltaTime = clock.tick(60) / 1000
    DeltaTime = max(0.001, min(0.1, DeltaTime))
    return DeltaTime
