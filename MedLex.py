#!/usr/bin/env python
# Copyright (c) - 2015 Dagan Martinez

import lex.ecsv as ecsv
import os
import lex.wordify as wordify
import time



def run_medlex(filename="medlex_result.txt"):
    starttime=time.time()

    #Define variables
    searchdirs=["./data/Dartmouth_Files","./data/Hospital_Revised_Flatfiles"]
    columns=["HCAHPS Question","Measure Name","Footnote Text","HCAHPS Answer Description"]

    stuff=[]
    it=1 # Iteration control


    # Pull data from files
    for current_dir in searchdirs:
        print("Pulling data from "+current_dir)
        files=os.listdir(current_dir)
        for file in files:
            grid=ecsv.make_grid_from_csv(current_dir+"/"+file)
            stuff+=ecsv.get_columns_from_grid(grid,columns)[1::]
            stuff+=ecsv.get_row_from_grid(grid,0)
            os.sys.stdout.write("Files: {0} with {1} cells   \r".format(str(it),str(len(stuff))))
            it+=1
            if it>100: break
        print("")


    # Get words from data
    print("Getting words")
    words=wordify.getWords(stuff, exclude=wordify.JUNK_WORDS+wordify.COMMON_WORDS)


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
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError:
        pass
    fout=open(filename,"w+")
    fout.write(output)
    fout.close()
    print("Time: "+str(time.time()-starttime))


default_plaintext_filename="medlex_result.txt"
if len(os.sys.argv)==1:
        run_medlex(default_plaintext_filename)
elif os.sys.argv[1][0]=="-":
    if "d" in os.sys.argv[1]:
        import lex.download_data as download_data
        download_data.download_all_data()
    if "r" in os.sys.argv[1]:
        if len(os.sys.argv)>2:
            run_medlex(os.sys.argv[2])
        else:
            run_medlex(default_plaintext_filename)