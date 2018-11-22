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
    "justify_right": "\x1B\x61\x02",

    'doubleprinting_on': "\x1B\x47\x01",
    'doubleprinting_off': "\x1B\x47\x00",
    
    'largefont': "\x1B\x21\x30", # 0=None 70=very lage+intalic, 90= medium large
    'mediumfont': "\x1B\x21\x10",
    'normalfont': "\x1B\x21\x00",

    'space_btw_letters_0L': '\x1B\x20\x00', # n [0,255]
    'space_btw_letters_5L': '\x1B\x20\x05', # n [0,255]
    'space_btw_letters_10L': '\x1B\x20\x10', # n [0,255]
    'space_btw_letters_20L': '\x1B\x20\x20', # n [0,255]    

    'paperfeed_1l': '\x1B\x64\x01' , 
    'paperfeed_10l': '\x1B\x64\x10' , 
    'papercut':'\x1D\x56\x00', 

    'direction_0': '\x1B\x56\x00' , 
    'direction_90': '\x1B\x56\x01' ,

    'reverse_print_on': '\x1D\x42\x01',
    'reverse_print_off': '\x1D\x42\x00'
}
