import os
import math
import json
from PIL import Image

# pixelate image
def pixelate(image, i, j, r, g, b):
    px_image = image.load()
    n = HEIGHT - SIDE
    if i <= n:
        for i_index in range(i ,i + SIDE):
            for j_index in range(j ,j + SIDE):
                px_image[j_index, i_index] = (r, g, b)

def add_all_pixels(pixels):
    r, g, b = 0, 0, 0
    for i in range(len(pixels)):
        r += pixels[i][0]
        g += pixels[i][1]
        b += pixels[i][2]
    return r, g, b

def similarity(r1, g1, b1, r2, g2, b2):
    similarity = math.sqrt( ((r2 - r1)**2) + ((g2 - g1)**2) + ((b2 - b1)**2) )
    return (round(similarity))

def source_img(r1, g1, b1, canvas, i, j):
    cache_path = r"C:\Users\ngour\cache.json"
    cache_file = open(cache_path, "r")
    data = json.load(cache_file)
    value = 300

    folder_path = r"C:\Users\ngour\data"
    for filename in os.listdir(folder_path):
        r2, g2, b2 = data[filename][0], data[filename][1], data[filename][2]  
        similar = similarity(r1 ,g1 ,b1 ,r2 ,g2 ,b2)
        if similar <= value:
            value = similar
            s_filename = filename

    file_path = os.path.join(folder_path, s_filename)
    source_img = Image.open(file_path)
    resize_img =  source_img.resize((10, 10))
    Image.Image.paste(canvas, resize_img , (i,j))

def main(image, canvas):
    # cropping a part of image one at a time 
    for i in range(0 ,HEIGHT ,SIDE):
        for j in range(0 ,WIDTH ,SIDE):
            # dimensions for cropping
            dimension = (i ,j ,i + SIDE ,j + SIDE)
            crop_img = image.crop(dimension)   
            
            # getting crop image pixels
            crop_pixels = crop_img.getdata()
            r1, g1, b1 = add_all_pixels(crop_pixels)
            # average of rgb
            r1, g1, b1 = r1//100, g1//100, b1//100
            pixelate(image, i, j, r1, g1, b1)
            #source_img(r1, g1, b1, canvas, i, j)

path = r"C:\Users\ngour\pineapple.jpg"
image = Image.open(path)
WIDTH, HEIGHT = image.size
SIDE = 10

canvas = Image.new(mode = "RGB", size = (WIDTH ,HEIGHT), color = None)
main(image, canvas)
canvas.show()