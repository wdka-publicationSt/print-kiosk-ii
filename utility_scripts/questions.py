questions = {
    '01-time' : {
        'question' : 'First, a bodily check-in. Are you most productive before noontime (12h)?',
        'variables' : ['yes','no'],
        'reply' : '',
        'error' : '',
        'noanswer': '',
        'user_answers': None
    },
    '02-common-words' : {
        'question' : 'Which words would you expect a Social Practice curriculum or project to have in mind?\n\n Write one at a time and press Enter.',
        'variables' : [],
        'reply': 'Looks like I have some articles that match your biorythym and your concept of a socially engaged cultural practice.',
        'error': ["Oh dear. We don't seem to have anything that matches those keywords. We will place your suggested concepts on a pedagogical wishlist and see whether we can incorporate them into our curriculum. Let's try again.", "Hmmm. Still no match. Let's try again. Your suggestions, by the way, have been added to a pedagogical wishlist.", "OK, wow. Your pedagogical style is quite radical. While we wait for our faculty to catch up with your futuristic approach to social practice, let's move on to the next content service filter."],
        'noanswer': 'I believe you forgot to provide an answer to my question.',
        'user_answers': None
    },
    
    '03-free-association' : {
        'question' : "Please write the first word that comes to your mind.",
        'variables' : ['empowerment', 'representation', 'activism', 'commons', 'engagement', 'whiteness', 'ownership', 'sustainability', 'identity', 'pedagogy', 'technology', 'participation'], 
        # more words could be here, from which only 3 will be randomly selected, and more if needed in order to  exampand the print quue
        'reply' : '{pagenumber} pages were found with to have the terms {terms} in them',
        'error': '{terms} have been in the minds of the Beyond Social editors, let\'s try others',
        'noanswer': 'No answer??',
        'user_answers': None
    },
    
    '04-irc' : {
    'question' : "",
        'variables' : [], 
        'reply' : '',
        'error': '',
        'noanswer': '',
        'user_answers': None
    }
}
