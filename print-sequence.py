#!/usr/bin/env python3
from questionnaire import questionnaire
from pprint import pprint
import json
from datetime import datetime
from queue2pdf import queue2pdf

######## 
# squence started by every new user/print
#############

# 1 - start questionnaire
articles_index = questionnaire()

# 2 - create a print-queue stored in latex/queue.json from the *articles_index* generated from questionnaire() and all_pages.json
f = open('all_pages.json', 'r').read()
all_pages = json.loads(f)
print_queue = { page: all_pages[page] for page in articles_index } # create dict from the *articles_index*
w = open('queue.tmp.json','w')
w.write(json.dumps(print_queue, indent=4))
w.close()
print('print_queue contains:', len(print_queue), 'articles')

# 3 - produce the PDF

timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
pdf_filename = 'output/queue.{}.pdf'.format(timestamp)
queue2pdf('all_pages.json', 'queue.tmp.json', 'queue.tmp.html', 'latex.metadata.yaml', pdf_filename)

# 4 - print

