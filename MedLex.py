#!/usr/bin/env python
# Copyright (c) - 2015 Dagan Martinez
import os




def run_medlex(filename="medlex_result.txt"):
    import lex.ecsv as ecsv
    import lex.wordify as wordify
    import time
    starttime=time.time()

    #Define variables
    searchdirs=[os.path.dirname(os.path.realpath(__file__))+"/data/Dartmouth_Files",os.path.dirname(os.path.realpath(__file__))+"/data/Hospital_Revised_Flatfiles"]
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



#Make MAN page
MAN_PAGE="""MedLex - Medical Lexicon

usage: medlex [option]
   or: medlex [option] [file]
   or: medlex [option] [txtfile] [htmlfile]

Options:
   -f\t\tExport formatted dictionary
   -r\t\tRun MedLex
   -d\t\tDownload required medical data
   -h\t\tPrint Help (this message) and exit
   -l\t\tPrint license and exit
"""

LICENSE_PAGE="""GPL License
Copyright (c) - 2015 Dagan Martinez

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
TRY_HELP="Try 'medlex -h' for more information"


# Deal with arguments
plaintext_filename="medlex_result.txt"
format_filename="medlex_result.html"
temp_folder="C:/Users/Dagan/AppData/Local/Temp/"
argv=os.sys.argv
available_flags="drfhl"
flags=""

#concat flags
i=0
for i in range(len(argv)-1):
    if argv[i+1][0]=="-":
        flags+=argv[i+1][1::]
    else:
        i-=1
        break

argv=[argv[0],"-"+flags]+argv[i+2::]
print(argv)
argc=len(os.sys.argv)


# Check for improper flags
for i in flags:
    if i not in available_flags:
        print ("Unknown option: '"+i+"'")
        print (TRY_HELP)
        exit()
flags=""


# Make sure there are arguments
if argc==1:
    print ("No arguments")
    print (TRY_HELP)
    exit()


# Interpret arguments
if argc>1:
    if argv[1][0]=="-":
        flags=argv[1]
    else:
        print("No flags. Please use -d, -r, -f, -h, or -l")
        print (TRY_HELP)
        exit()
    if "h" in flags:
        print(MAN_PAGE)
        exit()
    if "l" in flags:
        print(LICENSE_PAGE)
        exit()
    if "f" in flags:
        if argc>=2:
            if "r" in flags:
                plaintext_filename=temp_folder+plaintext_filename
        if argc>=3:
            format_filename=argv[2]
        if argc==4:
            plaintext_filename=argv[2]
            format_filename=argv[3]
        if argc>4:
            print("Too many arguments\n")
            print (TRY_HELP)
            exit()
    elif "r" in flags:
        if argc==3:
            plaintext_filename=argv[2]
        elif argc>3:
            print("Too many arguments\n")
            print (TRY_HELP)
            exit()
    if "d" in flags:
        import lex.download_data
        lex.download_data.download_all_data(temp_path=temp_folder,data_path="./data/")

if "r" in flags:
    run_medlex(plaintext_filename)
if "f" in flags:
    import lex.format_lex
    lex.format_lex.format_lex(plaintext_filename,format_filename)