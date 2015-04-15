#!/usr/bin/env python
# Copyright (c) - 2015 Dagan Martinez

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

# Create lexicon - 75% scrutiny
lexicon=wordify.associateWords(words,.75)

# Make output
print("Preparing to export")
output=""
for group in lexicon:
    for word in group:
        output+=word+", "
    output+="\n"

# Export
print("Exporting")
fout=open("lexi.txt","w")
fout.write(output)
fout.close()