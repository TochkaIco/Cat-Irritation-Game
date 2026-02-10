from PIL import Image
from pathlib import Path

#This script we gonna use for making prefabs on the scene out of pixel image by replacing every pixel with a specific texture block

path = Path("Images/Prefabs")
images = list(path.glob("*.png"))
if len(images) > 0:
    print("Found " + str(len(images)) + " images in the folder.")
else:
    print("No images found in the folder.")
targetpixels = []
x = 0

def color_enterpretation(number_color):
    if number_color == (255, 0, 0, 255) or number_color == (255, 0, 0):
        return "Red"
    elif number_color == (0, 209, 15, 255) or number_color == (0, 209, 15):
        return "Green"
    elif number_color == (0, 6, 255, 255) or number_color == (0, 6, 255):
        return "Blue"
    elif number_color == (0, 0, 0, 255) or number_color == (0, 0, 0):
        return "Black"
    else:
        return "Unknown + " + str(number_color)

#Go through each pixel in every image and if it it's a debug color - add it to the targetpixels list
for image in images:
    print("Processing image: " + str(image))
    newimage2 = Image.open(image)
    pix = newimage2.load()
    print("Image size: " + str(newimage2.size))
    while x < newimage2.width:
        y = 0
        while y < newimage2.height:
            if not (pix[x, y] == (255, 255, 255, 255) or pix[x, y] == (255, 0, 246, 255)): #If the pixel is not white or debug (purpl), we consider it as a target pixel
                number_color = pix[x, y]
                color = color_enterpretation(number_color)
                targetpixels.append((x, y, image.stem, color))
                print("Found target pixel at: " + str((x, y, image.stem, color)))
            y += 1
            #print(" y: " + str(y))
        x += 1
        #print(" x: " + str(x))

if len(targetpixels) > 0:
    print("Found " + str(len(targetpixels)) + " target pixels in the image.")
    print(targetpixels)
else:
    print("No target pixels found in the image.")