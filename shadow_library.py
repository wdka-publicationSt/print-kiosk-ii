#!/usr/bin/env python3

import os
import csv

path = '../BS-Shadow-Library/'


# --- create BS Shadow Library index
def create_shadow_index():
	shadow_library = os.listdir(path)

	print(shadow_library)

	csvfile = open('shadow_library.csv', 'w+')

	for i, pdf in enumerate(shadow_library):
		pdf_id = '{0:03}'.format(i)
		csvwriter = csv.writer(csvfile, delimiter='	', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csvwriter.writerow([pdf_id] + [pdf])

	csvfile.close()
	print('*shadow_library.csv is created*')

# create_shadow_index()


# --- make shadow_library.pdf
def grep_shadow_pdfs(selection_ids):
	outfile = 'shadow_library.pdf'

	# check if the shadow_library.csv file needs to be created
	if os.path.isfile(outfile) == False: 
		create_shadow_index()

	index = open('shadow_library.csv', 'r').readlines()
	index = [item.replace('\n', '') for item in index]
	index = [item.split('\t') for item in index]
	print(index)
	pdfs = []
	for selection_id in selection_ids:
		for item in index:
			pdf_id = item[0]
			pdf = item[1].replace(' ', '\ ') # to work with spaces in files
			if selection_id == pdf_id:
				pdfs.append(path+pdf)
				print('PDF: *{}* selected!'.format(pdf))

	# if there is only 1 pdf in the selection
	if len(pdfs) == 1: 
		cmd = 'cp {} {}'.format(pdfs[0], outfile)
		print(cmd)
		os.system(cmd)
		print('*{}* is ready!'.format(outfile))
	# if there are more, they will be [pdf]united into 1 pdf
	else: 
		cmd = 'pdfunite {} {}'.format(' '.join(pdfs), outfile)
		print(cmd)
		os.system(cmd)
		print('*{}* is [pdf]united!'.format(outfile))

# selection_ids = ['001']
# selection_ids = ['001', '002', '003']
# grep_shadow_pdfs(selection_ids)
