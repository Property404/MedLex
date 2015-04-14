#!/usr/bin/env python
# Dagan Martinez 2015

import ecsv
import os
import wordify

searchdir="./Hospital_Revised_Flatfiles";
columns=["HCAHPS Question","Measure Name","Footnote Text","HCAHPS Answer Description"]
files=os.listdir(searchdir)
stuff=[]
it=0
for file in files:
    os.sys.stdout.write("Files: {0} with {1} results   \r".format(str(it),str(len(stuff))))
    stuff+=ecsv.get_columns_from_csv(searchdir+"/"+file,columns)[1::]
    if it>=200: break
    it+=1

print("\nGetting words")
words=wordify.getWords(stuff,exclude=wordify.STOP_WORDS+wordify.ALPHABET)

print("Organizing words")
counts=wordify.getWordCounts(words)

print("Preparing to export")
output=""
for word in counts:
    output+=word[0]+"\n"

print("Exporting")
fout=open("lexi.txt","w")
fout.write(output)
fout.close()