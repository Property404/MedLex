#!/usr/bin/env python
# Copyright (c) - 2015 Dagan Martinez

import lex.ecsv as ecsv
import os
import lex.wordify as wordify

#Define variables
searchdir="./Hospital_Revised_Flatfiles"
columns=["HCAHPS Question","Measure Name","Footnote Text","HCAHPS Answer Description"]
files=os.listdir(searchdir)
stuff=[]
it=0 # Iteration control


# Pull data from files
print("Pulling data from files")
for file in files:
    stuff+=ecsv.get_columns_from_csv(searchdir+"/"+file,columns)[1::]
    os.sys.stdout.write("Files: {0} with {1} cells   \r".format(str(it),str(len(stuff))))
    if it>=6: break
    it+=1


# Get words from data
print("\nGetting words")
words=wordify.getWords(stuff, exclude=wordify.JUNK_WORDS)


# Create lexicon - 75% scrutiny
print("Creating lexicon")
words.sort()
lexicon=wordify.associateWords(words,.75)


# Make output
print("Exporting")
output=""
for group in lexicon:
    for word in group:
        output+=word+", "
    output+="\n"


# Export
fout=open("lexi.txt","w")
fout.write(output)
fout.close()
