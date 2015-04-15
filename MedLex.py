#!/usr/bin/env python
# Copyright (c) - Dagan Martinez 2015

import ecsv
import os
import wordify

#Define variables
searchdir="./Hospital_Revised_Flatfiles"
columns=["HCAHPS Question","Measure Name","Footnote Text","HCAHPS Answer Description"]
files=os.listdir(searchdir)
stuff=[]

it=0 # Iteration control
# Pull data from files
for file in files:
    stuff+=ecsv.get_columns_from_csv(searchdir+"/"+file,columns)[1::]
    os.sys.stdout.write("Files: {0} with {1} results   \r".format(str(it),str(len(stuff))))
    if it>=4: break
    it+=1

# Get words from data
print("\nGetting words")
words=wordify.getWords(stuff,exclude=wordify.STOP_WORDS+wordify.ALPHABET)

# Organize data
print("Organizing words")
counts=wordify.getWordCounts(words)

# Get words from 2D array
print("Preparing to export")
output=""
for word in counts:
    output+=word[0]+"\n"

# Export
print("Exporting")
fout=open("lexi.txt","w")
fout.write(output)
fout.close()