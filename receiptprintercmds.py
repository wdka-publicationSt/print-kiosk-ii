#!/usr/bin/env python3
import sys
try:
    stdout = open('/dev/ttyUSB0','w')
    stderr = open('/dev/ttyUSB0','w')
except:
    stdout = sys.__stdout__
    stderr = sys.__stderr__ 
    print('no receipt printer connected')

escpos = {
    "init_printer":  "\x1B\x40",

    "justify_left": "\x1B\x61\x00",
    "justify_center": "\x1B\x61\x01",

    'halfwidth_on': "\x1B\x21\x01",
    'halfwidth_off': "\x1B\x21\x00",

    'doubleprinting_on': "\x1B\x47\x01",
    'doubleprinting_off': "\x1B\x47\x00",

    'emphasis_on': '\x1B\x45\x01',
    'emphasis_off': '\x1B\x45\x00',
    
    'largefont': "\x1B\x21\x90", # 0=None 70=very lage+intalic, 90= medium large
    'mediumfont': "\x1B\x21\x90",
    'normalfont': "\x1B\x21\x00",

    'space_btw_letters': '\x1B\x20\x01', # n [0,255]

    'feedamount': '\x1B\x33\x09', #?

    'paperfeed': '\x1B\x4A\x01' , #??
    'papercut':'\x1D\x56\x00', 

    'direction_0': '\x1B\x56\x00' , 
    'direction_90': '\x1B\x56\x01' ,

    'pagedefault': '\x1B\x53' , #?
}
