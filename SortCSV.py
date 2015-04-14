# This is a program to manually find desired or relevant columns in a folder of CSV files
# The user enters "YES"  or "NO" depending on whether the shown text is of any relevance to the use

import ecsv
import os

# Define variable lists
searchdir = "./Hospital_Revised_Flatfiles";
files = os.listdir(searchdir);
columns = []
badlist = []


quit_bool = False # for breaking multiple loops
filenumber = 0
for file in files:
    filenumber+=1
    i = 0 # Iterate through columns
    # assign a grid based on CSV file
    grid = ecsv.make_grid_from_csv(searchdir+"/"+file)
    while True:
        try:
            os.system("cls")

            # Get column
            column = ecsv.get_columns_from_grid(grid,i)

            # Skip if seen before
            if column[0] in badlist:
                i+=1
                continue
            # Print out question
            print("File "+str(filenumber)+"("+file+") , column "+str(i+1))
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
                i+=1
                continue
            print('\nDoes this look "of relevance" to you? (Y/N)');

            #Take in input
            if os.sys.version_info[0]==3:
                inp = input().upper()
            else:
                inp = raw_input().upper()
            if inp[0] == "Y" or inp[0:4]=="SURE" or inp=="IDC":
                columns.append(column[0])
                badlist.append(column[0])
            elif inp[0] == "N":
                badlist.append(column[0])
            elif inp == "QUIT":
                quit_bool = True
                break
            elif inp == "FORFEIT":
                exit()
            else:
                print("DID NOT RECOGNIZE COMMAND")
                continue
            i+=1
        except Exception as e:
            print("Exception "+str(e.args)+'\n')
            print("Loading next file - please be patient")
            break
    # Break your rusty chain and run
    if quit_bool:
        print("\nBreaking...")
        break


# Export as Python
print("Exporting...")
import socket
import datetime
export_name = "EXPORTED_COLUMNS.TXT"
text="# Written by "+__file__+" on "+socket.gethostname()+"("+os.sys.platform+"/"+os.name+")\n# @ "+str(datetime.datetime.now())+"\n# Last file read: "+file+"\n# Files read: "+str(filenumber)+"\n# Columns: "+str(len(columns))+"\n\ndesired_columns=["
# Record list of columns
for i in columns:
    text+='"'+i.replace('"','\\"')+'", '
text=text[0:len(text)-2]+"]"
# Write to file
exp_file=open(export_name,"w")
exp_file.write(text)
exp_file.close()
print("Exported as \""+export_name+"\"")
