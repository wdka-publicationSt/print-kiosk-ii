#!/usr/bin/env python3
from questionnaire import questionnaire
from pprint import pprint
import json

######## 
# squence started by every new user/print
#############

# 1 - start questionnaire
articles_index = questionnaire()

# 2 - create a print-queue stored in latex/queue.json 
f = open('all_pages.json', 'r').read()
all_pages = json.loads(f)
print_queue = {  page: all_pages[page]  for page in articles_index } 
w = open('latex/queue.json','w')
json.dump( print_queue, w, indent=4)
print('print_queue contains:', len(print_queue), 'articles')

# 3 - produce the PDF

# 4 - print

