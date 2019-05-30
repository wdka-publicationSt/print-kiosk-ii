#!/usr/bin/env python3

#####
# Script downloads all the namescpace 0 (Main) onto a dictionary
# Dictionary is dumped onto all_pages.json
#####
import json
from datetime import datetime
from wikisite import *
from functions import count_article_length  # TODO : mv2 text_processing/
from utility_scripts.utilities import findpaths


path_file, path_dir, path_parentdir = findpaths(__file__)
all_pages = path_dir + '/' + 'all_pages.json'


f = open(all_pages, 'w')


def all_pages_dict():
    mainpages = site.allpages(namespace=0)  # namespace=0 is the Main
    pages_dict = {}
    for n, page in enumerate ( list(mainpages)):
        page_title = page.page_title
        pages_dict[page_title] = {}  # sub dictionary for each page
        pages_dict[page_title]["id"] = page.pageid
        pages_dict[page_title]["title"] = page.page_title
        pages_dict[page_title]["text"] = (site.api('parse', pageid=pages_dict[page_title]["id"]))['parse']['text']['*']  # html text
        pages_dict[page_title]["length"] = count_article_length(pages_dict[page_title]["text"])  # length of the article (number of words)
        pages_dict[page_title]["extlinks"] = list(page.extlinks())
        pages_dict[page_title]["categories"] = [cat.page_title for cat in list(page.categories())]  # .page_title because categories are a also pages, and presented as such
        pages_dict[page_title]["images"] = [img.page_title for img in list(page.images())]  # img.name #includes 'File:' in response
        revisions = list(page.revisions())
        contributors = list(set([rev['user'] for rev in revisions]))
        pages_dict[page_title]['contributors'] = contributors
        pages_dict[page_title]["revisions"] = {
                           "recent_revision_user": revisions[0]['user'],
                           "recent_revision_time": revisions[0]['timestamp'],
                           "recent_revision_time_iso":datetime(*(revisions[0]['timestamp'])[:6]).isoformat(),
                           "recent_revision_comment": revisions[0]['comment'],
                           "first_revision_user": revisions[-1]['user'],
                           "first_revision_time": revisions[-1]['timestamp'],
                           "first_revision_time_iso":datetime(*(revisions[-1]['timestamp'])[:6]).isoformat(),
                           "first_revision_comment": revisions[-1]['comment']
                           # time info comes in time.struct_time format
                           # making possible to query with  time.tm_year time.tm_mon
                          }
    return pages_dict


json.dump(all_pages_dict(), f, indent=4)
# from pprint import pprint
# pprint(pages_dict, indent=4)
f.close()
