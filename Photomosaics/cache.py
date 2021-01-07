from PIL import Image
import os, json
from photomosaics import Add_all_pixels

def json_file(path, DIV):

    try:
        File = open('cache.json')
        print('FOUND')
        print('')

    except:
        File = open("cache.json", "w")
        print("Creating json file...")
        print('')
        folder_path = path
        
        data = {}
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            source_image = Image.open(file_path)
            resize_image =  source_image.resize((10, 10))

            pixels = resize_image.getdata()
            r2, g2, b2 = Add_all_pixels(pixels)
            r2, g2, b2 = r2//DIV, g2//DIV, b2//DIV

            # adding rgb value to dict
            data.update({filename : (r2,g2,b2)})

        json.dump(data, File)  
    File.close()
    print('')
    print("JSON File loading..... ")
