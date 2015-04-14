# This module enables the programmer to easily interact with CSV files
import csv
from sys import version_info
from unicodedata import normalize

def make_grid_from_csv(filename):
    # Create grid variable
    grid=[]

    # open file
    with open(filename) as csvfile:
        # read file
        reader=csv.reader(csvfile)
        # Store file until finished(exception is raised)
        while True:
            try:
                if version_info[0]==3:
                    grid.append(reader.__next__())
                else:
                    grid.append(reader.next())
            except:
                break
    return grid

def get_columns_from_grid(grid,columns):
 #Convert columns argument to list of ints
    if isinstance(columns,int):
        columns=[columns]
    elif isinstance(columns,str):
        try:
            columns=[grid[0].index(columns)]
        except:
            columns=[]
    elif isinstance(columns[0],str):
        temp=[]
        for s in columns:
            try:
                temp.append(grid[0].index(s))
            except:
                pass
        columns=temp

    # Start finding result
    result=[]
    for column in columns:
        row=0
        # Add cells to result until exception in raised
        while True:
            try:
                result.append(str(((grid[row])[column]).decode('UTF-8')))
                row+=1
            except:
                 break
    # Return items in selected columns
    return result

def get_columns_from_csv(filename,columns):
    return get_columns_from_grid(make_grid_from_csv(filename),columns)

