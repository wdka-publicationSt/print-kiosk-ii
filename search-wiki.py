#!/usr/bin/env python3


##### 
# Script loads the wiki site
# To be loaded by other scripts that use the wiki APIo
from wikisite import *

search_results = site.search(search="Rotterdam", namespace='0',what="text" )
for match in list(search_results): 

    print('title:', match['title'])
    print('snippet:', match['snippet'])
    print('\n')
