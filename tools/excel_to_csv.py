import xlrd
import csv
import random
import os
def excel_to_csv(excel_filename,new_directory):
    if new_directory[-1]!='/':
        new_directory+='/'
    workbook=xlrd.open_workbook(excel_filename)
    for sheetname in workbook.sheet_names():
        csv_filename=new_directory+str(random.randint(0,1000))+"_"+sheetname+'.csv'
        #print(csv_filename)
        #exit()
        csv_file=open(csv_filename, "wb")
        sheet=workbook.sheet_by_name(sheetname)
        writer=csv.writer(csv_file,quoting=csv.QUOTE_ALL)

        for rownumber in range(sheet.nrows):
            row=sheet.row_values(rownumber)
            for i in range(len(row)):
                if isinstance(row[i],basestring):
                    row[i]=str(u''.join([k if ord(k)<128 else '' for k in row[i]]))
            try:
                writer.writerow(row)
            except:
                print(row)
        csv_file.close()

if __name__=="__main__":
    files=os.listdir("dartmouth_files")
    for i in range(len(files)):
        excel_to_csv("dartmouth_files/"+files[i],"dartmouth_files_csv")
        os.sys.stdout.write("Converting... "+str((100*i)//len(files))+"%\r")
    print("")
