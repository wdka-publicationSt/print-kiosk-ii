#!/usr/bin/env python3

##### 
# Script downloads all the namescpace 0 (Main) onto a dictionary
# Dictionary is dumped onto all_pages.json
#####
from wikisite import *

from pprint import pprint
from datetime import datetime
import json

f = open('all_pages.json', 'w')

def all_pages_dict():
    mainpages = site.allpages(namespace=0) # namespace=0 is the Main
    pages_dict = {}
    for n, page in enumerate ( list(mainpages) ):
        page_title = page.page_title
        pages_dict[page_title] = {} # sub dictionary for each page
        pages_dict[page_title]["id"] =  page.pageid 
        pages_dict[page_title]["title"] = page.page_title        
        pages_dict[page_title]["text"] = (site.api('parse',  pageid = pages_dict[page_title]["id"]))['parse']['text']['*'] # html text
        #print(pages_dict[page_title]["text"])
        pages_dict[page_title]["extlinks"] = list(page.extlinks())
        pages_dict[page_title]["categories"] = [cat.page_title for cat in list(page.categories())] # .page_title because categories are a also pages, and presented as such
        pages_dict[page_title]["images"] = [img.page_title for img in list(page.images())] #img.name #includes 'File:' in response
        pages_dict[page_title]["revisions"] = { "recent_revision_user": list(page.revisions())[0]['user'],
                           "recent_revision_time": list(page.revisions())[0]['timestamp'],
                           "recent_revision_time_iso":datetime(*(list(page.revisions())[0]['timestamp'])[:6]).isoformat(),
                           "first_revision_user": list(page.revisions())[-1]['user'],
                           "first_revision_time": list(page.revisions())[-1]['timestamp'],
                           "first_revision_time_iso":datetime(*(list(page.revisions())[-1]['timestamp'])[:6]).isoformat()

                           # time info comes in time.struct_time format
                           # making possible to query with  time.tm_year time.tm_mon

                           }
    
    return pages_dict




json.dump( all_pages_dict(), f, indent=4)    
    #pprint(pages_dict, indent=4)        
f.close()
