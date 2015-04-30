import zipfile
import shutil
import os
import bs4
import xlrd
import csv
if os.sys.version_info[0] == 3:
    from urllib.request import urlopen
    from urllib.parse import urljoin
else:
    from urllib import urlopen
    from urlparse import urljoin



def excel_to_csv(excel_path,new_directory):
    if new_directory[-1]!='/':
        new_directory+='/'
    excel_filename=excel_path
    while "/" in excel_filename:
        excel_filename=excel_filename[excel_path.index("/")+1::]
    workbook=xlrd.open_workbook(excel_path)
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
                if os.sys.version_info[0]==3:
                    str_obj=str
                else:
                    str_obj=basestring
                if isinstance(row[i],str_obj):
                    row[i]=str(u''.join([k if ord(k)<128 else '' for k in row[i]]))
            try:
                writer.writerow(row)
            except:
                print(row)
        csv_file.close()


def get_links_by_type(types,url):
    # Correct arguments
    links=[]
    if isinstance(types,str):
        types=[types]
    for i in range(len(types)):
        types[i]=types[i].lower()

    # Read page
    soup=bs4.BeautifulSoup((urlopen(url)).read())

    # Get links of certain filetypes
    for linktag in soup.findAll("a"):
        href=linktag.get("href")
        # Check if it has the right file type
        if href is None or "." not in href:
            continue
        file_ending=href[(len(href)-href[::-1].index("."))::]
        if file_ending.lower() in types:
            # Append if local link
            if href[0]=="/":
                href=urljoin(url,href)
            links.append(href)

    # Return links
    return links


def download_links(links,directory):
    if directory[-1]!="/":
        directory+="/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    count=0
    for href in links:
        filename=href[(len(href)-href[::-1].index("/"))::]
        file=open(directory+filename,"wb")
        file.write(urlopen(href).read())
        file.close()
        count+=1
        if count>5:
            break
        os.sys.stdout.write("Downloading... "+str((100*count//(len(links))))+"%\r")
    print("")


def download_all_data(data_path,temp_path):
    print("Downloading Hospital_Revised_Flatfiles")
    flatlines=open(temp_path+"HRF.zip","wb")
    flatlines.write(urlopen("https://data.medicare.gov/views/bg9k-emty/files/ol-7qtOwDLXwyS6jR48-fPp00gIx-yUN96CT_DfQDZ4?filename=Hospital_Revised_Flatfiles.zip").read())
    flatlines.close()


    # Remove old files
    try:
        shutil.rmtree(data_path+"Hospital_Revised_Flatfiles")
    except:
        pass



    #Unpack zip file
    os.sys.stdout.write("\tUnpacking...")
    flatlines=open(temp_path+"HRF.zip","rb")
    ziplines=zipfile.ZipFile(flatlines)
    unzip_p=0
    for name in ziplines.namelist():
        unzip_p+=1
        os.sys.stdout.write(str(unzip_p)+"\r")
        ziplines.extract(name,data_path+"Hospital_Revised_Flatfiles")
    flatlines.close()
    print("\n\tCleaning up...")
    os.remove(temp_path+"HRF.zip")
    for i in os.listdir(data_path+"Hospital_Revised_Flatfiles"):
        if i[-3::]!="csv":
            print("\tRemoving non CSV ("+i+")")
            os.remove(data_path+"Hospital_Revised_Flatfiles/"+i)


    # Download Dartmouth Files
    print("Downloading Dartmouth Files")

    try:
        shutil.rmtree(data_path+"Dartmouth_Files")
    except:
        pass
    print("\tScraping links")
    dartmouth_links=get_links_by_type(["xls","xlsx"],"http://www.dartmouthatlas.org/tools/downloads.aspx")

    print("\tDownloading links")
    download_links(dartmouth_links,temp_path+"Dartmouth_Files_TEMP")

    if not os.path.exists(data_path+"Dartmouth_Files"):
        os.makedirs(data_path+"Dartmouth_Files")

    print("\tConverting files to csv")
    for i in os.listdir(temp_path+"Dartmouth_Files_TEMP"):
        excel_to_csv(temp_path+"Dartmouth_Files_TEMP/"+i,data_path+"Dartmouth_Files/")

    print("\tCleaning up...")
    try:
        shutil.rmtree(temp_path+"Dartmouth_Files_TEMP")
    except:
        pass

if __name__=="__main__":
    download_all_data()