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
from irc import irc


#############
# squence started by every new user/print
#############

print(escpos['init_printer'], file=stdout)
print(escpos['justify_center'], file=stdout)
greeting = open("ELAINE.txt", "r").read()
print(greeting, file=stdout)
print(asciiart['flames2'], file=stdout)
print(escpos['justify_left'], file=stdout)
sleep(3)


# * * * * * * * * *
# START SCENE 1
# 
# Elaine as chat bot
# * * * * * * * * *

"""
	Start Elaine. Start the questionnaire.
	The questionnaire script stores the print queue as a list.
"""
print('\n\n\n', 'Please hit [ENTER] to meet Elaine ...',
      '\n\n\n\n\n\n\n', file=stdout)
answer = stdin.readline().lower()
if answer == '\n':
    print_queue = questionnaire() # list with article names, eg.: ['article1', 'article2', 'article3']

"""
	Processing the print queue, saving it to a .json file, 
	and counting the current number of articles in the queue.
"""
f = open('all_pages.json', 'r').read()
all_pages = json.loads(f)
print_queue_dict = {page: all_pages[page] for page in print_queue}
w = open('queue.tmp.json', 'w') # saving print queue to tmp file
w.write(json.dumps(print_queue_dict, indent=4))
w.close()
print('print_queue contains:', len(print_queue_dict), 'articles')

"""
	Converting the print queue to one PDF.
	The queue2pdf script first collects all the articles in a html file called queue.tmp.html.
	It then turns this html file into a PDF, using LaTEX templates and Pandoc to convert.
	The print queue is saved as queue.pdf.
"""
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
if os.path.isdir('tmp') is False:
    os.mkdir('tmp')
questionnaire_pdf = 'tmp/queue.{}.pdf'.format(timestamp)
# @TODO: add next line to print-sequence:
# print('Please be patient. I am working on producing your print out', asciiart['flames2'], file=stdout)
queue2pdf('all_pages.json', 'queue.tmp.json',
          'queue.tmp.html', 'latex.metadata.yaml', questionnaire_pdf)
# @TODO: trick to add a custom abstract (instead of an abstract through LaTeX):
# cmd = 'pdftk {} multibackground {} output {}'.format(
#               questionnaire_pdf, 'abstract.pdf', questionnaire_pdf)

"""
	Print the questionnaire PDF on the laser printer.
"""
cmd = "lp -d HP_LaserJet_500_colorMFP_M570dn -o media=a4 {pdf}".format(pdf=questionnaire_pdf)
print(cmd)
os.system(cmd)
print('First PDF (questionnaire selection) is printing ...')


# * * * * * * * * *
# START SCENE 2
# 
# Elaine as Shadow Library librarian
# * * * * * * * * *

"""
	Start the IRC session with the Shadow Library librarian.
"""
irc("bs_user")  # start the IRC chat
# irc module listens to #shadowlibrary key to collect PDF(s) from Shadow Library.
# A PDF can be selected by using the id number from the shadow_library.csv file.
# For example: #shadowlibrary 7

"""
	Resize the selected PDF to A4. 
"""
shadow_library_pdf = 'shadow_library.pdf'
shadow_library_pdf_a4 = 'shadow_library_A4.pdf'
cmd_resize_SL = "pdfjam --outfile {} --paper a4paper {}".format(
	shadow_library_pdf_a4, shadow_library_pdf)
os.system(cmd_resize_SL)

"""
	Print Shadow Library PDF.
"""
cmd = "lp -d HP_LaserJet_500_colorMFP_M570dn -o media=a4 {pdf}".format(
    pdf=shadow_library_pdf_a4)
print(cmd)
os.system(cmd)
print('Second PDF (shadow_library) is printing ...')

"""
	Print ANNEX.
"""
print('ps. .... I will add an ANNEX for you as well, to leak some information from the making process. Hope you will enjoy it!',
      asciiart['flames2'], file=stdout)
annex_pdf = 'annex.pdf'
cmd = "lp -d HP_LaserJet_500_colorMFP_M570dn -o media=a4 {pdf}".format(
    pdf=annex_pdf)
print(cmd)
os.system(cmd)
print('Third PDF (annex) is printing ... (Last one!)')


"""
	The end. EOF. EOConversation.
"""
sleep(3)
print(escpos['papercut'], file=stdout)  # move to print-sequence
