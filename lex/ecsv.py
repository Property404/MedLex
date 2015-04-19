# Copyright (c) - 2015 Dagan Martinez
# This module enables the programmer to easily interact with CSV files
import csv
from sys import version_info

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

def get_columns_from_grid(grid,columns,individual=False):
 #Convert columns argument to list of ints
    if isinstance(columns,int):
        columns=[columns]
    elif isinstance(columns,str):
        if columns in grid[0]:
            columns=[grid[0].index(columns)]
        else:
            columns=[]
    elif isinstance(columns[0],str):
        temp=[]
        for s in columns:
            if s not in grid[0]:
                continue
            temp.append(grid[0].index(s))
        columns=temp

    # Start finding result
    result=[]
    for column in columns:
        inv_result=[]
        for row in grid:
            if version_info[0]==3:
                inv_result.append(row[column].encode('ascii','ignore'))
            else:
                inv_result.append(row[column].decode('unicode_escape').encode('ascii','ignore'))
        if individual:
            result.append(inv_result)
        else:
            result+=inv_result

    # Return items in selected columns
    return result
def get_row_from_grid(grid,row):
    return grid[row]

def get_columns_from_csv(filename,columns):
    return get_columns_from_grid(make_grid_from_csv(filename),columns)

