import zipfile
import shutil
from lex.scrape import*
from lex.excel_to_csv import*
if os.sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    from urllib import urlopen




def download_all_data(data_path,temp_path):
    print("Downloading Hospital_Revised_Flatfiles")
    print("\tDownloading...")
    flatlines=open(temp_path+"HRF.zip","wb")
    flatlines.write(urlopen("https://data.medicare.gov/views/bg9k-emty/files/ol-7qtOwDLXwyS6jR48-fPp00gIx-yUN96CT_DfQDZ4?filename=Hospital_Revised_Flatfiles.zip").read())
    flatlines.close()


    # Remove old files
    try:
        shutil.rmtree(data_path+"Hospital_Revised_Flatfiles")
    except:
        pass



    #Unpack zip file
    os.sys.stdout.write("\tUnpacking... 0\r")
    flatlines=open(temp_path+"HRF.zip","rb")
    ziplines=zipfile.ZipFile(flatlines)
    unzip_p=0
    unzip_max=len(ziplines.namelist())
    for name in ziplines.namelist():
        unzip_p+=1
        os.sys.stdout.write("\tUnpacking... "+str(unzip_p)+"\r")
        ziplines.extract(name,data_path+"Hospital_Revised_Flatfiles")
    flatlines.close()
    print("")
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
    print("\tScraping...")
    dartmouth_links=get_links_by_type(["xls","xlsx"],"http://www.dartmouthatlas.org/tools/downloads.aspx")

    download_links(dartmouth_links,temp_path+"Dartmouth_Files_TEMP")

    if not os.path.exists(data_path+"Dartmouth_Files"):
        os.makedirs(data_path+"Dartmouth_Files")

    print("\tConverting files...")
    for i in os.listdir(temp_path+"Dartmouth_Files_TEMP"):
        excel_to_csv(temp_path+"Dartmouth_Files_TEMP/"+i,data_path+"Dartmouth_Files/")

    # Cleaning up
    try:
        shutil.rmtree(temp_path+"Dartmouth_Files_TEMP")
    except:
        pass