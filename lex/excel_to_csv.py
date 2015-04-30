import xlrd
import csv
from sys import version_info
def excel_to_csv(excel_filename,new_directory):
    if new_directory[-1]!='/':
        new_directory+='/'
    workbook=xlrd.open_workbook(excel_filename)
    it=0
    for sheetname in workbook.sheet_names():
        it+=1
        csv_filename=new_directory+excel_filename+"_sheet"+str(it)+'.csv'
        #print(csv_filename)
        #exit()
        csv_file=open(csv_filename, "wb")
        sheet=workbook.sheet_by_name(sheetname)
        writer=csv.writer(csv_file,quoting=csv.QUOTE_ALL)

        for rownumber in range(sheet.nrows):
            row=sheet.row_values(rownumber)
            for i in range(len(row)):
                str_obj=basestring
                if version_info[0]==3:
                    str_obj=str
                if isinstance(row[i],str_obj):
                    row[i]=str(u''.join([k if ord(k)<128 else '' for k in row[i]]))
            try:
                writer.writerow(row)
            except:
                print(row)
        csv_file.close()
