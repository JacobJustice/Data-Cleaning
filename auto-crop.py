from PIL import Image
import numpy as np
from os import listdir
from os.path import isfile, join
import os

import cv2

import argparse
import sys


"""
crop_image

Image cropping script designed to crop an image to a computed bounding box
and then resize the image to a fixed resolution

The bounding box is computed by finding the highest, lowest, rightmost and leftmost
pixel that is non-white (determined by a threshold).

@param image_fn: path to file
@param white_threshold: determines the acceptable difference from [255,255,255]
     that the pixel can be
@param output_directory: where the cropped images will go

@output: returns nothing but saves the cropped image to output_directory
"""
def crop_image(image_fn, directory="./images/", output_directory='./outputs/'):
    print("Loading:", directory+image_fn)
    try:
        pil_image = Image.open(directory + image_fn)
        image = np.array(pil_image)
        edges = cv2.Canny(image,20,100)
        edge_image = Image.fromarray(edges)
        edge_image.save("edges.jpeg")

        max_i = -99999
        min_i = 99999
        max_j = -99999
        min_j = 99999

        for i, row in enumerate(edges):
            for j, pixel in enumerate(row):

                # if the pixel is an edge
                if pixel == 255:
                    # check if i and j are greater or
                    # lower than the current maxes and mins
                    if i < min_i:
                        min_i = i
                    elif i > max_i:
                        max_i = i
                    if j < min_j:
                        min_j = j
                    elif j > max_j:
                        max_j = j

        print("min i:", min_i,"\t","max i:", max_i)
        print("min j:", min_j,"\t","max j:", max_j)
        pil_image = pil_image.crop((min_j, min_i, max_j, max_i))
        pil_image = pil_image.resize((13,10))

        save_string = output_directory + image_fn[:-4]+'.png'
        print("Saving...",save_string,'\n')
        pil_image.save(save_string)

    except KeyboardInterrupt as e:
        print(e)
        print("Exiting program...")
        sys.exit()
    except:
        e = sys.exc_info()
        print("Error loading image: ",e,"\n")


"""
crop_directory

opens a directory and calls crop_image on each file in the directory

@param directory_path: path to desired directory
"""
def crop_directory(directory_path, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    onlyfiles = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]

    for image in onlyfiles:
        crop_image(image, directory_path, output_directory)

"""
main

"""
def main():
    parser = argparse.ArgumentParser(description='Auto-crop a directory of images')
    parser.add_argument('-d','--directory', required=True, help='directory you wish to auto-crop all images in')
    parser.add_argument('-o','--output', default='./outputs/', help='desired output directory')
    args = parser.parse_args(sys.argv[1:])

    crop_directory(args.directory, args.output)

if __name__ == "__main__":
    main()
