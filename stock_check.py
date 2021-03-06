from PIL import Image
import imagehash

from os import listdir
from os.path import isfile, join

image_dir = './outputs/aj1/'
hash0 = imagehash.average_hash(Image.open('./outputs/aj1/AJ1CB-SBBTD.png')) 
cutoff = 1

# 
#@param hash0: imagehash value of stockx logo
#@param hash1: image to be compared to stockx logo
#
def stock_check(hash0, imagedir, hash1_image):
    hash1 = imagehash.average_hash(Image.open(image_dir+hash1_image))
    if hash0 - hash1 < cutoff:
      print('images are similar', hash1_image)


from os import listdir
from os.path import isfile, join
from pprint import pprint


onlyfiles = [f for f in listdir(image_dir) if isfile(join(image_dir, f))]

for image in onlyfiles:
    stock_check(hash0, image_dir, image)

