#!/usr/bin/env python3

import os
import csv

path = '../BS-Shadow-Library/'

# --- create BS Shadow Library index
def create_shadow_index():
	print('\n*Creating shadow_library.csv ...*')
	shadow_library = os.listdir(path)

	# print(shadow_library)

	csvfile = open('shadow_library.csv', 'w+')

	for i, pdf in enumerate(shadow_library):
		pdf_id = '{0:03}'.format(i)
		csvwriter = csv.writer(csvfile, delimiter='	', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csvwriter.writerow([pdf_id] + [pdf])

	csvfile.close()
	print('*shadow_library.csv is created*\n')


# --- make shadow_library.pdf
def grep_shadow_pdfs(selection_ids):
	outfile = 'shadow_library.pdf'

	# check if the shadow_library.csv file needs to be created
	if os.path.isfile('shadow_library.csv') == False: 
		create_shadow_index()

	index = open('shadow_library.csv', 'r').readlines()
	index = [item.replace('\n', '') for item in index]
	index = [item.split('\t') for item in index]
	# print(index)
	pdfs = []
	for selection_id in selection_ids:
		for item in index:
			pdf_id = item[0]
			pdf = item[1].replace(' ', '\\ ') # to work with spaces in files
			if selection_id == pdf_id:
				pdfs.append(path+pdf)
				print('PDF: *{}* selected!'.format(pdf))

	# if there is only 1 pdf in the selection
	if len(pdfs) == 1: 
		cmd = 'cp {} {}'.format(pdfs[0], outfile)
		print(cmd)
		os.system(cmd)
		print('\n*{}* is ready!\n'.format(outfile))
	# if there are more, they will be [pdf]united into 1 pdf
	else: 
		print('\n*Currently it\'s only possible to feed one PDF from the Shadow Library.*\n')
		# cmd = 'pdfunite {} {}'.format(' '.join(pdfs), outfile)
		# print(cmd)
		# os.system(cmd)
		# print('\n*{}* is [pdf]united!\n'.format(outfile))

def get_pdf_filename(selection_id):
	# check if the shadow_library.csv file needs to be created
	if os.path.isfile('shadow_library.csv') == False: 
		create_shadow_index()

	number = selection_id[0]
	index = open('shadow_library.csv', 'r').readlines()
	index = [item.replace('\n', '') for item in index]
	index = [item.split('\t') for item in index]
	# print(index)
	pdfs = []
	for item in index:
		pdf_id = item[0]
		pdf = item[1].replace(' ', '\\ ') # to work with spaces in files
		if number == pdf_id:
			return pdf.replace('\\ ', '')

if __name__ == '__main__':
	create_shadow_index()
	selection_ids = ['009']
	selection_ids = ['001', '002', '003']
	grep_shadow_pdfs(selection_ids)
