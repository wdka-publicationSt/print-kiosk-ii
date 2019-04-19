#!/usr/bin/env python3

from sys import stdin, stderr, stdout
from pprint import pprint
import json, os, sys
from datetime import datetime
from time import sleep
from questionnaire import questionnaire
from queue2pdf import queue2pdf
import argparse
from receiptprintercmds import escpos, asciiart, stdout, stderr

#############
# squence started by every new user/print
#############

# 0 - presentions
print(escpos['init_printer'], file=stdout)
print(escpos['justify_center'], file=stdout)
greeting = open("ELAINE.txt", "r").read()
print(greeting, file=stdout)
print(asciiart['flames2'], file=stdout)
print(escpos['justify_left'], file=stdout)
sleep(3)

# 1 - start questionnaire
print('\n\n\n', 'Please hit [ENTER] to meet Elaine ...',
      '\n\n\n\n\n\n\n', file=stdout)
answer = stdin.readline().lower()
if answer == '\n':
    articles_index = questionnaire()

# 2 - create a print-queue stored in latex/queue.json
# from the *articles_index* generated from questionnaire() and all_pages.json
f = open('all_pages.json', 'r').read()
all_pages = json.loads(f)
# create dict from the *articles_index*
print_queue = {page: all_pages[page] for page in articles_index}
w = open('queue.tmp.json', 'w')
w.write(json.dumps(print_queue, indent=4))
w.close()
print('print_queue contains:', len(print_queue), 'articles')

# 3a - produce the PDF
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
if os.path.isdir('tmp') is False:
    os.mkdir('tmp')
pdf_filename = 'tmp/queue.{}.pdf'.format(timestamp)
# TODO: move next line to print-sequence
# print('Please be patient. I am working on producing your print out', asciiart['flames2'], file=stdout)
queue2pdf('all_pages.json', 'queue.tmp.json',
          'queue.tmp.html', 'latex.metadata.yaml', pdf_filename)
# trick to add a custom abstract (instead of an abstract through LaTeX):
# cmd = 'pdftk {} multibackground {} output {}'.format(
#               pdf_filename, 'abstract.pdf', pdf_filename)

# # 4 - prepare the Shadow Library PDF selection
from irc import irc
irc("bs_user")  # start the IRC chat
# irc module listens to #shadowlibrary key to collect PDF(s) from Shadow Library.
# The PDF's can be inserted by using the id numbers from the shadow_library.csv file

# # 5 - resize pdf
shadow_library_pdf = 'shadow_library.pdf'
shadow_library_pdf_a4 = 'shadow_library_A4.pdf'
# resize pdf to A4:
cmd_resize_SL = "pdfjam --outfile {} --paper a4paper {}".format(
                shadow_library_pdf_a4, shadow_library_pdf)
os.system(cmd_resize_SL)

# # 6 Print squence
# P1 - print questionnaire PDF
cmd = "lp -d HP_LaserJet_500_colorMFP_M570dn -o media=a4 {pdf}".format(
    pdf=pdf_filename)
print(cmd)
os.system(cmd)
print('First PDF (questionnaire selection) is printing ...')

# # # P2 - print shadow library PDF
cmd = "lp -d HP_LaserJet_500_colorMFP_M570dn -o media=a4 {pdf}".format(
    pdf=shadow_library_pdf_a4)
print(cmd)
os.system(cmd)
print('Second PDF (shadow_library) is printing ...')

print('ps. .... I will add an ANNEX for you as well, to leak some information from the making process. Hope you will enjoy it!',
      asciiart['flames2'], file=stdout)

# # # P3 - print annex PDF
annex_pdf = 'annex.pdf'
cmd = "lp -d HP_LaserJet_500_colorMFP_M570dn -o media=a4 {pdf}".format(
    pdf=annex_pdf)
print(cmd)
os.system(cmd)
print('Third PDF (annex) is printing ... (Last one!)')

# # 7 receipt printer: cut
# #receipt printer
# title = open("ELAINE.txt","r").read()
# printer.text( title )
# printer.text("\n\n")
# #    printer.text(articles_index)
# printer.cut()
sleep(3)
print(escpos['papercut'], file=stdout)  # move to print-sequence
