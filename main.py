#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from fileinput import filename
from urllib.request import urlopen 
from urllib.parse import quote
from requests.sessions import session   
import youtube_dl
from ntpath import join
from bs4 import BeautifulSoup
import requests
import re
import random
import time
import urllib
from urllib.request import urlretrieve
import json
from tqdm import tqdm
from sys import exit
import sys
import posixpath
import os
import glob

from pathlib import Path
import libtorrent as torrent
from requests.exceptions import RequestException


try:
    from urlparse import urlsplit
    from urllib import unquote
except ImportError: # Python 3
    from urllib.parse import urlsplit, unquote


#list_links=[]

#file = open("link.txt", "r")

#file_link = file.read()

def Get_urls_from_local_file(filename):
    file =open(filename)
    file_link = file.read()
    # findall() has been used 
    # with valid conditions for urls in string
    url = "([\w+]+\:\/\/)?([\w\d-]+\.)*[\w-]+[\.\:]\w+([\/\?\=\&\#.]?[\w-]+)*\/?"
    magnet = "magnet:\?xt=urn:btih:[a-zA-Z0-9]*"
    regex=f"({url}|{magnet})"
    urls = re.findall(regex,file_link)      
    return urls
#[x[0] for x in urls]

def Get_urls_from_string(string):
    url = "([\w+]+\:\/\/)?([\w\d-]+\.)*[\w-]+[\.\:]\w+([\/\?\=\&\#.]?[\w-]+)*\/?"
    magnet = "magnet:\?xt=urn:btih:[a-zA-Z0-9]*"
    regex=f"({magnet}|{url})"
    urls = re.findall(regex,string)      
    return [x[0] for x in urls]
 
def Get_urls_from_remote_file(url):
    file_link = requests.get(url).text
    # with valid conditions for urls in string
    url = "([\w+]+\:\/\/)?([\w\d-]+\.)*[\w-]+[\.\:]\w+([\/\?\=\&\#.]?[\w-]+)*\/?"
    magnet = "magnet:\?xt=urn:btih:[a-zA-Z0-9]*"
    regex=f"({magnet}|{url})"
    urls = re.findall(regex,file_link)      
    return [x[0] for x in urls] 
      


def Get_link_anonfiles(list_link):
     r=re.compile("^https?://anonfiles.com")
     list_link_anonfiles = list(filter(r.match,list_link))
     return list_link_anonfiles
 
def Get_link_bayfiles(list_link):
     r=re.compile("^https?://bayfiles.com")
     list_link_bayfiles = list(filter(r.match,list_link))
     return list_link_bayfiles 

def Get_link_SiaSky(list_link):
     r=re.compile("^https?://siasky.net")
     list_link_siasky = list(filter(r.match,list_link))
     return list_link_siasky

def Get_link_SolidFiles(list_link):
     r=re.compile("^https?:\/\/(www.)*solidfiles.com/v/")
     
     list_link_SolidFiles = list(filter(r.match,list_link))
     return list_link_SolidFiles

def Get_link_mediaFire(list_link):
     regex="^https?://(www.)*mediafire.com/file/"    
     r=re.compile(regex)
     list_link_mediaFire = list(filter(r.match,list_link))
     return list_link_mediaFire
 
def Get_link_torrent(list_link):
     regex="magnet:\?xt=urn:btih:[a-zA-Z0-9]*|https?:\/\/[^\s]+\.torrent"
     r=re.compile(regex)
     list_link_torrent = list(filter(r.match,list_link))
    
     return list_link_torrent
 
def Get_link_onedriver(list_link):
    regex="^https?://1drv.ms(/x/|/v/|/w/|/p/|/t/)|^https?://onedrive.live.com/(\?cid|embed\?|view.aspx|\?authkey)"
    r=re.compile(regex)
    list_link_onedriver = list(filter(r.match,list_link))
    return list_link_onedriver
    
     
 
def Get_link_support_by_youtube_dl(list_link):
     youtube="^https?:\/\/(www.)*youtube.com(\/watch\?|\/channel/|\/feed\/explore|\/channels|\/c\/|\/user\/)|(https?://youtu.be/)"
     pornhub="^https?:\/\/(www.)*pornhub.com(\/model\/|\/view_video|\/video|\/pornstar|\/channels|\/users|\/playlist|\/albums|\/recommended|\/explore)"
     facebook="^https?:\/\/(www.)*facebook.com/(watch|[a-zA-Z0-9]*/videos/)"
     bilibili="^https?:\/\/(www.)*bilibili.com(/video/|/[a-zA-Z0-9]*/play/)"
     google_driver="^https?://drive.google.com/file/"
     regex="|".join([youtube,pornhub,facebook,bilibili,google_driver])
     r=re.compile(regex)
     link_support_by_youtube_dl = list(filter(r.match,list_link))
     return link_support_by_youtube_dl
           

def Download_from_anonfiles(list_link):
    for link in list_link:  
        req = requests.get(link)
        soup = BeautifulSoup(req.text, "html.parser")
        #print(soup.title)
        for url in soup.findAll('a', attrs={'href': re.compile("^https://cdn-")}):
            link_direct = (url.get('href'))
            print("Download file of link: "+link)
            filename=Download_file_from_direct_link(link_direct)
            print("Done download filename: "+filename)
            sleep_time=random.randint(1,5)
            print("Pause until next download for %s s" %sleep_time )
            time.sleep(sleep_time)

def Download_from_bayfiles(list_link):
    for link in list_link:  
        req = requests.get(link)
        soup = BeautifulSoup(req.text, "html.parser")
    
        for url in soup.findAll('a', attrs={'href': re.compile("^https://cdn-")}):
            link_direct = (url.get('href'))
            print("Download file of link: "+link)
            filename=Download_file_from_direct_link(link_direct)
            print("Done download filename: "+filename)
            sleep_time=random.randint(1,5)
            print("Pause until next download for %s s" %sleep_time )
            time.sleep(sleep_time)

def Download_from_SiaSky(list_link):
    for link in list_link:
            print("Download file of link: "+link)
            filename=Download_file_from_direct_link(link)
            print("Done download filename: "+filename)
            sleep_time=random.randint(1,5)
            print("Pause until next download for %s s" %sleep_time )
            time.sleep(sleep_time)
         
            

def Download_from_mediaFire(list_link,path_folder="."):
    list_file=[]
    list_path_file=[]
    for link in list_link:  
        req = requests.get(link)
        soup = BeautifulSoup(req.text, "html.parser")
       # print(soup.title)
        for url in soup.findAll('a', attrs={'href': re.compile("^https?://download")}):
            link_direct = (url.get('href'))
            
            print("Download file of link: "+link)
            filename=Download_file_from_direct_link(link_direct)
            print("Done download filename: "+filename)
            list_file.append(filename)
            sleep_time=random.randint(1,5)
            print("Pause until next download for %s s" %sleep_time )
            time.sleep(sleep_time)   
            
    for file in list_file:
        new_path=path_folder+'/'+file
        print(new_path)
        try:
            Path(file).rename(new_path)
            list_path_file.append(new_path)
        except :
            print("The system cannot find the file specified: "+file+"->"+new_path)
            
                     
    return list_path_file   

    

     
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

def Download_file_from_MagnetLink(url,path_folder="."):
    session = torrent.session()
    session.listen_on(6881, 6891)
    params = {   
        'save_path': path_folder,
        'storage_mode': torrent.storage_mode_t(2),
       #'paused': False,
       #'auto_managed': True,
       #'duplicate_is_error': True
    
    }
    link = url
    handle = torrent.add_magnet_uri(session, link, params)
    session.start_dht()
    print ('Downloading Metadata...')
    while (not handle.has_metadata()):
        time.sleep(1)
    print ('Got metadata, starting torrent download...')
    while (handle.status().state != torrent.torrent_status.seeding):
        s = handle.status()
        state_str = ['queued', 'checking', 'downloading metadata', \
            'downloading', 'finished', 'seeding', 'allocating']
        print ('%.2f%% Complete (Down: %.1f kb/s Up: %.1f kB/s Peers: %d) %s' % \
            (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
            s.num_peers, state_str[s.state]))  
        time.sleep(5)      
    print(handle.status().name, 'Complete')
    path=(path_folder+'/'+handle.status().name)
    try:
        list_path_file=Get_list_files_from_folder(path,".mp4")
    except :
        print("Cannot get list files from folder.Something is wrong, please check ! ")
        
    return list_path_file
    

def Download_file_from_TorrentFile(url,path_folder="."):
    
    filetorrent=Download_file_from_direct_link(url)
    ses = torrent.session({'listen_interfaces': '0.0.0.0:6881'})

    info = torrent.torrent_info(filetorrent)
    h = ses.add_torrent({'ti': info, 'save_path': path_folder})
    s = h.status()
    print('starting', s.name)

    while (not s.is_seeding):
        s = h.status()
        print('\r%.2f%% Complete (Down: %.1f kB/s Up: %.1f kB/s Peers: %d) %s' % (
            s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
            s.num_peers, s.state), end=' ')
        alerts = ses.pop_alerts()
        for a in alerts:
             if a.category() & torrent.alert.category_t.error_notification:
                  print(a)
           
        sys.stdout.flush()
        time.sleep(1)
    print(h.status().name, 'Complete')
    path=(path_folder+'/'+h.status().name)
    try:
        path_file=Get_list_files_from_folder(path,".mp4")
    except :
        print("Cannot get list files from folder.Something is wrong, please check ! ")
        
    return path_file
    


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


def Download_from_Torrent(list_link,path_folder="."):
    for link in list_link:
         if 'http' in link :
             try:
                Path_file=Download_file_from_TorrentFile(link,path_folder)
                return Path_file
             except:
                print("Your url: "+link+" is not support \n Please check! ")
              
         elif 'magnet' in link:
             try:
                Path_file= Download_file_from_MagnetLink(link,path_folder)
                return Path_file
             except:
                print("Your url: "+link+" is not support \n Please check! ")
            

def Get_filename_from_url(url):
    try:
        with requests.get(url) as r:
            filename = ''
        if "Content-Disposition" in r.headers.keys():
            filename = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0]
            filename=filename.replace('"', '')
        else:
            urlpath = urlsplit(url).path
            filename = posixpath.basename(unquote(urlpath))
            if (os.path.basename(filename) != filename or
                unquote(posixpath.basename(urlpath)) != filename):
                raise ValueError
            return filename
            
        return filename
    except RequestException as error:
        print(error)
                    
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
    
def Get_list_files_from_folder(path_folder,ext):
    list_files = []
    for file in glob.glob(path_folder+"/*"+ext):
        list_files.append(file)
    return(list_files)
    
def Upload_to_DooStream(list_files,api_key):
    list_results=[]
    extensions_video_file = ['.mp4','.flv','.h264','.avi','.mkv','.mpeg','.mpg','.mov','.m4v','.3gp','.wmv','.vob']
    list_path_video = [s for s in list_files if any(xs in s for xs in extensions_video_file)]
    for path_video in list_path_video:
        url=('https://doodapi.com/api/upload/server?key='+api_key)
        r=requests.get(url).text
        y = json.loads(r)
        upload_url= (y["result"])
        data = {
        "api_key": api_key
        }
        files = {
        "file": (path_video, open(path_video, 'rb')),
        }
        url=(upload_url+'?'+api_key)
        response = requests.post(url, data=data,  files=files)
        result=json.loads(response.text)
        
        print(result["result"])
        list_results.append(result["result"])
    return list_results

print("Get link from links.txt \n Please wait..")
#list_link = Get_urls_from_local_file("links.txt")
#print(list_link)
#link_driver=Get_link_onedriver(list_link)
#Download_from_OneDriver(link_driver)
#link_ano=Get_link_anonfiles_bayfiles(link)
#Download_from_anonfiles_bayfiles(link_ano)
#link_solid=Get_link_SolidFiles(list_link)
#Download_from_SolidFiles(link_solid)
#link_torrent=Get_link_torrent(list_link)
#print(link_torrent)
#Download_from_Torrent(link_torrent)
#link_media=Get_link_mediaFire(list_link)
#print(link_media)
#Download_from_mediaFire(link_media)
#link_youtube_dl=Get_link_support_by_youtube_dl(link)
#Download_url_support_by_youtube_dl(link_youtube_dl)


path_video=Upload_to_DooStream(["D:\Data\Public\Video\\61 comments.mp4","D:\Data\Public\Video\Coming Soon - HYIP.NET Chuyên trang đầu tư tài chính HYIP,MLM và Economic game...mp4"],"83898e7z7wd2f0nv0jb60")
print(path_video)
