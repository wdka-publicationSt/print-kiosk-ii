#!/usr/bin/env python3

import re
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

	html = str(soup.body)
	return html
