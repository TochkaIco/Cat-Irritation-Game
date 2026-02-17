import pygame
import numpy as np
import random
from pathlib import Path
from scipy.interpolate import CubicSpline
import logging
logger = logging.getLogger(__name__)

#So I have remade almost the entire island generation code to use Pygame Surfaces directly
#This should be way faster and easier to manage. Ask me if you have questions. Roman

#Configuration stuff
IslandSize = 4096
n = 15
min_r = 0.8
extra_points = 1000
jaggedness = 0.25
num_flowers = 1000
water_color = [25, 76, 204]  #Water color (blue)
ground_color = [25, 153, 51]  #Ground color (green)

logger.info("MapGenerator start...")

def load_flowers(folder_path):
    logger.info(f"Loading images from {folder_path}")
    path = Path(folder_path)
    #Search for all png files
    flower_files = list(path.glob("*.png"))
    
    if not flower_files:
        logger.info(f"No flower images found in {folder_path}")
        print(f"You fucked up: No flowers found in {folder_path}")
        return []

    images = []
    for f in flower_files:
        img = pygame.image.load(str(f)).convert_alpha()
        #Making them 2x bigger (as we discassed with Adam)
        w, h = img.get_size()
        img = pygame.transform.scale(img, (w * 2, h * 2))
        images.append(img)
    return images

def Generate_Island_BG():
    logger.info(f"Generating Island BG...")
    #Spaming to the system, to prevent "No response"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            #pygame.DoABarrelRoll!!!!

    #Dots Generation
    np.random.seed()
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    points = []
    for a in angles:
        r = min_r + (np.random.rand() - 0.5) * jaggedness
        points.append([r * np.cos(a), r * np.sin(a)])
    points = np.array(points)

    #Making the border smooth by generating 1000 extra points
    pts_closed = np.vstack([points, points[0]])
    t = np.arange(len(pts_closed))
    t_smooth = np.linspace(0, len(points), extra_points, endpoint=False)
    cs_x = CubicSpline(t, pts_closed[:, 0], bc_type='periodic')
    cs_y = CubicSpline(t, pts_closed[:, 1], bc_type='periodic')
    sx, sy = cs_x(t_smooth), cs_y(t_smooth)

    #Now we use Pygame Surface directly for simplicity
    island_surface = pygame.Surface((IslandSize, IslandSize))
    island_surface.fill(water_color) #Water (blue)

    #Convert coordinates for pygame
    px = ((sx + 1) * IslandSize / 2).astype(int)
    py = ((sy + 1) * IslandSize / 2).astype(int)
    polygon_points = list(zip(px, py))

    #This thing should be way faster than drawing line by line
    pygame.draw.polygon(island_surface, ground_color, polygon_points) #Ground (green)

    #Fancy flower generation
    flower_sprites = load_flowers("Images/Flowers")
    
    if flower_sprites:
        placed = 0
        
        while placed < num_flowers:
            #Randomly pick from land area 
            #Basicly we gamble until we find a green pixel (shoyld be ok in our case)
            x = random.randint(0, IslandSize - 1)
            y = random.randint(0, IslandSize - 1)
            
            if island_surface.get_at((x, y))[:3] == tuple(ground_color):
                flower = random.choice(flower_sprites)
                rect = flower.get_rect(center=(x, y))
                
                #Baking them into one surface
                island_surface.blit(flower, rect)
                placed += 1
    logger.info("Returning island surface")
    return island_surface