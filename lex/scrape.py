#!/usr/bin/env python
# Copyright (c) - 2015 Dagan Martinez
import os
import bs4

if os.sys.version_info[0] == 3:
    from urllib.request import urlopen
    from urllib.parse import urljoin
else:
    from urllib import urlopen
    from urlparse import urljoin


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
        os.sys.stdout.write("\tDownloading... "+str((100*count//(len(links))))+"%\r")
    print("")
