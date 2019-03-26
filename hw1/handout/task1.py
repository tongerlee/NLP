# -*- coding: utf-8 -*-
"""
For Spring 2019 NLP class

Homework 1 Task 1

@author: Jennifer Li
"""

import sys
import os


def replaceName(namelist, rfoldername, wfoldername):
    f = open(namelist, "r")
    nytfiles = os.listdir(rfoldername);
    banned_names = f.readlines()
    # print(nytfiles)
    # print (content)
    if not os.path.exists(wfoldername):
        os.makedirs(wfoldername)
#    testline = "Tiger-Woods' should not change, Woodsever should also not change, Tiger Woods' needs to be changes, Woods will be smith as well"
#    testline = testline.replace("Tiger Woods", "John Smith")
#    for eachletter in "abcdefghijklmnopqrstuvwxyz-":
#        testline = testline.replace("Woods"+eachletter, "zzzzz" + eachletter)
#    testline = testline.replace("-"+"Woods", "donotchangethis")
#    testline = testline.replace("Woods", "Smith")
#    testline = testline.replace("donotchangethis", "-"+"Woods")
#    for eachletter in "abcdefghijklmnopqrstuvwxyz":
#        testline = testline.replace("zzzzz"+eachletter, "Woods" + eachletter)
#    print(testline)
    for eachfile in nytfiles:
        curr_w_path = os.path.join(wfoldername, eachfile)
        curr_r_path = os.path.join(rfoldername, eachfile)
        currfile_r = open(curr_r_path, "r")
        currfile_w = open(curr_w_path, "w")
        file_content = currfile_r.readlines()
        for eachline in file_content:
            for eachname in banned_names:
                eachname = eachname.rstrip()
                eachline = eachline.replace(eachname, "John Smith")
                lastName = eachname.split()[-1]
                for eachletter in "abcdefghijklmnopqrstuvwxyz-":
                    eachline = eachline.replace(lastName+eachletter, "zzzzz" + eachletter)
                eachline = eachline.replace("-"+lastName, "donotchangethis")
                eachline = eachline.replace(" " + lastName, " Smith")
                eachline = eachline.replace("donotchangethis", "-"+lastName)
                for eachletter in "abcdefghijklmnopqrstuvwxyz":
                    eachline = eachline.replace("zzzzz"+eachletter, lastName + eachletter)
            currfile_w.write(eachline)
        currfile_r.close()
        currfile_w.close()
    print("Task 1 done!")       
    
    
if __name__ =='__main__':
    replaceName(sys.argv[1], "nyt", "nytmodified")
    