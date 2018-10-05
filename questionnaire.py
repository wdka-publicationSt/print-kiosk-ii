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

        
        if 'free-association' in key:
                while True:
                    user_terms = []
                    search_results = []
                    print(colors.GREEN,
                          q,
                          file=stderr)                
                    for word in options:
                            subquestion = 'When I say {}, you say: ___________'.format(word)
                            print(subquestion, file=stderr)
                            answer = stdin.readline()
                            user_terms.append(answer.replace('\n', ''))
                            
                    for term in user_terms:
                            for article in  search_request(query=term, namespace=0, reach='text'):
                                    search_results.append(article )
                                    
                    if len(search_results ) > 10:
                    
                            print ( colors.BLUE,
                                    reply.format(pagenumber=len(search_results), terms=((" ").join(user_terms)) )
                            )
                            break   
                    else:
                            print (colors.FAIL,
                                   error.format(answer)
                           )

                current_match = list( set(current_match).intersection( search_results ) ) 
                print( '\n> > > but in the print queue, only {} pages were found to contain the words {}\n'.format(len(current_match), (", ").join(user_terms)  ) )


# TODO: IF THERE ARE NOT ENOUGHT ENTRIES IN THE CURRENT MATCH INCLUDE A QUESTION THAT SUPPLEMENTS MORE ENTRIES.


