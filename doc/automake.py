from sys import version_info
if version_info[0] < 3:
    input = raw_input


def upload_by_ftp(src, destination, password):
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
        print(ftp_base)
        session = ftplib.FTP(ftp_base, "a6077027", password)
        session.cwd(ftp_path)
        srcfile = open(src, "rb")
        session.storbinary("STOR "+ftp_filename, srcfile)
    except ftplib.error_perm as e:
        print("File transfer failed: "+e.args[0])
        return False
    srcfile.close()
    session.quit()
    print("File transfer successful")
    return True

style_link = '<link rel="stylesheet" href="/ibm.css" />'

usage_text = open("Usage Documentation.html", "r").read().replace("</title>", "</title>\n    "+style_link+"")
example_formatted_text = open("MedLex Example.html", "r").read()
example_plain_text = "<pre>"+open("MedLex Example.txt", "r").read()+"\n</pre>"
index_text = """<!DOCTYPE html>
<html>
    <head>
        <title>MedLex</title>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="/ibm.css" />
        <style type="text/css">
            body{
                text-align: center;
            }
        </style>
    </head>
    <body>
        <h1>MedLex</h1>
        A tool designed to take in CSV data and create a lexicon<br>
        <br>
        <iframe width="640" height="372" style="background: #000;" src="https://www.youtube.com/embed/F8xS0XtO-eE?rel=0&amp;controls=0&amp;showinfo=0&amp;modestbranding=1" frameborder="1" allowfullscreen></iframe>
        <br><br>
        <a href="usage.html">Usage Documentation</a><br>
        <a href="plaintext_example.html">Plaintext Lexicon Example</a><br>
        <a href="html_example.html">Formatted Lexicon Example</a><br>
        <a href="https://github.com/Property404/MedLex">Source Code</a><br>

        <p>Information:
        <p>MedLex has three basic functions: Download databases, create lexicons from those databases, and upload the lexicons<br/>
        to various computers. With MedLex, the user is able to do all of this from a single command:<br>
        <code>medlex -dr lexicon.txt -u lexicon.txt ftp://server1.net;ftp://server2.net</code><br>
        Of course, MedLex has addition features, such as allowing the user to create a custom lexicon from a custom data<br>
        data source, creating HTML-formatted lexicons, finding word definitions from an online dictionary, and more. You can<br/>
        read more about this in the usage documentation.

        <p>MedLex uses an 4500-word long vocabulary list to ignore basic (i.e. non-specialized) words when making lexicons.<br>
        Most of the words in the list came from parsing online lists of the most common words in the English language into a<br>
        Python list format. Other means, such as taking the English list from the
        <a href="https://pypi.python.org/pypi/stop-words">stop-words</a> python module, were also used.<br>
        Contributers: Dagan Martinez, William Lees

        <p>MedLex uses <a href='http://www.nltk.org/'>NLTK</a>(natural language tool kit) for identifying which words to associate as equivilant. This<br>
        works by finding the root of a word, and checking if any other word from the source data has the same root.<br>
        Initially, MedLex could only associate words based on how many letters they shared, which proved a very poor<br>
        algorithm.

        <p>When running speed test (with '<code>medlex.py -r</code>'), MedLex performed much faster on UNIX and UNIX-like systems than<br>
        on Windows, even when using older hardware. This could be due to the way UNIX handles file input/output.

        <p>MedLex was programmed by Dagan Martinez, and is free and open source under the
        <a href="http://www.gnu.org/licenses/gpl-3.0.en.html#content">GNU General Public License.</a><br>

    </body>
</html>
"""

local_dir = "C:\\xampp\\htdocs\\medlex\\"
server_dir = "daganmartinez.com/public_html/MedLex/"
open(local_dir+"index.html", "w").write(index_text)
open(local_dir+"usage.html", "w").write(usage_text)
open(local_dir+"html_example.html", "w").write(example_formatted_text)
open(local_dir+"plaintext_example.html", "w").write(example_plain_text)

import getpass
password = getpass.getpass("pass> ")

for fname in ["index.html", "usage.html", "html_example.html", "plaintext_example.html"]:
    upload_by_ftp(local_dir+fname, server_dir+fname, password)