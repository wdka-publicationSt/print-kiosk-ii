#!/usr/bin/env python3

from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+') # initialize tokenizer

def parse_html(html):
	soup = BeautifulSoup(html, "lxml")

	# remove the contribute banner + recent articles suggestions banner
	contribute = soup.find(id='contribute-wrapper')
	if contribute != None:
		contribute.clear()
	suggestions = soup.find_all('div', class_='oneline-wrapper')
	if len(suggestions) > 0:
		suggestions[0].clear()

	plain = soup.text
	return plain

def tokenize(plain):
	words = tokenizer.tokenize(plain)
	return words

def count_article_length(html):
	plain = parse_html(html)
	words = tokenize(plain)
	length = len(words)
	print('length of this article: ', length)
	return length