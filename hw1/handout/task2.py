# -*- coding: utf-8 -*-
"""
For Spring 2019 NLP class

Homework 1 Task 1

@author: Jennifer Li
"""
import sys
import os
from collections import OrderedDict

def decrypt(encryptFile, datafolder):
    # do frequency analysis for files in nyt
    nytfiles = os.listdir(datafolder);
    char_freq_data = {}
    char_freq_test = {}
    for eachletter in "abcdefghijklmnopqrstuvwxyz":
        char_freq_data[eachletter] = 0
        char_freq_test[eachletter] = 0
    for eachfile in nytfiles:
        curr_r_path = os.path.join(datafolder, eachfile)
        currfile_r = open(curr_r_path, "r")
        file_content = currfile_r.readlines()
        for eachline in file_content:
            eachline = eachline.rstrip()
            for eachletter in "abcdefghijklmnopqrstuvwxyz":
                char_freq_data[eachletter] += eachline.count(eachletter)
                char_freq_data[eachletter] += eachline.count(eachletter.upper())
        currfile_r.close()
    sorted_char_freq =  sorted(char_freq_data.items(),key=lambda item:item[1],
                                                       reverse=True)
    # do frequency analysis for mit.txt
    f = open(encryptFile, "r")
    content = f.readlines()
    for eachline in content:
        # eachline = eachline.rstrip()
        for eachletter in "abcdefghijklmnopqrstuvwxyz":
            char_freq_test[eachletter] += eachline.count(eachletter)
    sorted_mit_freq =  sorted(char_freq_test.items(),key=lambda item:item[1],
                                                       reverse=True)
    f.close()
    match = {}
    for (k, v), (k1, v1) in zip(OrderedDict(sorted_char_freq).items(), 
                                OrderedDict(sorted_mit_freq).items()):
        print("match['" + k1  + "'] = '" + k + "'")
        match[k1] = k
        
    match['s'] = 'e'
    match['k'] = 't'
    match['t'] = 'o'  # match['t'] = 'a'
    match['v'] = 'a'  # match['v'] = 'o'
    match['p'] = 'n'  # match['p'] = 'i'
    match['c'] = 'i'  # match['c'] = 'i'
    match['n'] = 's'
    match['j'] = 'r'
    match['i'] = 'h'
    match['o'] = 'd'  # match['o'] = 'l'
    match['z'] = 'l'  # match['z'] = 'd'
    match['e'] = 'c'
    match['m'] = 'f'  # match['m'] = 'u'
    match['r'] = 'm'
    match['w'] = 'u'  # match['w'] = 'f'
    match['l'] = 'p'  # match['l'] = 'g' 
    match['x'] = 'g'  # match['x'] = 'p'
    match['f'] = 'w'
    match['b'] = 'y'
    match['a'] = 'v'  # match['a'] = 'b'
    match['y'] = 'b'  # match['y'] = 'v'
    match['d'] = 'k'
    match['q'] = 'x'
    match['h'] = 'j'
    match['u'] = 'q'  # match['u'] = 'z'
    match['g'] = 'z'  # match['g'] = 'q'
    
    outputFile = open("decoded.txt", "w")
    f = open(encryptFile, "r")
    content_in_chars = f.read()
    decrypted_content = ""
    for eachChar in content_in_chars:
        if eachChar.isalpha():
            if eachChar.isupper():
                decrypted_content += match[eachChar.lower()].upper()
            else:
                decrypted_content += match[eachChar]
        else:
            decrypted_content += eachChar
    outputFile.write(decrypted_content)
    outputFile.close()
    f.close()
            

if __name__ =='__main__':
    decrypt(sys.argv[1], "nyt")
