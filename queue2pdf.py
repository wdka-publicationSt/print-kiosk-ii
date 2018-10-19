#!/usr/bin/env python3
import json
import os, re
from pprint import pprint
from functions import remove_wiki_elements
import pypandoc
from bs4 import BeautifulSoup



# * * * * * * * * * * * * * * * * * *
# queue.json > queue.tmp.html
#

# --- load all contributors
def load_all_contributors(data):
	print(data)
	f = open(data, 'r').read()
	data = json.loads(f)
	all_pages_contributors = []
	for page, _ in data.items():
		page_contributors = data[page]['contributors']
		for contributor in  page_contributors:
			all_pages_contributors.append(contributor)
	all_pages_contributors = sorted(list(set(all_pages_contributors)))
	return all_pages_contributors


# --- load print queue
def load_print_queue(data):
	print(data)
	f = open(data, 'r').read()
	queue = json.loads(f)
	#pprint(queue)
	return queue


# --- Pre-process the content html
def text_replacements(html):
		soup = BeautifulSoup(html, "lxml")
		imgs = soup.find_all("img")
		for img in imgs:
			img['src'] = 'images/'+(img['src'].split('/'))[-1]
			print(img)
		html = remove_wiki_elements(html)
		html = re.sub(r'<span class="mw-editsection-bracket">\[</span>.*?edit.*?<span class="mw-editsection-bracket">]', '', html)
		html = html.replace('/wiki/images/', '/var/www/html/wiki/images/') # to load images locally
		html = re.sub(r'<table.*?</table>', '', html) # to remove tables from the print queue (unfortunately, \longtables give us the following error: "! Package longtable Error: longtable not in 1-column mode.")
		html = re.sub(r'width=".*?"', '', html) # to force images to template size - this is hacky, should perhaps be done with a html parser!
		html = re.sub(r'height=".*?"', '', html) # to force images to template size - this is hacky, should perhaps be done with a html parser!
		# to remove the TOC that is generated by the wiki
		html = html.replace('<div class="toc" id="toc"><div class="toctitle" id="toctitle"><h2>Contents</h2></div>','')
		html_out = []
		
	
		lines = html.split('\n')
		for line in lines:
				if 'toclevel' not in line:
						html_out.append(line)
		return '\n'.join(html_out)

def base_header_shift(content):
	content_shifted_headers = pypandoc.convert_text(content, 'html', format='html', extra_args=['--base-header-level=2'])
	return content_shifted_headers

# --- Place content html in template, add information to the article from the all_pages.json
def get_article_template(title, contributors, categories, content):
	content = text_replacements(content)
	content = base_header_shift(content)
	if len(categories) == 0:
		categories_string = '...'
	else:
		categories_string = ''
		for i, c in enumerate(categories):
			string = '<em>{}</em>'.format(c)
			if i == 0:
				categories_string = categories_string + string
			else:
				categories_string = categories_string + ' & ' + string

	template = '''<div class="article_wrapper">
		<h1 class="article_title">{}</h1>
		<div class="article_metadata">CONTRIBUTOR(s) {}</div>
		<hr>
		<div class="article_metadata">CATEGORIZED as {}</div>
		<hr>
		<div class="article_content">{}</div>
	</div>'''.format(title, ' & '.join(contributors), categories_string, content)
	return template

# --- Write metadata file
def create_metadata_authors_string(authors):
	''' authors = [] '''
	string = ''
	for author in authors:
		tmp = '- name: {}'.format(author)
		string = string +'\n'+ tmp
	return string
	# print(string)

def create_metadata_file(metadata_filename, authors):
	''' authors = [] '''
	''' categories = [] '''
	authors_string = create_metadata_authors_string(authors)
	metadata = '''---
title: PRINT KIOSK II
subtitle: a tech carnival experiment :)
author:
{}
abstract: PROMISCUOUS PRINT SERVICE? CHATTY PRINT SERVICE? Continuing the idea of what BS looks like in physical form, how does it become human, material, present in a space, able to engage with its community. Can the platform be made to speak? How can a digital platform give and be given a human voice? Three printers, serving three layers of information in the form of a personalized magazine. The content of the magazine is served to each visitor in three ways.
...'''.format(authors_string)
	out = open(metadata_filename, 'w+')
	out.write(metadata)
	out.close()
	print('*{} written*'.format(metadata_filename))

# --- write queue to html
def queue2html(queue, html_filename):
	queue_html = ''
	keywords = []
	for page, _ in queue.items():

		# collect content
		title = queue[page]['title']
		contributors = queue[page]['contributors']
		categories = queue[page]['categories']
		content = queue[page]['text']
		current_page_html = get_article_template(title, contributors, categories, content)
		queue_html = queue_html + current_page_html

	out = open(html_filename, 'w+')
	out.write(queue_html)
	out.close()
	print('*{} written*'.format(html_filename))


# * * * * * * * * * * * * * * * * * *
# queue.tmp.html > queue.pdf
#

# --- use pandoc to convert the html file into a pdf with the LaTeX engine
def html2pdf(html_tmp_filename, metadata_filename, pdf_filename):
	
	# pandoc variables
	# 
	# -V or --variable = insert variable
	# -N or --number-sections = Number section headings in LaTeX, ConTeXt, HTML, or EPUB output. By default, sections are not numbered. Sections with class unnumbered will never be numbered, even if --number-sections is specified.
	# --template=template.tex 
	# --number-offset=1 

	# latex variables
	# 
	# lof = list of figures
	# pagestyle=headings
	# logo=/path/to/image
	# fontsize=100 (doesn't work...)
	# documentclass=twocolumn, article, report, book, memoir

	cmd = '''pandoc -f html -t latex --pdf-engine pdflatex --template=latex.twocolumns.tex --title "PRINT KIOSK II" -N -V papersize=A4 -V geometry:margin=10mm -V version=2.0 -V thanks="Thank you!" -V toc-title=TOC! {} --metadata-file {} --toc -o {}'''.format(html_tmp_filename, metadata_filename, pdf_filename)
	os.system(cmd)
	print('*done! {} written*'.format(pdf_filename))

# --- main function, generate the pdf
def queue2pdf(data_json_file, queue_json_file, html_tmp_filename, metadata_filename, pdf_filename):

	# --- load queue data
	all_pages_contributors = load_all_contributors(data_json_file)
	queue = load_print_queue(queue_json_file)

	# --- queue2html
	queue2html(queue, html_tmp_filename)

	# --- metadata.yaml
	create_metadata_file(metadata_filename, all_pages_contributors)
	
	# --- html2pdf
	html2pdf(html_tmp_filename, metadata_filename, pdf_filename)

#queue2pdf('all_pages.json', 'queue.tmp.json', 'queue.tmp.html', 'metadata.yaml', 'queue.pdf')
