import pygame
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from matplotlib.path import Path

#IslandSize
IslandSize = 4096
n = 15
min_r = 0.8
extra_points = 1000
jaggedness = 0.25
water_color = [25, 76, 204]  #Water color (blue)
ground_color = [25, 153, 51]  #Ground color (green)

def Generate_Island_BG():
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

    px = ((sx + 1) * IslandSize / 2).astype(int)
    py = ((sy + 1) * IslandSize / 2).astype(int)

    #Creating an image
    img = np.zeros((IslandSize, IslandSize, 3), dtype=np.uint8)
    img[:] = water_color  #Water  (blue)

    #Scanline fill algorithm
    #Creating edges, each edge is a pair (start, end)
    polygon_points = list(zip(px, py))

    for y in range(IslandSize):
        intersections = []

        #Find all intersections of the contour with this horizontal line
        for i in range(len(polygon_points)):
            x1, y1 = polygon_points[i]
            x2, y2 = polygon_points[(i + 1) % len(polygon_points)]

            # Check whether the edge crosses this line
            if (y1 <= y < y2) or (y2 <= y < y1):
                #Getting the X coordinate of the intersection
                if y2 != y1:
                    t = (y - y1) / (y2 - y1)
                    x = x1 + t * (x2 - x1)
                    intersections.append(int(x))

        #Sort intersections
        intersections.sort()

        #Fill in between pairs of intersections
        for i in range(0, len(intersections) - 1, 2):
            x_start = max(0, intersections[i])
            x_end = min(IslandSize - 1, intersections[i + 1])
            if x_start <= x_end:
                img[y, x_start:x_end] = ground_color   #Ground (green)

    #Converting to an PyGame Surface
    img = np.transpose(img, (1, 0, 2))
    return pygame.surfarray.make_surface(img)