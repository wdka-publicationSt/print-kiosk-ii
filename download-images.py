#!/usr/bin/env python3

###
# Script downloads all wiki images onto the img/ dir
# 1 it begins by getting a list of all images form API
# 1.1 if the image file IS NOT stored in the images folder: it downloads it
# 1.2 if the image file IS stored in the images folder: it reads its checksum
# 1.2.2 if different (the image has changed in server) then  it downloads it
###

import os, urllib.request
from hashlib import sha1
from wikisite import *
from pprint import pprint

wiki_images = site.images

current_dir = os.path.dirname(os.path.realpath(__file__))
img_dir = os.path.dirname(os.path.realpath(__file__))+'/images/'
if os.path.exists(img_dir) is False:
    os.mkdir(img_dir)
img_dir_files = os.listdir(img_dir)

for wiki_img in list(wiki_images):
    info = wiki_img.imageinfo
    # pprint(info)
    url = (info['url'].replace(" ","_")
    size = int(info['size'])
    print(url)
    if wiki_img.page_title not in img_dir_files:
        try:
            urllib.request.urlretrieve(info['url'], img_dir + wiki_img.page_title)
            print('Image: {} not found. Downloading it!'.format(wiki_img.page_title))
        except:
            print("Error downloading {}".format(url))
    else:
        print('Image: {} in folder!'.format(wiki_img.page_title))
        local_img_size = os.path.getsize(img_dir + wiki_img.page_title)
        if local_img_size != size:
            try:
                urllib.request.urlretrieve(info['url'], img_dir + wiki_img.page_title)
                print('Image: {} in folder has DIFFERENT SIZE! Local {}, wiki {}. Downloading it'.format(wiki_img.page_title,local_img_size, size ))
            except:
                print("Error downloading {}".format(url))



