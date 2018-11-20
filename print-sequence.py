#!/usr/bin/env python3

from sys import stdin, stderr, stdout
from pprint import pprint
import json, os, sys
from datetime import datetime
from time import sleep
from queue2pdf import queue2pdf
# from printerreceipt import printer
import argparse
from receiptprintercmds import escpos, stdout, stderr

######## 
# squence started by every new user/print
#############

# 0 - presentions
print(escpos['init_printer'], file=stdout)
print(escpos['justify_center'], file=stdout)
greeting = open("ELAINE.txt","r").read()
print(greeting, file=stdout)
print("\n\n\n\n\n\n", file=stdout)
print(escpos['justify_left'], file=stdout)
sleep(3)

# 1 - start questionnaire
from questionnaire import questionnaire 
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
print('Please be patient. I am working on prodcuing your print out','\n\n' , file=stdout) # move to print-sequence 

queue2pdf('all_pages.json', 'queue.tmp.json', 'queue.tmp.html', 'latex.metadata.yaml', pdf_filename)
cmd = "lp -d HP_LaserJet_500_colorMFP_M570dn -o media=a4 {pdf}".format(pdf=pdf_filename)
print(cmd)
os.system(cmd)
print('First PDF (questionnaire selection) is printing ...')

# 4 - prepare the Shadow Library PDF selection 
from irc import irc
irc("bs_user") #start the IRC chat, the script listens to the #shadowlibrary key to collect PDF(s) from the BS Shadow Library. The PDF's can be inserted by using the id numbers from the shadow_library.csv file.

# 5 - unite shadow_library.pdf + annex.pdf && print this pdf
annex_pdf = 'annex.pdf'
shadow_library_pdf = 'shadow_library.pdf'
printstack_pdf = 'output/print-stack.{}.pdf'.format(timestamp)
if os.path.isdir('output') is False:
    os.mkdir('output')
# cmd = 'pdfunite {} {} {}'.format(shadow_library_pdf, annex_pdf, printstack_pdf) # shadow_library.pdf + annex.pdf
cmd = 'pdftk {} {} output {}'.format(shadow_library_pdf, annex_pdf, printstack_pdf) # shadow_library.pdf + annex.pdf
print(cmd)
os.system(cmd)
cmd = 'gs -o {} -sDEVICE=pdfwrite -sPAPERSIZE=a4 -dFIXEDMEDIA -dPDFFitPage -dCompatibilityLevel=1.4 {}'.format(printstack_pdf, printstack_pdf) # to resize to A4
print(cmd)
os.system(cmd)
print('*shadow_library.pdf + annex.pdf united*')

print('Your PDF will be printed soon. Thank you!', '\n\n\n', file=stdout) # move to print-sequence 
sleep(1)
print('ps. .... I added an ANNEX as well, to leak some information from the making process. Hope you will enjoy it!', '\n\n\n\n\n\n', file=stdout)
cmd = "lp -d HP_LaserJet_500_colorMFP_M570dn -o media=a4 {pdf}".format(pdf=printstack_pdf)
print(cmd)
os.system(cmd)
print('Second PDF (shadow_library + annex) is printing ...')
#if args.noreceipt is False:

# #receipt printer
# title = open("ELAINE.txt","r").read()
# printer.text( title )
# printer.text("\n\n")
# #    printer.text(articles_index)
# printer.cut()
print(escpos['papercut'], file=stdout) # move to print-sequence 
