#!/usr/bin/env python
# Copyright (c) - Dagan Martinez 2015
# This is a program to manually find desired or relevant columns in a folder of CSV files
# The user enters "YES"  or "NO" depending on whether the shown text is of any relevance to the use

import ecsv
import os

# Define variable
searchdir = "./Hospital_Revised_Flatfiles"
files = os.listdir(searchdir)
columns = [] # List of columns to iterate through
usedlist = [] # List of used columns
goodlist=[] # List of columns to export
quit_bool = False # Quit - helps to break multiple loops
filenumber = 0 # Current file number

# Cycle through files
for file in files:
    filenumber+=1

    # Create list of columns
    grid = ecsv.make_grid_from_csv(searchdir+"/"+file)
    columns=ecsv.get_columns_from_grid(grid,range(0,len(grid[0])),individual=True)

    # Cycle through columns
    for column in columns:
            # Clear screen
            if os.sys.platform == "win32":
                os.system("cls")
            else:
                os.system("clear")

            # Skip columnif seen before
            if column[0] in usedlist:
                continue

            # Print out question
            print("<File "+str(filenumber)+": "+file+">")
            print("<Column "+str(columns.index(column)+1)+": "+column[0]+">")
            print("")
            if len(column)>1:
                print('"'+column[1]+'"')
                if len(column)>2:
                    print('"'+column[2]+'"')
                    if len(column)>3:
                        print('"'+column[3]+'"')
                        if len(column)>4:
                            print('"'+column[4]+'"')
            else:
                continue
            print('\nDoes this look "of relevance" to you? (Y/N)')

            #Take in input
            inp=""
            while True:
                if os.sys.version_info[0]==3:
                    inp = input().upper()
                else:
                    inp = raw_input().upper()
                if inp[0] == "Y" or inp[0:4]=="SURE" or inp=="IDC":
                    goodlist.append(column[0])
                    usedlist.append(column[0])
                    break
                elif inp[0] == "N":
                    usedlist.append(column[0])
                    break
                elif inp == "QUIT":
                    quit_bool = True
                    break
                elif inp == "FORFEIT":
                    exit()
                else:
                    print("DID NOT RECOGNIZE COMMAND")
                    continue
            if inp=="QUIT":
                break

    # Calm the user
    if os.sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")
    print("Loading next file - please wait")
    print("You may want to get some trail mix")

    # Break your rusty chain and run
    if quit_bool:
        print("\nBreaking...")
        break


# Prepare to export as Python
print("Exporting...")
import socket
import datetime
export_name = "EXPORTED_COLUMNS.TXT"
text="# Exported by "+__file__+" on "+socket.gethostname()+"("+os.sys.platform+"/"+os.name+")\n# @ "+str(datetime.datetime.now())+"\n# Last file read: "+file+"\n# Files read: "+str(filenumber)+"\n# Columns: "+str(len(goodlist))+"\n\ndesired_columns=["

# Record list of columns
for i in goodlist:
    text+='"'+i.replace('"','\\"')+'", '
text=text[0:len(text)-2]+"]"

# Write to file
exp_file=open(export_name,"w")
exp_file.write(text)
exp_file.close()
print("Exported as \""+export_name+"\"")
