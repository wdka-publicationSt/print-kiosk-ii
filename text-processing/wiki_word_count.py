import json
from pprint import pprint

from bs4 import BeautifulSoup

from nltk import FreqDist
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+') # initialize tokenizer

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
# adding dutch stopwords
for word in set(stopwords.words('dutch')):
	stop_words.add(word)

f = open('all_pages.json', 'r').read()
data = json.loads(f)
# pprint(data)

alltexts_words = []
lengths = []

def parse_html(html):
	soup = BeautifulSoup(html, "lxml")

	# remove the contribute banner + recent articles suggestions banner
	contribute = soup.find(id='contribute-wrapper')
	if contribute != None:
		contribute.clear()
	toc = soup.find(id='toc')
	if toc != None:
		toc.clear()
	suggestions = soup.find_all('div', class_='oneline-wrapper')
	if len(suggestions) > 0:
		suggestions[0].clear()

	plain = soup.text

	stopwords = ['edit']
	for word in stopwords:
		plain = plain.replace(' '+word+' ', '')

	return plain

def tokenize(text):
	words = tokenizer.tokenize(plain_text)
	return words

def count_article_length(text):
	words = tokenize(text)
	length = len(words)
	return length

for page, _ in data.items():

	# --- collected content of the article in plain text ---
	html = data[page]['text']
	plain_text = parse_html(html)

	# --- append a list of words to alltext ---
	words = tokenize(plain_text)
	alltexts_words.extend(words)

	# --- count length of article ---
	length = count_article_length(plain_text)
	lengths.append(length)

# print('\nall texts =', alltexts)

# --- save alltext_plain to txt file to inspect the content ---
alltexts_plain = ' '.join(alltexts_words)
tmp = open('wiki_word_count-alltext.txt','w+')
tmp.write(alltexts_plain)

# --- start word count ---
unique_words = set(alltexts_words)
words_no_stopwords = [word.lower() for word in alltexts_words if word.lower() not in stop_words]
freqdist = FreqDist(words_no_stopwords)

# --- select most common words ---
most_common = freqdist.most_common(50)
# print('\nfreqdist', freqdist.most_common(50))
print('')
for item in most_common:
	word = item[0]
	count = item[1]
	print(word, count)

least_common = freqdist.most_common()[50:]
for item in least_common:
	word = item[0]
	count = item[1]
	print(word, count)

# --- process information about article length ---
print('\nlength of articles = ', lengths)

number_of_articles = len(lengths)
print('number_of_articles = ', number_of_articles)

total_number_of_words = 0
for length in lengths:
	total_number_of_words += length 
print('total_number_of_words of all articles = ', total_number_of_words)

average_length = total_number_of_words / number_of_articles
print('average_length = ', average_length)

#  *************

## Another way to do this (doesn't work yet, but would be nice to explore further)
# import nltk.corpus
# from nltk.text import Text, TextCollection
# txt = Text(f)
# print('\ntext:', txt)
# print('\ntext.vocab():', txt.vocab())
# print('\nTextCollection:', TextCollection([txt]))
