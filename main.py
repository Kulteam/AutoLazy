#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from urllib.request import urlopen 
from urllib.parse import quote   
import youtube_dl
from ntpath import join
from bs4 import BeautifulSoup
import requests
import re
import random
import wget
import time
import urllib
from urllib.request import urlretrieve
import json
from tqdm import tqdm
from sys import exit
import sys
import posixpath
import os
import locale
os.environ["PYTHONIOENCODING"] = "utf-8"
scriptLocale=locale.setlocale(category=locale.LC_ALL, locale="en_GB.UTF-8")

try:
    from urlparse import urlsplit
    from urllib import unquote
except ImportError: # Python 3
    from urllib.parse import urlsplit, unquote


#list_links=[]

#file = open("link.txt", "r")

#file_link = file.read()

def Get_url_from_file(filename):
    file =open(filename)
    file_link = file.read()
    # findall() has been used 
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,file_link)      
    return [x[0] for x in url]
      


def Get_link_anonfiles_bayfiles(list_link):
     r=re.compile("^https?://(anonfiles.com|bayfiles.com)")
     list_link_anonfiles = list(filter(r.match,list_link))
     return list_link_anonfiles

def Get_link_SolidFiles(list_link):
     r=re.compile("^https?:\/\/(www.)*solidfiles.com/v/")
     
     list_link_SolidFiles = list(filter(r.match,list_link))
     return list_link_SolidFiles

def Get_link_mediaFire(list_link):
     regex="^https?://(www.)*mediafire.com/file/"    
     r=re.compile(regex)
     list_link_mediaFire = list(filter(r.match,list_link))
     return list_link_mediaFire
 
def Get_magnet_link(list_link):
     regex="magnet:\?xt=urn:btih:[a-zA-Z0-9]*"
     r=re.compile(regex)
     list_magnet_link = list(filter(r.match,list_link))
    
     return list_magnet_link
 
def Get_link_onedriver(list_link):
    regex="^https?://1drv.ms(/x/|/v/|/w/|/p/|/t/)|^https?://onedrive.live.com/(\?cid|embed\?|view.aspx|\?authkey)"
    r=re.compile(regex)
    list_link_onedriver = list(filter(r.match,list_link))
    return list_link_onedriver
    
     
 
def Get_link_support_by_youtube_dl(list_link):
     youtube="(^https?:\/\/(www.)*youtube.com)(\/watch\?|\/channel/|\/feed\/explore|\/channels|\/c\/|\/user\/)|(https://youtu.be/)"
     pornhub="((^https?:\/\/(www.)*pornhub.com)(\/model\/|\/view_video|\/video|\/pornstar|\/channels|\/users|\/playlist|\/albums|\/recommended|\/explore))"
     facebook="^https?://(www.)*facebook.com/(watch|[a-zA-Z0-9]*/videos/)"
     bilibili="^https?:\/\/(www.)*bilibili.com(/video/|/[a-zA-Z0-9]*/play/)"
     google_driver="^https?://drive.google.com/file/"
     regex="|".join([youtube,pornhub,facebook,bilibili,google_driver])
     r=re.compile(regex)
     link_support_by_youtube_dl = list(filter(r.match,list_link))
     return link_support_by_youtube_dl
           

def Download_from_anonfiles_bayfiles(list_link):
    for link in list_link:  
        req = requests.get(link)
        soup = BeautifulSoup(req.text, "html.parser")
        #print(soup.title)
        for url in soup.findAll('a', attrs={'href': re.compile("^https://cdn-")}):
            link_direct = (url.get('href'))
            #print(link_direct)
            print("Download file of link: "+link)
            filename=Download_file_from_direct_link(link_direct)
            print("Done download filename: "+filename)
            sleep_time=random.randint(1,5)
            print("Pause until next download for %s s" %sleep_time )
            time.sleep(sleep_time)

def Download_from_mediaFire(list_link):
    for link in list_link:  
        req = requests.get(link)
        soup = BeautifulSoup(req.text, "html.parser")
       # print(soup.title)
        for url in soup.findAll('a', attrs={'href': re.compile("^https?://download")}):
            link_direct = (url.get('href'))
            #print(link_direct)
            print("Download file of link: "+link)
            filename=Download_file_from_direct_link(link_direct)
            #filename=wget.download(link_direct)
            print("Done download filename: "+filename)
            sleep_time=random.randint(1,5)
            print("Pause until next download for %s s" %sleep_time )
            time.sleep(sleep_time)            
    
def Get_direct_link_SolidFiles(url):
     headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
        }
     pageSource = requests.get(url, headers = headers).text
     if 'Page not found | SolidFiles' in pageSource:
         print("Link die: "+url)
         print("Check the URL again manually please.")
         exit(0)
                
     else:
          mainOptions = str(re.search(r'viewerOptions\'\,\ (.*?)\)\;', pageSource).group(1))
          jsonString = json.loads(mainOptions)
          downloadUrl = jsonString["downloadUrl"]
          nodeName = jsonString["nodeName"]
          filetype = jsonString["filetype"]
          return(downloadUrl)



def Get_direct_link_onedriver(list_link):
    new_list=[]  
    for link in list_link:
        if 'http://1drv.ms' in link:
            new_url=urllib.request.urlopen(link)
            new_list.append(new_url.url) 
    for link in list_link:
        if 'https://1drv.ms' in link:
            new_url=urllib.request.urlopen(link)
            new_list.append(new_url.url)             
    
    for link in list_link:
        if re.match(r'^https?://onedrive.live.com/(redir\?|embed\?|view.aspx)', link):
            new_list.append(link)
    return new_list
            

def Download_from_OneDriver(list_link):
    list_link_onedriver=Get_direct_link_onedriver(list_link)
    direct_links = list(map(lambda item: item.replace("redir","download"), list_link_onedriver))
    direct_links = list(map(lambda item: item.replace("view.aspx","download.aspx"), direct_links))
    direct_links = list(map(lambda item: item.replace("embed","download"), direct_links))
    for link in direct_links:
        print("Download file of link: "+link)
        filename=Download_file_from_direct_link(link)
        #filename=wget.download(link)
        print("Done download filename: "+filename)
        sleep_time=random.randint(1,5)
        print("Pause until next download for %s s" %sleep_time )
        time.sleep(sleep_time)     
       
def Download_from_SolidFiles(list_link):
    for link in list_link:
        direct_link=Get_direct_link_SolidFiles(link)
        print("Download file of link: "+link)
        filename=Download_file_from_direct_link(direct_link)
        print("Done download filename: "+filename)
        sleep_time=random.randint(1,5)
        print("Pause until next download for %s s" %sleep_time )
        time.sleep(sleep_time)
        
def Download_url_support_by_youtube_dl(list_link):
    try:
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
             ydl.download(list_link)
    except youtube_dl.DownloadError:
        print("Youtube-dl only support download videos \n Please manually download or try other way If you want download other type file \n" 
              "Host support by this script: \n-Youtube (Only Video)\n-Facebook (Only Video) \n-BiliBili (Only Video)\n-PornHub (Only Video)\n-AnonFiles\n-BayFiles"
              "\n-mediaFire\n-SolidFiles")   
               
def Get_url_from_string(string):
     regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))|(magnet:\?xt=urn:btih:[a-zA-Z0-9]*)"
     url = re.findall(regex,string)      
     return [x[0] for x in url]
            

def Get_filename_from_url(url):
    urlpath = urlsplit(url).path
    basename = posixpath.basename(unquote(urlpath))
    if (os.path.basename(basename) != basename or
        unquote(posixpath.basename(urlpath)) != basename):
        raise ValueError
    return basename  
                
def Download_file_from_direct_link(url):
    response = requests.get(url, stream=True)
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 1024 #1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    filename=Get_filename_from_url(url)
    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
            
    
        
    progress_bar.close()
    
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
        print("Check the direct link again manually please.")
    return filename    

print("Get link from links.txt \n Please wait..")
list_link = Get_url_from_file("links.txt")
link_driver=Get_link_onedriver(list_link)
Download_from_OneDriver(link_driver)
link_ano=Get_link_anonfiles_bayfiles(list_link)
Download_from_anonfiles_bayfiles(link_ano)
link_solid=Get_link_SolidFiles(list_link)
Download_from_SolidFiles(link_solid)




