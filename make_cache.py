#! python3
import math
from PIL import Image
import os, json

def avg_rgb(pixels):
    r, g, b = 0, 0, 0
    for i in range(len(pixels)):
        r += pixels[i][0]
        g += pixels[i][1]
        b += pixels[i][2]
    return r, g, b

data = {}
file = open("cache.json", "w")
folder_path = r"C:\Users\ngour\data"
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    source_img = Image.open(file_path)
    resize_img =  source_img.resize((10, 10))

    s_pixels = resize_img.getdata()
    r2, g2, b2 = avg_rgb(s_pixels)
    r2, g2 , b2 = r2//100, g2//100, b2//100
    data.update({filename : (r2,g2,b2)})

json.dump(data, file)  
file.close()
print('done')