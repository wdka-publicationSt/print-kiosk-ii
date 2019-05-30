#!/usr/bin/env python3

###
# Script downloads all wiki images onto the img/ dir
# 1 it begins by getting a list of all images form API
# 1.1 if the image file IS NOT stored in the images folder: it downloads it
###

import os, urllib.request, json
from hashlib import sha1
from wikisite import *
from pprint import pprint
from utility_scripts.utilities import findpaths

wiki_images = site.images
api = '{protocol}://{host}{path}api.php?'.format(protocol='https',
                                                 host=site.host,
                                                 path=site.path)
set_hight = 800
path_file, path_dir, path_parentdir = findpaths(__file__)
img_dir = path_dir + '/images/'
if os.path.exists(img_dir) is False:
    os.mkdir(img_dir)
img_dir_files = os.listdir(img_dir)


for wiki_img in list(wiki_images):
    # Download image if is png, jpg, gif and is being used
    if (wiki_img.page_title.replace(' ','_')) not in img_dir_files and \
        ((wiki_img.page_title).split('.')[-1]).lower() \
        in ['png', 'jpg', 'gif'] and \
            len(list(wiki_img.imageusage())) > 0:
        print(wiki_img.page_title)
        info = wiki_img.imageinfo
        # pprint(info)
        height = info['height']
        size = info['size']
        if height > set_hight:  # request a thumb
            api_thumb_action = 'action=query&format=json&prop=imageinfo&iiprop=url&iiurlheight={height}&titles={page}'.format(
                height= str(set_hight) ,
                page=wiki_img.name.replace(" ", "_"))
            api_query = api + api_thumb_action
            api_query = urllib.parse.quote(api_query)
            try:  # try getting the thumbnail file url 
                with urllib.request.urlopen(api_query) as response:
                    api_thumb = response.read().decode('utf-8')
                    api_thumb = json.loads(api_thumb)
                    api_thumb_key = [*api_thumb['query']['pages'].keys()][0]
                    url = api_thumb['query']['pages'][api_thumb_key]['imageinfo'][0]['thumburl']
            except: # if cannot get thumb go with original :/
                url = info['url'].replace(" ", "_")

                # print(url)
        else:  # request regular image
            url = info['url'].replace(" ", "_")


        img_title = wiki_img.page_title.replace(' ', '_')
        try:
            urllib.request.urlretrieve(url, img_dir + img_title)
            print('Image: {} not found. Downloading it!'.format(
                wiki_img.page_title))
        except:
            print("Error downloading {}".format(url))
    else:
        print("{} already present in images dir".format(
            wiki_img.page_title))
