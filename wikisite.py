#!/usr/bin/env python3

##### 
# Script loads the wiki site
# To be loaded by other scripts that use the wiki API
#####
from mwclient import Site
#from mwclient.listing import List
#from mwclient import Page
from argparse import ArgumentParser

p = ArgumentParser()
p.add_argument("--host", default="beyond-social.org")
p.add_argument("--path", default="/wiki/", help="nb: should end with /")
args = p.parse_args()


site = Site(args.host, args.path)
# print(site)
