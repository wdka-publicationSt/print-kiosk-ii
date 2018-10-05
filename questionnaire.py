#!/usr/bin/env python3
from sys import stdin, stderr, stdout
import requests
import json
from datetime import datetime
from questions import questions
from colors import colors
from pprint import pprint
from search_wiki import search_request

print(questions)
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

current_match = [] # list of matching articles which will be added and filtered out to produce the final list of articles

# * * * * * * * * * * * * * * * * * * * * * * *
# Questions > Article index
# 
# * * * * * * * * * * * * * * * * * * * * * * *
# This is where we work with the questions from 
# the questionnaire, and process their answers.
#
# The list of pages is shrinking depending on 
# the answers that are given.



def check_first_edit(first_edit_hour):
        # default is 'no'
        # if article is written between 9-17 return 'yes'
	result = 'no'
	if first_edit_hour >= 9:
		if first_edit_hour <= 17:
			result = 'yes'
	return result

# questions, variables, tags = load_questions()
# # print(questions, tags)

# queue = {} # queue is the temporary storage object 

# start
print(colors.HEADER,
      'Please answer these questions with your general first impression response. Don\'t overthink it.',
      colors.ENDC,
      '\n')


for key in sorted(questions):
        q = questions[key]['question']
        options = questions[key]['variables']
        reply  = questions[key]['reply']
        error =  questions[key]['error']
        
        if 'time' in key:                
                print(colors.GREEN,
                      q,
                      colors.BLUE,                      
                      options,
                      colors.ENDC,
                      file=stderr)
                
                answer = stdin.readline().lower()
                
                if 'yes' in answer:
                        print('\n', 'Really? Me too!','\n', file=stderr)
                elif 'no' in answer:
                        print('\n', 'Oh yes me neither.','\n', file=stderr)                        
                else:
                        print('Hmm ...','\n')

                # populate the current_match by comparing the answer with the officehours
                for page, page_data in data.items(): 
                        first_edit_hour = data[page]['revisions']['first_revision_time'][3] # get the hour in which the first edit of a page is made                                
                        check = check_first_edit(first_edit_hour) # check if the first_edit_hour matches the officehours with the answer                        
                        if check in answer: # according to the answer and match
                                #print (check, answer)
                                current_match.append(page)
                                
                # print('\nThese pages are something for you:\n\n', current_match)
                print('\n> > > {} pages are added to your print queue ...\n'.format(len(current_match)))

#print( current_match )
        elif 'common-words' in key:                
                while True: # start a loop until (if)
                        print(colors.GREEN,
                              q,
                              colors.BLUE,                      
                              options,
                              colors.ENDC,
                              file=stderr)
                        answer = stdin.readline().lower()                
                        search_results = search_request(query=answer, namespace='0', reach='text')
                        if len(search_results) >= 20: # get minimum number of results 
                                print ( colors.BLUE,
                                        reply.format(pagenumber=len(search_results), term=answer )
                                )
                                break  # and break the while loop
                        else:   # continue loop
                                print (colors.FAIL,
                                       error.format(answer)
                                )
                                
                current_match = list( set(current_match).intersection(search_results)) 

                print( '\n> > > but in the print queue, only {} pages were found to contain the word {}\n'.format(len(current_match), answer ) )
                
                       
#                print ('serch_results', search_results)
                
                
        elif 'free-association' in key:                
                print(colors.GREEN,
                      q,
                      colors.BLUE,                      
                      options,
                      colors.ENDC,
                      file=stderr)

                
'''                

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
			match = check_first_edit(first_edit_hour)
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


'''
# pprint(queue)


# * * * * * * * * * * * * * * * * * * * * * * *
# queue > layout(s)
# 
# * * * * * * * * * * * * * * * * * * * * * * *
# Process the content into different print layout(s)
# laser, dot-matrix, receipt printer ......

# pprint(data)
# queue = data

