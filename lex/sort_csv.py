#!/usr/bin/env python
# Copyright (c) - 2015 Dagan Martinez
# This is a module to manually find desired or relevant columns in a folder of CSV files
# The user enters "YES"  or "NO" depending on whether the shown text is of any relevance to the use

import lex.ecsv as ecsv
import os


def run(searchdir, limit, automatic=False):
    # Import extra stuff
    if automatic:
        import lex.vocabulary
    # Define variable
    files = []
    for root, sub, docs in os.walk(searchdir):
            for csv_file in docs:
                files.append(root+"/"+csv_file)
    usedlist = []  # List of used columns
    goodlist = []  # List of columns to export
    quit_bool = False  # Quit - helps to break multiple loops
    filenumber = 0  # Current file number

    # Cycle through files
    for file in files:
        filenumber += 1

        # Create list of columns
        grid = ecsv.make_grid_from_csv(file)
        columns = ecsv.get_columns_from_grid(grid, range(0, len(grid[0])), individual=True)

        # Cycle through columns
        for column in columns:

                # Clear screen
                if not automatic:
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
                first_column = ""
                if len(column) > 1:
                    print('"'+column[1]+'"')
                    first_column = column[1]
                else:
                    continue
                if not automatic:
                    if len(column) > 2:
                        print('"'+column[2]+'"')
                        if len(column) > 3:
                            print('"'+column[3]+'"')
                            if len(column) > 4:
                                print('"'+column[4]+'"')
                    print('\nDoes this look "of relevance" to you? (Y/N)')

                # Take in input
                while True:
                    if automatic:
                        inp = "N"
                        for i in lex.vocabulary.vocab:
                            if i in first_column.split(" "):
                                inp = "Y"
                                break
                        print(inp)
                    else:
                        if os.sys.version_info[0] >= 3:
                            inp = input().upper()
                        else:
                            inp = raw_input().upper()
                    if len(inp) > 0 and inp[0] == "Y":
                        goodlist.append(column[0])
                        usedlist.append(column[0])
                        break
                    elif len(inp) > 0 and inp[0] == "N":
                        usedlist.append(column[0])
                        break
                    elif len(inp) > 0 and inp[0] == "H":
                        print("""COMMANDS:
    YES - add column to list
    NO - skip column
    DONE - Save and exit
    FORFEIT - Give up and exit
    HELP - Display this message""")
                        continue
                    elif inp == "DONE":
                        quit_bool = True
                        break
                    elif inp == "FORFEIT":
                        exit()
                    else:
                        print("DID NOT RECOGNIZE COMMAND\nTYPE 'HELP' FOR LIST OF COMMANDS")
                        continue
                if quit_bool:
                    break
        # Break your rusty chain and run
        if quit_bool or filenumber == limit:
            print("\nBreaking and exporting...")
            break

        # Calm the user
        if not automatic:
            if os.sys.platform == "win32":
                os.system("cls")
            else:
                os.system("clear")
            print("Loading next file - please wait")
            print("If it's a big file, you may want to get some trail mix")

    # Record list of columns
    return str(goodlist)
