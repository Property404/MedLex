import xlrd
import csv
from sys import version_info
import os.path


def excel_to_csv(excel_filepath, new_directory):
    # Make sure path names are in the right format
    if new_directory[-1] != '/':
        new_directory += '/'

    # Get filename from file path
    excel_filename = os.path.basename(excel_filepath)

    # Open workbook and begin converting each sheet to CSV file
    workbook = xlrd.open_workbook(excel_filepath)
    it = 0  # iteration control
    for sheetname in workbook.sheet_names():
        it += 1
        # Open new CSV file
        csv_filename = new_directory + excel_filename+"_sheet" + str(it) + '.csv'
        if version_info[0] >= 3:
            csv_file = open(csv_filename, "w", newline='')
        else:
            csv_file = open(csv_filename, "wb")
        # Write to CSV file
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
        # close CSV file
        csv_file.close()
