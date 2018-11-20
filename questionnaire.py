#!/usr/bin/env python3
from sys import stdin, stderr, stdout
#import requests
import json
from datetime import datetime
from questions import questions
from colors import colors
from pprint import pprint
from search_wiki import search_request
from random import shuffle
from receiptprintercmds import escpos, stdout, stderr

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

print('Please answer these questions with your general first impression response. Don\'t overthink it.',
      '\n\n\n', file=stdout)

def questionnaire():
    articles_index = [] # list of matching articles; after articles are added in 'time' questions, they are filtered out inf following questions to produce the final list of articles

    for key in sorted(questions):
        q = questions[key]['question']
        options = questions[key]['variables']
        reply  = questions[key]['reply']
        error =  questions[key]['error']

        if 'time' in key:
            while True:
                print(q,
                      '\n\n\n',
                      options,
                      '\n\n\n\n\n\n\n\n\n\n',
                      file=stdout)
                answer = stdin.readline().lower()
                print(escpos['justify_center'],answer,'\n\n\n\n', file=stdout)
                print(escpos['justify_left'], file=stdout)
                if 'yes' in answer:
                    print( 'Carpe diem!', '\n\n\n\n\n', file=stdout)
                    break
                elif 'no' in answer:
                    print('Me neither.', '\n\n\n\n\n', file=stdout)
                    break
                print('Hmm ..not quite sure about', answer, 
                      '\n\n', 'Can you please answer yes or no?','\n\n\n\n\n', file=stdout)

            # populate the articles_index by comparing the answer with the officehours
            for page, page_data in data.items(): 
                    first_edit_hour = data[page]['revisions']['first_revision_time'][3] #hour of first edit of page
                    check = check_first_edit(first_edit_hour) # first_edit_hour matches the officehours? yes or no
                    if check in answer: # yes(officehours) in yes(answer) or no(officehours) in no(answer)
                            articles_index.append(page)
            # print('\n\n\nThese pages are something for you:\n\n\n\n\n\n\n', articles_index)
            #print(colors.BLUE,'\n\n\n> > > {} pages are added to your print queue ...\n\n\n'.format(len(articles_index)), colors.ENDC)

        elif 'common-words' in key:
            n = -1
            # the user is asked for a word *answer* that should be in BS curriculum
            # the *answer* is searched for with the API            
            while True:
                n=n+1
                # the while loop keeps asking for *answer* until a *search_results* has > N results in current_mach,
                # in which case the loop breaks
                # otherwise it continues asking the user for terms, searching, and comparing to articles_index
                print(q,
                       '\n\n\n\n\n\n\n\n\n\n',
                      file=stdout)
                answer = stdin.readline().lower()
                print(escpos['justify_center'], answer,'\n\n\n\n', file=stdout)
                print(escpos['justify_left'], file=stdout)                
                search_results = search_request(query=answer, namespace='0', reach='text')
                if len(list( set(articles_index).intersection( search_results ) )) > 20: # if search_results in articles_index are > N                       
                    print ( reply, "\n\n\n", file=stdout ) 
                    break  # and break the while loop # MOVE TO F5
                else:   # continue loop
                    print ( error[n], "\n\n\n", file=stdout)
                    if n == 2:
                        break # break while loop after 3rd attempt # MOVE TO F3 (to do)
                    

            articles_index = list( set(articles_index).intersection(search_results)) 
#            print(colors.BLUE, '\n\n\n> > > In the print queue, {} pages were found to contain the word {}\n\n\n'.format(len(articles_index), answer ),colors.ENDC )                
            # print ('serch_results', search_results)


        elif 'free-association' in key:
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
            print(q,
                  "\n\n\n\n\n",
                  file=stdout)
            shuffle(options)
            #print( options )
            for option in options:
                subquestion = 'When I say {}, you say: ___________'.format(option)
                print(subquestion, '\n\n\n\n\n\n\n\n\n', file=stdout)
                answer = stdin.readline()
                print(escpos['justify_center'],answer,'\n\n\n\n', file=stdout)
                print(escpos['justify_left'], file=stdout)
                user_terms.append(answer.replace('\n', '')) # TODO add to questions dict                
                search = search_request(query=answer, namespace=0, reach='text')
                for i in  list( set(articles_index).intersection( search ) ):
                    if i not in search_results_in_articles_index:
                            search_results_in_articles_index.append(i)

                #print('search_results_in_articles_index:', search_results_in_articles_index )
                #print('articles_index', len(articles_index), 'search:',len(search), 'intersection:', len(search_results_in_articles_index) )

                if len(search_results_in_articles_index) > 10:
                    break
            if len(search_results_in_articles_index) > 3: # in case there is a selection of > 15 articles
                shuffle(search_results_in_articles_index)
                articles_index = search_results_in_articles_index[:3]
            else:
                articles_index = search_results_in_articles_index

            print("Ok, so based on the information you have provided, I think I have a nice selection of Beyond Social articles for you to read. These have been written by students, teachers, and friends of WdKA Social Practices. While I print this out for you, one of my chatbots will serve you a parting gift from our shadow library. It contains research material that our teachers are currently reading or writing.", "\n\n\n\n\n",file=stdout)
                
 #           print('\n\n\n> > > In the print queue, {} pages were found to contain the words {}\n\n\n'.format(len(articles_index),(", ").join(user_terms) ),file=stdout )
#            print( '\n\n\n> > > The following articles will be printed:\n\n\n', colors.GREEN, (("\n\n\n").join(articles_index ) ), colors.ENDC )

        # elif 'irc' in key:
        #     from irc import irc # import needs to be here in order to only establish a connection at this point
        #     irc( 'bsuser' )
        # # how the IRC add to the article index ???

        
        

        
    return articles_index

# QUESTIONNAIRE IS RUN BY run-questionnaire.py or print-sequence.py
#articles_index = questionnaire()
 # for some unknow reason nickname has to be hard coded
 
#print(escpos['papercut'], file=stdout) # move to print-sequence
