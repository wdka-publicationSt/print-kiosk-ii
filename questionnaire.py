#!/usr/bin/env python3
from sys import stdin, stderr, stdout
import requests
import json
from datetime import datetime
from questions import questions
from colors import colors
from pprint import pprint
from search_wiki import search_request
from random import shuffle
#print(questions)

# * * * * * * * * * * * * * * * * * * * * * * *
# Questions asked to the user generate the Articles' index
# 
# * * * * * * * * * * * * * * * * * * * * * * *
# This is where we work with the questions from  the *questions* dict, and ask the user to answer them
#
# The list of pages is shrinking depending on  the answers given to each question
# That is done in the main loop which cycles thought the *questions* dict
# and if conditions trigger the different processes for each question

# TODO: add to questions['03-free-association']['user_answers'] # perhaps as tuple

def load_mw_data(): # Load pages index
	f = open('all_pages.json','r').read()
	data = json.loads(f)
	return data

def check_first_edit(first_edit_hour):
        # default is 'no'
        # if article is written between 9-17 return 'yes'
	result = 'no'
	if first_edit_hour >= 9:
		if first_edit_hour <= 17:
			result = 'yes'
	return result

data = load_mw_data()

print(colors.HEADER,
      'Please answer these questions with your general first impression response. Don\'t overthink it.',
      colors.ENDC,
      '\n')

def questionnaire():
    articles_index = [] # list of matching articles; after articles are added in 'time' questions, they are filtered out inf following questions to produce the final list of articles
    
    for key in sorted(questions):
        q = questions[key]['question']
        options = questions[key]['variables']
        reply  = questions[key]['reply']
        error =  questions[key]['error']

        if 'time' in key:
                while True:
                    print(colors.GREEN,
                          q,
                          colors.BLUE,                      
                          options,
                          colors.ENDC,
                          file=stderr)
                    answer = stdin.readline().lower()
                    if 'yes' in answer:
                            print(colors.WARNING, '\n', 'Really? Me too!','\n', colors.ENDC, file=stderr)
                            break
                    elif 'no' in answer:
                            print(colors.WARNING, '\n' 'Oh yes me neither.','\n', colors.ENDC, file=stderr)
                            break
                    print(colors.FAIL, 'Hmm ..not quite sure about', colors.WARNING, answer, colors.FAIL,
                          '\n', 'Can you please answer yes or no?','\n',
                          colors.ENDC)

                # populate the articles_index by comparing the answer with the officehours
                for page, page_data in data.items(): 
                        first_edit_hour = data[page]['revisions']['first_revision_time'][3] #hour of first edit of page
                        check = check_first_edit(first_edit_hour) # first_edit_hour matches the officehours? yes or no
                        if check in answer: # yes(officehours) in yes(answer) or no(officehours) in no(answer)
                                articles_index.append(page)
                # print('\nThese pages are something for you:\n\n', articles_index)
                print(colors.BLUE,'\n> > > {} pages are added to your print queue ...\n'.format(len(articles_index)), colors.ENDC)

        elif 'common-words' in key:
                # the user is asked for a word *answer* that should be in BS curriculum
                # the *answer* is searched for with the API            
                while True:
                        # the while loop keeps asking for *answer* until a *search_results* has > N results in current_mach,
                        # in which case the loop breaks
                        # otherwise it continues asking the user for terms, searching, and comparing to articles_index
                        print(colors.GREEN,
                              q,
                              colors.BLUE,                      
                              options,
                              colors.ENDC,
                              file=stderr)
                        answer = stdin.readline().lower()                
                        search_results = search_request(query=answer, namespace='0', reach='text')
                        if  len(list( set(articles_index).intersection( search_results ) )) > 20: # if search_results in articles_index are > N                       
                                print ( colors.BLUE, reply.format(pagenumber=len(search_results), term=answer), colors.ENDC ) 
                                break  # and break the while loop
                        else:   # continue loop
                                print (colors.FAIL, error.format(answer), colors.ENDC)

                articles_index = list( set(articles_index).intersection(search_results)) 
                print(colors.BLUE, '\n> > > In the print queue, {} pages were found to contain the word {}\n'.format(len(articles_index), answer ),colors.ENDC )                
                # print ('serch_results', search_results)


        if 'free-association' in key:
                # free-association: should result in at least 10 articles
                # uses the shuffled questions['03-free-association']['options']
                # which are looped through
                # at each iteration of the loop one *subquestion* is asked
                # the *answer* is searched for using the API, returning results in *search*
                # an intersection of the *search* with the *articles_index* is performed resulting in 
                # the common articles to *search* & *articles_index* are added to *search_results_in_articles_index*
                # the loop break when more than 10 articles are in the *search_results_in_articles_index*

                user_terms = [] 
                search_results_in_articles_index = []
                print(colors.GREEN,
                      q,
                      file=stderr)
                shuffle(options)
                #print( options )
                for option in options:
                    subquestion = 'When I say {}, you say: ___________'.format(option)
                    print(colors.HEADER, subquestion, colors.ENDC, file=stderr)
                    answer = stdin.readline()
                    user_terms.append(answer.replace('\n', '')) # TODO add to questions dict                
                    search = search_request(query=answer, namespace=0, reach='text')
                    for i in  list( set(articles_index).intersection( search ) ):
                            if i not in search_results_in_articles_index:
                                    search_results_in_articles_index.append(i)

                    #print('search_results_in_articles_index:', search_results_in_articles_index )
                    #print('articles_index', len(articles_index), 'search:',len(search), 'intersection:', len(search_results_in_articles_index) )

                    if len(search_results_in_articles_index) > 10:
                            break
                if len(search_results_in_articles_index) > 15: # in case there is a selection of > 15 articles
                    shuffle(search_results_in_articles_index)
                    articles_index = search_results_in_articles_index[:14]
                else:
                    articles_index = search_results_in_articles_index
                print(colors.BLUE, '\n> > > In the print queue, {} pages were found to contain the words {}\n'.format(len(articles_index),(", ").join(user_terms) ) )
                print( colors.HEADER, '\n> > > The following articles will be printed:\n', colors.GREEN, (("\n").join(articles_index ) ), colors.ENDC )
    return articles_index

# QUESTIONNAIRE IS RUN BY run-questionnaire.py or print-sequence.py
# articles_index = questionnaire()
