import webbrowser
from sys import version_info
if version_info[0] < 3:
    input = raw_input

DROPBOX_APP_KEY = 'jutrudkdtkkhosd'
DROPBOX_APP_SECRET = 'ny5ewhyu4djkpii'
DRIVE_APP_KEY = '717412404707-7ktghdcckmdig18u700oh8hkb6glggtq.apps.googleusercontent.com'
DRIVE_APP_SECRET = 'UjaHNJZMEZA09qP_nf1OQIlb'


def upload_to_dropbox(filename, new_filename, app_key=DROPBOX_APP_KEY, app_secret=DROPBOX_APP_SECRET):
    try:
        import dropbox
    except ImportError:
        print("Dropbox Python API not installed\nTry:\tpip install dropbox")
        exit()
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    authorize_url = flow.start()
    webbrowser.open(authorize_url)
    code = input("Enter DropBox authorization code>")
    try:
        access_token, user_id = flow.finish(code)
    except dropbox.rest.ErrorResponse:
        print("Invalid code for Dropbox")
        return False
    client = dropbox.client.DropboxClient(access_token)
    print('linked account: ', client.account_info()['display_name'])
    f = open(filename, 'rb')
    client.put_file('/'+new_filename, f)
    print("Uploaded "+filename+" to Dropbox")
    return True


def upload_to_drive(filename, new_filename, app_key=DRIVE_APP_KEY, app_secret=DRIVE_APP_SECRET):
    try:
        import httplib2
        from apiclient.discovery import build
        from apiclient.http import MediaFileUpload
        from oauth2client.client import OAuth2WebServerFlow
        from oauth2client.client import FlowExchangeError
    except ImportError:
        print("Google API Python Client not installed\nTry:\tpip install --upgrade google-api-python-client")
        exit()

    oauth_scope = 'https://www.googleapis.com/auth/drive'
    redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    
    flow = OAuth2WebServerFlow(app_key, app_secret, oauth_scope,
                               redirect_uri=redirect_uri)
    authorize_url = flow.step1_get_authorize_url()
    webbrowser.open(authorize_url)
    code = input("Enter Google Drive authorization code>")
    try:
        credentials = flow.step2_exchange(code)
    except FlowExchangeError:
        print("Invalid code for Google Drive")
        return False

    http = httplib2.Http()
    http = credentials.authorize(http)

    drive_service = build('drive', 'v2', http=http)

    media_body = MediaFileUpload(filename, mimetype='text/plain', resumable=True)
    body = {
        'title': new_filename,
        'description': 'Uploaded by MedLex',
        'mimeType': 'text/plain'
    }
    drive_service.files().insert(body=body, media_body=media_body).execute()
    print("Uploaded "+filename+" to Google Drive")
    return True


def upload_by_ftp(src, destination):
    from os.path import basename
    import ftplib

    # Get information from destination string
    while destination[0] == '/':
        destination = destination[1::]
    if "/" in destination:
        ftp_base = destination[0:destination.index('/')]
        ftp_rest = destination[destination.index('/')::]
        if "." in ftp_rest:
            ftp_path = ftp_rest[0:len(ftp_rest)-ftp_rest[::-1].index('/')]
            ftp_filename = ftp_rest[len(ftp_rest)-ftp_rest[::-1].index('/')::]
        else:
            ftp_path = ftp_rest
            ftp_filename = basename(src)
    else:
        ftp_base = destination
        ftp_path = "."
        ftp_filename = basename(src)

    # Start FTP session
    try:
        session = ftplib.FTP(ftp_base, input("Username>"), input("Password>"))
        session.cwd(ftp_path)
        srcfile = open(src, "rb")
        session.storbinary("STOR "+ftp_filename, srcfile)
    except ftplib.error_perm as e:
        print("File transfer failed: "+e.args[0])
        return False
    except (FileNotFoundError, PermissionError) as e:
        print("File transfer failed(client): "+e.args[1])
        return False
    srcfile.close()
    session.quit()
    print("File transfer successful")
    return True


def upload(src, destination):
    # Upload to Google Drive
    if len(destination) > len("drive.google:") and destination[0:len("drive.google:")] == "drive.google:":
        upload_to_drive(src, destination[len("drive.google:")::])
    # Upload to Dropbox
    elif len(destination) > len("dropbox:") and destination[0:len("dropbox:")] == "dropbox:":
        upload_to_dropbox(src, destination[len("dropbox:")::])
    # Upload to server by FTP
    elif len(destination) > len("ftp:") and destination[0:len("ftp:")] == "ftp:":
        upload_by_ftp(src, destination[len("ftp:")::])
    # Copy to local directory
    else:
        from shutil import copyfile
        copyfile(src, destination)
        print("File copied "+src+" to local destination")
