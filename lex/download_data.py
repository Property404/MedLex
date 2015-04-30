import excel_to_csv
import scrape
import zipfile
import shutil
import os
if os.sys.version_info[0]==3:
    from urllib.request import urlopen
else:
    from urllib import urlopen


# Download Hospital_Revised_Flatlines
def download_all_data():
    print("Downloading Hospital_Revised_Flatfiles")
    flatlines=open("HRF.zip","wb")
    flatlines.write(urlopen("https://data.medicare.gov/views/bg9k-emty/files/ol-7qtOwDLXwyS6jR48-fPp00gIx-yUN96CT_DfQDZ4?filename=Hospital_Revised_Flatfiles.zip").read())
    flatlines.close()


    # Remove old files
    try:
        shutil.rmtree("./data/Hospital_Revised_Flatfiles")
    except:
        pass



    #Unpack zip file
    os.sys.stdout.write("\tUnpacking...")
    flatlines=open("HRF.zip","rb")
    ziplines=zipfile.ZipFile(flatlines)
    unzip_p=0
    for name in ziplines.namelist():
        unzip_p+=1
        os.sys.stdout.write(str(unzip_p)+"\r")
        ziplines.extract(name,"./data/Hospital_Revised_Flatfiles")
    flatlines.close()
    print("\n\tCleaning up...")
    os.remove("HRF.zip")
    for i in os.listdir("./data/Hospital_Revised_Flatfiles"):
        if i[-3::]!="csv":
            print("\tRemoving non CSV ("+i+")")
            os.remove("./data/Hospital_Revised_Flatfiles/"+i)


    # Download Dartmouth Files
    print("Downloading Dartmouth Files")

    try:
        shutil.rmtree("./data/Dartmouth_Files")
    except:
        pass
    print("\tScraping links")
    dartmouth_links=scrape.get_links_by_type(["xls","xlsx"],"http://www.dartmouthatlas.org/tools/downloads.aspx")

    print("\tDownloading links")
    scrape.download_links(dartmouth_links,"./Dartmouth_Files_TEMP")

    if not os.path.exists("./data/Dartmouth_Files"):
        os.makedirs("./data/Dartmouth_Files")

    print("\tConverting files to csv")
    for i in os.listdir("./Dartmouth_Files_TEMP"):
        excel_to_csv.excel_to_csv("./Dartmouth_Files_TEMP/"+i,"./data/Dartmouth_Files/")

    print("\tCleaning up...")
    try:
        shutil.rmtree("./Dartmouth_Files_TEMP")
    except:
        pass

if __name__=="__main__":
    download_all_data()