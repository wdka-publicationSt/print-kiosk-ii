#!/usr/bin/env python3
from questionnaire import questionnaire
from pprint import pprint
import json, os
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
if os.path.isdir('tmp') is False:
    os.mkdir('tmp')
pdf_filename = 'tmp/queue.{}.pdf'.format(timestamp)
queue2pdf('all_pages.json', 'queue.tmp.json', 'queue.tmp.html', 'latex.metadata.yaml', pdf_filename)

# # 4 - add the Shadow Library PDF selection 
# from irc import irc
# irc("bs_user") #start the IRC chat, the script listens to the #shadowlibrary key to collect PDF(s) from the BS Shadow Library. The PDF's can be inserted by using the id numbers from the shadow_library.csv file.
# cmd = 'pdfunite {} {} output/print.queue.{}.pdf'.format(pdf_filename, 'shadow_library.pdf', timestamp) # unite the questionnaire PDF with the shadow_library PDF
# print(cmd)
# os.system(cmd)

# 5 - add Rümneysa's work, the glossary

# See the pad for notes that i wrote for Rümeysa. These are suggestions about the place where she can leave her definitions.
# How can we include these pages or descriptions in the print queue ..... ?
# Perhaps we better do this manually?

# 6 - print

