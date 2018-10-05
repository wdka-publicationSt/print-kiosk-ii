#!/usr/bin/env python3


##### 
# Script loads the wiki site
# To be loaded by other scripts that use the wiki APIo
from wikisite import *

def search_request(query, namespace, reach):
	search_results = site.search(search=query, namespace='0', what=reach)
	search_results_titles = []
	for match in list(search_results): 

	    # print('title:', match['title'])
	    # print('snippet:', match['snippet'])
	    # print('\n')
	    search_results_titles.append(match['title'])
	
	return search_results_titles
