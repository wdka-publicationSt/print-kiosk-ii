#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+') # initialize tokenizer
from yaml import load, Loader, Dumper
from utility_scripts.wiki_word_count import parse_html

def remove_wiki_elements(soup):
	"""
		Removing the contribute banner + recent articles suggestions banner from all the pages.
	"""	
	# Remove contribute banner
	contribute = soup.find(id='contribute-wrapper')
	if contribute != None:
		contribute.clear()
	# Remove suggestions banner
	suggestions = soup.find_all('div', class_='oneline-wrapper')
	if len(suggestions) > 0:
		suggestions[0].clear()

	html = str(soup.body)
	return html
	
def tokenize(plain):
	"""
		Splitting plain text up into a list of words.
	"""
	words = tokenizer.tokenize(plain)
	return words

def count_article_length(html):
	plain = parse_html(html)
	words = tokenize(plain)
	length = len(words)
	print('length of this article: ', length)
	return length

def get_yaml_data(filename):
    yaml_f = open(filename, "r").read()
    data = load(yaml_f, Loader=Loader)
    metadata = {}
    metadata['title'] = data['title']
    metadata['subtitle'] = data['subtitle']
    metadata['abstract'] = data['abstract']
    authors = []
    for entry in data['author']:
        authors.append( entry['name'] )
    metadata['authors']=authors
    return metadata

