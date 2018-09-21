from sys import stdin, stderr, stdout
import requests
import json
from datetime import datetime

import pprint
pp = pprint.PrettyPrinter(indent=4)


# * * * * * * * * * * * * * * * * * * * * * * *
# Load pages index
# 
# * * * * * * * * * * * * * * * * * * * * * * *
# Request a list of wiki pages from the BS wiki.

def load_mw_data():
	f = open('mwdata.example.json','r').read()
	data = json.loads(f)
	return data

data = load_mw_data()


# * * * * * * * * * * * * * * * * * * * * * * *
# Type 1 - Questions > Article index
# 
# * * * * * * * * * * * * * * * * * * * * * * *
# This is where we work with the questions from 
# the questionnaire, and process their answers.
#
# The list of pages is shrinking depending on 
# the answers that are given.

def load_questions():
	lines = open('./questions.txt', 'r').readlines()
	questions = [line.split('/')[0] for line in lines]
	tags = [line.split('/')[1].replace(' ', '').replace('\n', '') for line in lines]
	return questions, tags

def process_timestamp(tm_hour):
	if tm_hour < 12:
		return 'morning'
	elif tm_hour > 18:
		return 'evening'
	else:
		return 'daytime'

questions, tags = load_questions()
# print(questions, tags)

tmp = data # tmp is the temporary storage object

for i, question in enumerate(questions):
	tag = tags[i]
	print('\n* * *\n') # aesthetic-line-break :)
	print(question, file=stderr)
	answer = stdin.readline()

	if tag == 'morning':
		if 'morning' in answer:
			print('\nReally? I\'m a morning person too!', file=stderr)
		else:
			print('\nOh no! I\'m an evening person too!', file=stderr)

		for page, page_data in data['articles'].items():

			# get first edit of a page
			api_first_edit = 'http://beyond-social.org/wiki/api.php?format=json&action=query&titles={}&prop=revisions&rvprop=timestamp%7Cuser%7Cids&rvdir=newer&rvlimit=1'.format(page)
			response = requests.get(api_first_edit)
			response = response.json()
			# pp.pprint(response)

			# get timestamp of this article
			for _, data in response['query']['pages'].items():
				tm_hour = 11
				timestamp = tm_hour

			# check if the timestamp matches with the answer of the user
			time_of_the_day = process_timestamp(timestamp)
			print('\nTime of the day of this page:', time_of_the_day)

			if time_of_the_day in answer:
				print('\nThis page is for you:', page)
			else:
				print('\nThis page doesn\'t suit your rhythm ...')
				del tmp[page]

	if tag == ''

pp.pprint(tmp)


# * * * * * * * * * * * * * * * * * * * * * * *
# Type 2 - Topics/interests
# 
# * * * * * * * * * * * * * * * * * * * * * * *
# Search API processing


# nothing yet


# * * * * * * * * * * * * * * * * * * * * * * *
# Article index > API content gathering
# 
# * * * * * * * * * * * * * * * * * * * * * * *
# Based on the article index, we now will use
# the wiki API to request content. 
# 
# Next to the page content, we will also request
# specific kinds of metadata, which we will use
# later on in the print layout(s).

# the final article index after having finished the questions
article_index = tmp
article_api_gathering = {}

def get_page_content(page):
	'''api request for the content of a page'''
	content = 'This is example content.'
	return content

for page, page_data in data['articles'].items():
	article_api_gathering[page] = page_data
	article_api_gathering[page]['content'] = get_page_content(page)
	article_api_gathering[page]['extra-api-content-type'] = 'Example'


# * * * * * * * * * * * * * * * * * * * * * * *
# article_api_gathering > layout(s)
# 
# * * * * * * * * * * * * * * * * * * * * * * *
# Process the content into different print layout(s)
# laser, dot-matrix, receipt printer ......

