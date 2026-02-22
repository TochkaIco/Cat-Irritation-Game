#No more PIL, yeay
import pygame
import random
from pathlib import Path
import Classes
import logging
import MapGenerator
logger = logging.getLogger(__name__)

#This script we gonna use for making prefabs on the scene out of pixel image by replacing every pixel with a specific texture block

#Func to check prefs, find place, optimize and spawn
def Load_And_Spawn_Prefabs_Optimized(block_texture, island_surface):
    folder_path = Path("Images/Prefabs")
    images = list(folder_path.glob("*.png"))
    
    if not images:
        logger.warning(f"No prefabs found in {folder_path}!")
        print(f"No prefabs found in {folder_path}!")
        return

    #Mult everything by 2
    base_w = block_texture.get_width()
    base_h = block_texture.get_height()
    step_w = base_w * 2  
    step_h = base_h * 2

    #For a check proccess
    island_size = island_surface.get_width()
    ground_color_tuple = tuple(MapGenerator.ground_color)
    occupied_rects = []

    #Go through each image
    for img_path in images:
        prefab_surface = pygame.image.load(str(img_path)).convert_alpha()
        img_width, img_height = prefab_surface.get_size()
        
        #Actual size
        prefab_physical_w = img_width * step_w
        prefab_physical_h = img_height * step_h
        
        #Find random place
        valid_position = False
        start_x, start_y = 0, 0
        
        #Just why not, give it 200 attempts, so we dont run into inf loop
        for attempt in range(200):
            rx = random.randint(0, island_size - prefab_physical_w - 1)
            ry = random.randint(0, island_size - prefab_physical_h - 1)
            test_rect = pygame.Rect(rx, ry, prefab_physical_w, prefab_physical_h)
            
            #Check 1 - does something overlays?
            if test_rect.collidelist(occupied_rects) != -1:
                continue
                
            #Check 2 - is full on land (4 corners)
            points_to_check = [
                test_rect.topleft, test_rect.topright,
                test_rect.bottomleft, test_rect.bottomright,
                test_rect.center
            ]
            
            on_land = True
            for px, py in points_to_check:
                color_at_pos = island_surface.get_at((int(px), int(py)))
                #Check rgb without alfa
                if color_at_pos[:3] != ground_color_tuple:
                    on_land = False
                    break
                    
            if on_land:
                valid_position = True
                start_x, start_y = rx, ry
                #Reserv place
                occupied_rects.append(test_rect)
                break
                
        if not valid_position:
            logger.warning(f"Could not find free space on land for {img_path.name}. Skip.")
            print(f"Skipping {img_path.name}: No space or too many overlaps.")
            continue
            
        print(f"Spawning {img_path.name} at X:{start_x} Y:{start_y}")

        #Save pic into a massive with color save
        #I finally understood how to do a grid properly
        grid = [[None for _ in range(img_height)] for _ in range(img_width)]
        for x in range(img_width):
            for y in range(img_height):
                color = prefab_surface.get_at((x, y))
                #If not white or deubg-purple
                if color != (255, 255, 255, 255) and color != (255, 0, 246, 255) and color[3] > 0:
                    grid[x][y] = color

        #Greedy Meshing is a cool thing
        for y in range(img_height):
            for x in range(img_width):
                target_color = grid[x][y]
                #Find a piece
                if target_color is not None:
                    #Stretch up right if color is right
                    w = 1
                    while x + w < img_width and grid[x + w][y] == target_color:
                        w += 1
                    #Stretch down left if color is right
                    h = 1
                    can_expand_down = True
                    while y + h < img_height and can_expand_down:
                        for i in range(w):
                            if grid[x + i][y + h] != target_color:
                                can_expand_down = False
                                break
                        if can_expand_down:
                            h += 1
                    #Mark the spot
                    for ix in range(w):
                        for iy in range(h):
                            grid[x + ix][y + iy] = None
                    #Make a surf
                    merged_surface = pygame.Surface((w * base_w, h * base_h), pygame.SRCALPHA)
                    #Coloring
                    tinted_block = block_texture.copy()
                    tinted_block.fill(target_color, special_flags=pygame.BLEND_RGBA_MULT)
                    for ix in range(w):
                        for iy in range(h):
                            merged_surface.blit(tinted_block, (ix * base_w, iy * base_h))
                    #Finding center and spawning as a wall
                    world_center_x = start_x + (x * step_w) + (w * step_w) / 2
                    world_center_y = start_y + (y * step_h) + (h * step_h) / 2
                    Classes.Wall(world_center_x, world_center_y, 0, merged_surface)