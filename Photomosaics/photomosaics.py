from PIL import Image
import os, json
import math


def pixelate(image, i, j, r, g, b):
    px_image = image.load()
    n = HEIGHT - SIDE
    if i <= n:
        for i_index in range(i ,i + SIDE):
            for j_index in range(j ,j + SIDE):
                px_image[j_index, i_index] = (r, g, b)

def Add_all_pixels(pixels):
    r, g, b = 0, 0, 0
    for i in range(len(pixels)):
        r += pixels[i][0]
        g += pixels[i][1]
        b += pixels[i][2]
    return r, g, b

def Calculate_Similarity(r1, g1, b1, r2, g2, b2):
    similarity = math.sqrt( ((r2 - r1)**2) + ((g2 - g1)**2) + ((b2 - b1)**2) )
    return (round(similarity))

def source_image(i, j, new_img, r1, g1, b1, SIDE, folder_path):
    # open rgb values file
    Filename_ = 'cache.json'
    path_ = os.path.abspath(Filename_)
    RGB_VALS = open(path_ ,"r")
    Data = json.load(RGB_VALS)
    Value = 300

    sim_filename  = None
    for filename in os.listdir(folder_path):
        r2, g2, b2 = Data[filename][0], Data[filename][1], Data[filename][2]  
        sim_value = Calculate_Similarity(r1 ,g1 ,b1 ,r2 ,g2 ,b2)
        if sim_value <= Value:
            Value = sim_value
            sim_filename = filename

    file_path = os.path.join(folder_path, str(sim_filename))
    source_img = Image.open(file_path)
    resize_img =  source_img.resize((SIDE, SIDE))
    Image.Image.paste(new_img, resize_img, (j,i))

def start(image, new_image, WIDTH, HEIGHT, SIDE, DIV, folder_path):
    # cropping a part of main_image
    for i in range(0 ,HEIGHT ,SIDE):
        for j in range(0 ,WIDTH ,SIDE):
            # dimensions for cropping
            dimensions = (j ,i ,j + SIDE ,i + SIDE)
            Crop_image = image.crop(dimensions)   
            
            # getting cropped image pixels
            Crop_img_pixels = Crop_image.getdata()
            r1, g1, b1 = Add_all_pixels(Crop_img_pixels)
            # average rgb of cropped image
            r1, g1, b1 = r1//DIV, g1//DIV, b1//DIV
            source_image(i, j, new_image, r1, g1, b1, SIDE, folder_path)
    print('image ready')
