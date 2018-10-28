questions = {
    '01-time' : {
        'question' : 'First, a bodily check-in. Are you most productive before noontime (12h)?',
        'variables' : ['yes','no'],
        'reply' : '',
        'error' : '',
        'user_answers': None
    },
    '02-common-words' : {
        'question' : 'Now, a  question. Which words would you expect a Social Practice curriculum or project to have in mind?',
        'variables' : [],
        'reply': '{pagenumber} pages were found with to have {term} in mind',
        'error': '{} does not seem to be a word that Social Practice at Willem de Kooning Academy is throwing around, we will add it to our wishlist.  Please try another.',
        'user_answers': None
    },
    '03-free-association' : {
        'question' : "Please write the first word that comes to your mind. Don't overthink it.",
        'variables' : ['activism', 'commons', 'representation', 'engagement', 'empowerment', 'participation', 'ownership', 'sustainability', 'identity', 'pedagogy', 'technology', 'whiteness'], 
        # more words could be here, from which only 3 will be randomly selected, and more if needed in order to  exampand the print quue
        'reply' : '{pagenumber} pages were found with to have the terms {terms} in them',
        'error': '{terms} have been in the minds of the Beyond Social editors, let\'s try others',
        'user_answers': None
    },
    '04-irc' : {
    'question' : "",
        'variables' : [], 
        # more words could be here, from which only 3 will be randomly selected, and more if needed in order to  exampand the print quue
        'reply' : '',
        'error': '',
        'user_answers': None
    }
}
