#!/usr/bin/env python3

##### 
# Script downloads all the namescpace 0 (Main) onto a dictionary
# Dictionary is dumped onto all_pages.json
#####
from mwclient import Site
from mwclient.listing import List
#from mwclient import Page
from argparse import ArgumentParser
from pprint import pprint
from datetime import datetime
import json
p = ArgumentParser()
p.add_argument("--host", default="beyond-social.org")
p.add_argument("--path", default="/wiki/", help="nb: should end with /")
args = p.parse_args()


site = Site(('http',args.host), args.path)
print(site)

f = open('all_pages.json', 'w')

def all_pages_dict():
    mainpages = site.allpages(namespace=0) # namespace=0 is the Main
    for n, page in enumerate ( list(mainpages) ):
        pages_dict = {}
        page_id =  str(page.pageid)
        pages_dict[page_id] = {} # sub dictionary for each page
        pages_dict[page_id]["id"] =  page.pageid 
        pages_dict[page_id]["title"] = page.page_title        
        pages_dict[page_id]["text"] = page.text() 
        #print(pages_dict[page_id]["text"])
        pages_dict[page_id]["extlinks"] = list(page.extlinks())
        pages_dict[page_id]["categories"] = [cat.page_title for cat in list(page.categories())] # .page_title because categories are a also pages, and presented as such
        pages_dict[page_id]["lastedittime"] = page.edit_time
        pages_dict[page_id]["images"] = [img.page_title for img in list(page.images())] #img.name #includes 'File:' in response
        pages_dict[page_id]["revisions"] = { "recent_revision_user": list(page.revisions())[0]['user'],
                           "recent_revision_time": list(page.revisions())[0]['timestamp'],
                           "recent_revision_time_iso":datetime(*(list(page.revisions())[0]['timestamp'])[:6]).isoformat(),
                           "last_revision_user": list(page.revisions())[-1]['user'],
                           "last_revision_time": list(page.revisions())[-1]['timestamp'],
                           "last_revision_time_iso":datetime(*(list(page.revisions())[-1]['timestamp'])[:6]).isoformat()

                           # time info comes in time.struct_time format
                           # making possible to query with  time.tm_year time.tm_mon

                           }
        return pages_dict



json.dump( all_pages_dict(), f, indent=4)    
    #pprint(pages_dict, indent=4)        
f.close()
