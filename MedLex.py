#!/usr/bin/env python
# Copyright (c) - 2015 Dagan Martinez
import os




def run_medlex(filename="medlex_result.txt"):
    import lex.ecsv as ecsv
    import lex.wordify as wordify
    import time
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



#Make MAN page
MAN_PAGE="""MedLex - Medical Lexicon

usage: medlex [arguments]
   or: medlex [arguments] [file]
   or: medlex [arguments] [txtfile] [htmlfile]

Arguments:
   -f\t\tExport formatted dictionary
   -r\t\tRun MedLex (automatic if no option flags)
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


# Deal with arguments
plaintext_filename="medlex_result.txt"
format_filename="medlex_result.html"
temp_folder="C:/Users/Dagan/AppData/Local/Temp/"
argc=len(os.sys.argv)
argv=os.sys.argv
flags="-r"
if argc>1:
    if argv[1][0]=="-":
        flags=argv[1]
    else:
        argv.insert(1,flags)
        argc+=1
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
            print(MAN_PAGE)
            exit()
    elif "r" in flags:
        if argc==3:
            plaintext_filename=argv[2]
        elif argc>3:
            print("Too many arguments\n")
            print(MAN_PAGE)
            exit()
    if "d" in flags:
        import lex.download_data
        lex.download_data.download_all_data(temp_path=temp_folder,data_path="./data/")

if "r" in flags:
    run_medlex(plaintext_filename)
if "f" in flags:
    import lex.format_lex
    lex.format_lex.format_lex(plaintext_filename,format_filename)