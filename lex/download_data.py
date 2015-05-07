import zipfile
import shutil
from lex.scrape import*
from lex.excel_to_csv import*
if os.sys.version_info[0] == 3:
    from urllib.request import urlopen
    from urllib.error import URLError
else:
    from urllib2 import urlopen
    from urllib2 import URLError


def download_all_data(data_path, temp_path):
    # Make sure paths are in proper format
    if temp_path[-1] != "/":
        temp_path += "/"
    if data_path[-1] != "/":
        data_path += "/"

    # Remove old files
    try:
        shutil.rmtree(data_path)
    except (NameError, WindowsError):
        pass

    # Downloads
    print("Downloading Hospital_Revised_Flatfiles")
    print("\tDownloading...")
    flatlines = open(temp_path+"HRF.zip", "wb")
    try:
        flatlines.write(urlopen("https://data.medicare.gov/views/bg9k-emty/files/ol-7qtOwDLXwyS6jR48-"
                                "fPp00gIx-yUN96CT_DfQDZ4?filename=Hospital_Revised_Flatfiles.zip").read())
    except URLError:
        print("URLError.\nPlease check your network connection.")
        exit()
    flatlines.close()

    # Unpack zip file
    os.sys.stdout.write("\tUnpacking... 0\r")
    flatlines = open(temp_path+"HRF.zip", "rb")
    ziplines = zipfile.ZipFile(flatlines)
    unzip_p = 0
    for name in ziplines.namelist():
        unzip_p += 1
        os.sys.stdout.write("\tUnpacking... "+str(unzip_p)+"\r")
        ziplines.extract(name, data_path+"Hospital_Revised_Flatfiles")
    flatlines.close()
    print("")
    os.remove(temp_path+"HRF.zip")
    for i in os.listdir(data_path+"Hospital_Revised_Flatfiles"):
        if i[-3::] != "csv":
            print("\tRemoving non CSV ("+i+")")
            os.remove(data_path+"Hospital_Revised_Flatfiles/"+i)

    # Download Dartmouth Files
    print("Downloading Dartmouth Files")

    # Get and download links to TEMP
    print("\tScraping...")
    try:
        dartmouth_links = get_links_by_type(["xls", "xlsx"], "http://www.dartmouthatlas.org/tools/downloads.aspx")
        download_links(dartmouth_links, temp_path+"Dartmouth_Files_TEMP")
    except URLError:
        print("URLError.\nPlease check your network connection.")
        exit()

    # Convert files and place in new folder
    if not os.path.exists(data_path+"Dartmouth_Files"):
        os.makedirs(data_path+"Dartmouth_Files")
    os.sys.stdout.write("\tConverting files...\r")
    it = 0
    for i in os.listdir(temp_path+"Dartmouth_Files_TEMP"):
        it += 1
        excel_to_csv(temp_path+"Dartmouth_Files_TEMP/"+i, data_path+"Dartmouth_Files/")
        os.sys.stdout.write("\tConverting files... "+str(it)+"\r")
    print("")

    # Don't need to clean up. Medlex should do that from main