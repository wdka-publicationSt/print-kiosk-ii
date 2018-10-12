#!/usr/bin/env python3
import json
import re
from pprint import pprint
from functions import parse_html

# * * * * * * * * * * * * * * * * * *
# queue.json > queue.tmp.html
#

# --- load print queue

f = open('queue.json', 'r').read()
queue = json.loads(f)
# pprint(queue)


# --- Write all pages' content to one html file

def text_replacements(html):
	html = parse_html(html)
	html = re.sub(r'<span class="mw-editsection-bracket">\[</span>.*?edit.*?<span class="mw-editsection-bracket">]', '', html)
	html = html.replace('/wiki/images/', '/var/www/html/wiki/images.bak/') # to load images locally
	html = re.sub(r'width=".*?"', '', html) # to force images to template size - this is hacky, should perhaps be done with a html parser!
	html = re.sub(r'height=".*?"', '', html) # to force images to template size - this is hacky, should perhaps be done with a html parser!
	return html

def get_article_template(title, contributors, content):
	content = text_replacements(content)
	template = '''<div class="article_wrapper">
		<h1 class="article_title">{}</h1>
		<div class="article_authors">{}</div>
		<div class="article_content">{}</div>
	</div>'''.format(title, ', '.join(contributors), content)
	return template

queue_html = ''
all_contributors = []
for page, _ in queue.items():

	title = queue[page]['title']
	contributors = queue[page]['contributors']
	for contributor in contributors:
		all_contributors.append(contributor)
	content = queue[page]['text']
	current_page_html = get_article_template(title, contributors, content)

	queue_html = queue_html + current_page_html

out = open('queue.tmp.html', 'w+')
out.write(queue_html)
out.close()
print('*queue.tmp.html written*')


# --- Write metadata file

def create_metadata_authors_string(authors):
	''' authors = [] '''
	string = ''
	for author in authors:
		tmp = '- name: {}'.format(author)
		string = string +'\n'+ tmp
	return string
	print(string)

def create_metadata_file(authors, keywords):
	''' authors = [] '''
	''' keywords = [] '''
	authors_string = create_metadata_authors_string(authors)
	metadata = '''---
title: PRINT KIOSK II
subtitle: a tech carnival experiment :)
author:
{}
keywords: {}
abstract: PROMISCUOUS PRINT SERVICE? CHATTY PRINT SERVICE? Continuing the idea of what BS looks like in physical form, how does it become human, material, present in a space, able to engage with its community. Can the platform be made to speak? How can a digital platform give and be given a human voice? Three printers, serving three layers of information in the form of a personalized magazine. The content of the magazine is served to each visitor in three ways.
...'''.format(authors_string, str(keywords))
	out = open('metadata.yaml', 'w+')
	out.write(metadata)
	out.close()
	print('*metadata.yaml written*')

keywords = []
for page, _ in queue.items():
	first_editor = queue[page]['revisions']['recent_revision_user']
	categories = queue[page]['categories']
	for category in categories:
		keywords.append(category)
create_metadata_file(all_contributors, keywords)


# * * * * * * * * * * * * * * * * * *
# queue.tmp.html > queue.pdf
#

import os

def html2pdf(html, pdf):
	
	# pandoc
	# 
	# -V or --variable = insert variable
	# -N or --number-sections = Number section headings in LaTeX, ConTeXt, HTML, or EPUB output. By default, sections are not numbered. Sections with class unnumbered will never be numbered, even if --number-sections is specified.
	# --template=template.tex 


	# latex variables
	# 
	# lof = list of figures
	# pagestyle=headings
	# logo=/path/to/image
	# fontsize=100 (doesn't work...)
	# documentclass=twocolumn, article, report, book, memoir

	cmd = '''pandoc -f html -t latex --pdf-engine pdflatex --template=twocolumns.tex --title "PRINT KIOSK II" -N -V papersize=A4 -V geometry:margin=10mm -V version=2.0 -V thanks="Thank you!" -V toc-title=TOC! {} --metadata-file {} --toc -o {}'''.format(html, 'metadata.yaml', pdf)
	os.system(cmd)

html = 'queue.tmp.html'
pdf = 'queue.pdf'
html2pdf(html, pdf)
print('*done! queue.pdf written*')