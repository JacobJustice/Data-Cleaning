import csv
import numpy as np
from PIL import Image
from os import listdir
from os.path import isfile, join

from pprint import pprint

"""
given an RGB image, flatten it and add it's name as a title

generate a name for each pixel and each color within it

return a dictionary with each titled pixel

ex: {'ticker':

"""
def generate_row(image_name, directory_path="./", header="filename"):
    output_dict = {header:image_name[image_name.rfind('/')+1:image_name.rfind('.')]}
    print("Loading image:", image_name)
    image = np.array(Image.open(directory_path + image_name))
    image = image.flatten()

    for i, pixel_value in enumerate(image):
        entry_title = "pixel" + str(i // 3)
        if i % 3 == 0:
            entry_title += "_r"
        elif i % 3 == 1:
            entry_title += "_g"
        else:
            entry_title += "_b"

        output_dict.update({entry_title:pixel_value})

    return output_dict

"""
generates a csv with rows containing rgb pixel info from images and 
an identifier using all image files within a directory

all images in the directory should be the same resolution

@param directory_path: path to directory containing images
@param header: the string title of the image identifier
@param csv_output_name: allows you to specify what the filename of the csv will be 
"""
def generate_csv_from_directory(directory_path="./", header="filename", csv_output_name="output.csv"):
    onlyfiles = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]

    with open(csv_output_name, 'w', newline='') as csvfile:
        csvwriter = None
        for i, image in enumerate(onlyfiles):
            if i==0:
                first_row = generate_row(image, directory_path, header=header)
                csvwriter = csv.DictWriter(csvfile, fieldnames=first_row.keys())
                csvwriter.writeheader()
                csvwriter.writerow(first_row)
            else:
                print(i)
                csvwriter.writerow(generate_row(image, directory_path, header=header))
                print()

    return 

def main():
    print(generate_csv_from_directory("./outputs/"))

if __name__ == "__main__":
    main()
