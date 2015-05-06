import xlrd
import csv
from sys import version_info
import os.path


def excel_to_csv(excel_path, new_directory):
    if new_directory[-1] != '/':
        new_directory += '/'
    excel_filename = os.path.basename(excel_path)
    workbook = xlrd.open_workbook(excel_path)

    it = 0
    for sheetname in workbook.sheet_names():
        it += 1
        csv_filename = new_directory + excel_filename+"_sheet" + str(it) + '.csv'
        if version_info[0] >= 3:
            csv_file = open(csv_filename, "w", newline='')
        else:
            csv_file = open(csv_filename, "wb")
        sheet = workbook.sheet_by_name(sheetname)
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

        for rownumber in range(sheet.nrows):
            row = sheet.row_values(rownumber)
            for i in range(len(row)):
                if version_info[0] == 3:
                    str_obj = str
                else:
                    str_obj = basestring
                if isinstance(row[i], str_obj):
                    row[i] = str(u''.join([k if ord(k) < 128 else '' for k in row[i]]))
            writer.writerow(row)
        csv_file.close()
