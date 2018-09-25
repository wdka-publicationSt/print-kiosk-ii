from sys import stdin, stderr, stdout
import requests
import json
from datetime import datetime

from pprint import pprint
from search_wiki import *

# * * * * * * * * * * * * * * * * * * * * * * *
# Load pages index
# 
# * * * * * * * * * * * * * * * * * * * * * * *
# Request a list of wiki pages from the BS wiki.

def load_mw_data():
	f = open('all_pages.json','r').read()
	data = json.loads(f)
	return data

data = load_mw_data()


# * * * * * * * * * * * * * * * * * * * * * * *
# Questions > Article index
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
	variables = [line.split('/')[1].replace(' ', '') for line in lines]
	tags = [line.split('/')[2].replace(' ', '').replace('\n', '') for line in lines]
	return questions, variables, tags

def process_first_edit(first_edit_hour):
	result = 'no'
	if first_edit_hour >= 9:
		if first_edit_hour <= 17:
			result = 'yes'
	return result

questions, variables, tags = load_questions()
# print(questions, tags)

queue = {} # queue is the temporary storage object 

# start
print('\nPlease answer these questions with your general first impression response. Don\'t overthink it.')

for i, question in enumerate(questions):
	tag = tags[i]
	var = variables[i]
	print('\n* * *\n') # aesthetic-line-break :)
	# print('tag:', tag)
	# print('var:', var)

	if tag == 'hours':

		tmp = {}

		# ----------------------------
		# Start: Are you most productive during normalized working day hours (9am-5pm)?

		print(question, file=stderr)
		answer = stdin.readline().lower()
		if 'yes' in answer:
			print('\nReally? Me too!', file=stderr)
		elif 'no' in answer:
			print('\nOh yes me neither.', file=stderr)
		else: 
			print('Hmm ...')

		matches = []
		no_matches = []

		for page, page_data in data.items():

			# get the hour in which the first edit of a page is made
			first_edit_hour = data[page]['revisions']['first_revision_time'][3]

			# check if the first_edit_hour matches with the answer 
			match = process_first_edit(first_edit_hour)
			print('\n*{}* is produced between 9am-5pm:'.format(page), match)

			if match in answer:
				matches.append(page)
				tmp[page] = data[page]
			else:
				no_matches.append(page)

		print('\nThese pages are something for you:\n\n', matches)
		print('\nThese pages don\'t suit your rhythm ...\n\n', no_matches)

		print('\n> > > {} pages are added to your print queue ...\n'.format(len(matches)))


		# ----------------------------
		# Then: In general, do you like reading long texts?

		print('\nIn general, do you like reading long texts?', file=stderr)
		answer = stdin.readline().lower()

		# for page, page_data in data.items():
			# word_count = data[page]['word_count']


	if tag == 'most-common-words':
		print(question, file=stderr)
		print('\nnot there yet!!')

	if tag == 'free-association':
		print(question, file=stderr)

		words = var.split(',')
		for word in words: 
			subquestion = 'When I say {}, you say: ___________'.format(word)
			print(subquestion, file=stderr)
			answer = stdin.readline()

			# search request
			query = answer
			namespace = 0

			# first we search in the title of the articles ... 
			reach = 'title'
			search_results = search_request(query, namespace, reach)

			# if that doesn't give resutls, we also query the content of the articles
			if search_results == []:
				reach = 'text'
				search_results = search_request(query, namespace, reach)
			
			print(search_results)
			print('\n> > > {} pages are added to your print queue ...\n'.format(len(search_results)))



# pprint(queue)


# * * * * * * * * * * * * * * * * * * * * * * *
# queue > layout(s)
# 
# * * * * * * * * * * * * * * * * * * * * * * *
# Process the content into different print layout(s)
# laser, dot-matrix, receipt printer ......

# pprint(data)
# queue = data