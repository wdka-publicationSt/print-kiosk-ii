import json
from pprint import pprint

from nltk import FreqDist
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+') # initialize tokenizer

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
# adding dutch stopwords
for word in set(stopwords.words('dutch')):
	stop_words.add(word)

f = open('all_pages.json', 'r').read()
d = json.loads(f)
pprint(d)

alltexts = []

for title, data in d.items():
	alltexts.append(data['text'])
# print('\nall texts =', alltexts)

alltexts_plain = ' '.join(alltexts)
words = tokenizer.tokenize(alltexts_plain)
# print('\nwords =', words)

unique_words = set(words)
print('\nunique_words', unique_words)

words_no_stopwords = [word.lower() for word in words if word.lower() not in stop_words]

freqdist = FreqDist(words_no_stopwords)
most_common = freqdist.most_common(50)
# print('\nfreqdist', freqdist.most_common(50))
print('')
for item in most_common:
	word = item[0]
	count = item[1]
	print(word, count)


#  *************

## Another way to do this (doesn't work yet, but would be nice to explore further)
# import nltk.corpus
# from nltk.text import Text, TextCollection
# txt = Text(f)
# print('\ntext:', txt)
# print('\ntext.vocab():', txt.vocab())
# print('\nTextCollection:', TextCollection([txt]))
