
questions = {
    '01-time' : {
        'question' : 'Are you most productive during normalized working day hours (9am-5pm)?',
        'variables' : ['yes','no'],
        'reply' : '',
        'error' : ''
    },
	'02-common-words' : {
            'question' : 'Which words would you expect a Social Practice curriculum or project to have in mind?',
            'variables' : [],
            'reply': '{pagenumber} pages were found with to have {term} in mind',
            'error': '{} does not seem to be a word that Social Practice curriculum or project to have yet in mind, please try another.'
        },
	'03-free-association' : {
            'question' : 'Please write the first word that comes to your mind.',
            'variables' : ['activism', 'democracy', 'representation'],
            'reply' : '{pagenumber} pages were found with to have the terms {terms} in them',
            'error' : ''
        }
}
