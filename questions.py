
questions = {
    '01-time' : {
        'question' : 'Are you most productive during normalized working day hours (9am-5pm)?',
        'variables' : ['yes','no'],
        'reply' : '',
        'error' : '',
        'user_answers': None
    },
	'02-common-words' : {
            'question' : 'Which words would you expect a Social Practice curriculum or project to have in mind?',
            'variables' : [],
            'reply': '{pagenumber} pages were found with to have {term} in mind',
            'error': '{} does not seem to be a word that Social Practice curriculum or project to have yet in mind, please try another.',
        'user_answers': None
        },
	'03-free-association' : {
            'question' : 'Please write the first word that comes to your mind.',
            'variables' : ['activism', 'democracy', 'representation', 'engagement', 'community'], # more words could be here, from which only 3 will be randomly selected, and more if needed in order to  exampand the print quue 
            'reply' : '{pagenumber} pages were found with to have the terms {terms} in them',
            'error': '{terms} have been in the minds of the Beyond Social editors, let\'s try others',
        'user_answers': None            
        }
}
