#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from distutils.errors import LinkError
from fileinput import filename
from genericpath import isfile
from shutil import which
import shutil
import subprocess
import urllib
from urllib.request import HTTPDefaultErrorHandler, urlopen ,urlretrieve
from urllib.parse import quote, urlparse,urlsplit, unquote
from requests.sessions import session   
import youtube_dl
from ntpath import join
from bs4 import BeautifulSoup
import requests
import re
import random
import time
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import json
from tqdm import tqdm 
from sys import exit
import sys
import posixpath
import os
import platform
import glob
from fsplit.filesplit import Filesplit
import cgi
import hashlib

from pathlib import Path
import libtorrent as torrent
from requests.exceptions import RequestException

#list_links=[]

#file = open("link.txt", "r")

#file_link = file.read()
def get_digest(file_path):
    h = hashlib.sha256()

    with open(file_path, 'rb') as file:
        while True:
            # Reading is buffered, so we can read smaller chunks.
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()


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
            buffer_size = 1024
# download the body of response by chunk, not immediately
            response = requests.get(link, stream=True)
            file_size = int(response.headers.get("Content-Length", 0))
          # get the default filename
            default_filename = link.split("/")[-1]
            # get the content disposition header
            content_disposition = response.headers.get("Content-Disposition")
            if content_disposition:
                value, params = cgi.parse_header(content_disposition)
            # extract filename from content disposition
                filename = params.get("filename", default_filename)
        
            # parse the header using cgi
            else:
                 filename = default_filename
       
           # if content dispotion is not available, just use default from URL
            progress = tqdm(response.iter_content(buffer_size), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "wb") as f:
                 for data in progress.iterable:
                     f.write(data)
                     # update the progress bar manually
                     progress.update(len(data)) 
    return filename
                    

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
             link=ydl.download(list_link)
             return link
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
                    
    
def Get_list_files_from_folder(path_folder,ext='.*'):
    list_files = []
    for file in glob.glob(path_folder+"/*"+ext):
        list_files.append(file)
    return(list_files)

def Upload_to_DooStream(path_file,api_key):
    def is_video_file(path_file):
        if os.path.isfile(path_file):
            file_extension = os.path.splitext(path_file)[1]
            if file_extension.lower() in {'.mp4','.flv','.h264','.avi','.mkv','.mpeg','.mpg','.mov','.m4v','.3gp','.wmv','.vob'}:
                return True
            return False
        return False
    
    
    fields = {
    "api_key": api_key,
  
    }
    
    if is_video_file(path_file)==True:
        if os.path.exists(path_file)==True:
            path = Path(path_file) 
            total_size = path.stat().st_size
            filename = path.name
      
            with tqdm(
              desc=filename,
              total=total_size,
              unit="B",
              unit_scale=True,
              unit_divisor=1024,
            ) as bar:
                with open(path_file, "rb") as f:
                   fields["file"] = (path_file, f)
                   e = MultipartEncoder(fields=fields)
                   m = MultipartEncoderMonitor(
                   e, lambda monitor: bar.update(monitor.bytes_read - bar.n)
                   )
                   headers = {"Content-Type": m.content_type}
                   url=('https://doodapi.com/api/upload/server?key='+api_key)
                   response=requests.get(url).text
                   server_upload = json.loads(response)["result"]
                   upload_url=(server_upload+'?'+api_key)
                   response=requests.post(upload_url, data=m, headers=headers)
                   return json.loads(response.text)["result"][0]["protected_embed"]
                
    return False

   
def Uploads_to_DooStream(list_files,api_key):
    list_results=[]
    fields = {
    "api_key": api_key,
  #"field2": value2
    }
    extensions_video_file = ['.mp4','.flv','.h264','.avi','.mkv','.mpeg','.mpg','.mov','.m4v','.3gp','.wmv','.vob']
    list_path_video = [s for s in list_files if any(xs in s for xs in extensions_video_file)]
    for path_video in list_path_video:
        path = Path(path_video)
        total_size = path.stat().st_size
        filename = path.name

        with tqdm(
             desc=filename,
             total=total_size,
             unit="B",
             unit_scale=True,
             unit_divisor=1024,
        ) as bar:
            with open(path_video, "rb") as f:
                fields["file"] = (path_video, f)
                e = MultipartEncoder(fields=fields)
                m = MultipartEncoderMonitor(
                    e, lambda monitor: bar.update(monitor.bytes_read - bar.n)
                )
                headers = {"Content-Type": m.content_type}
                url=('https://doodapi.com/api/upload/server?key='+api_key)
                response=requests.get(url).text
                server_upload = json.loads(response)["result"]
                upload_url=(server_upload+'?'+api_key)
                response=requests.post(upload_url, data=m, headers=headers)
                link_embed=json.loads(response.text)["result"][0]["protected_embed"]
                list_results.append(link_embed)
        
    return list_results
            
def Download_file_from_direct_link(url,path_folder=".",filename=None):
    if filename==None:
        local_filename = Get_filename_from_url(url)
    else:
        local_filename=filename    
        
    # NOTE the stream=True parameter
    
    if path_folder=="." :
      local_filename=path_folder+"/"+local_filename
    else :
        if os.path.isdir(path_folder)==True :
            local_filename= path_folder+"/"+local_filename   
        else :
            print("The specified path not an existing directory: "+path_folder)
            return False
    r = requests.get(url, stream=True)
    total_size_in_bytes= int(r.headers.get('content-length', 0))
    #block_size = 1024 #1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)    
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            progress_bar.update(len(chunk))
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    
    progress_bar.close()  
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
        print("Check the direct link again manually please.")
        return False
    return local_filename


def Get_FFMPEG(path_dir="./ffmpeg"):
    if platform.system()=='Windows':
                if os.path.exists(path_dir+"/ffmpeg.exe")==True:
                    return path_dir+"/ffmpeg.exe"
                else :    
                    os.makedirs(path_dir)
                    if os.path.exists(path_dir)!=True:
                      print("Cannot create folder to download FFMPEG \n Please check! ") 
                      return False
                    urls_file_ffmpeg=(["https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_1.exe?raw=true","https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_2.exe?raw=true","https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_3.exe?raw=true","https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_4.exe?raw=true","https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_5.exe?raw=true","https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_6.exe?raw=true","https://raw.githubusercontent.com/Kulteam/AutoLazy/main/ffmpeg/win/fs_manifest.csv"])
                    for path in urls_file_ffmpeg:
                         Download_file_from_direct_link(path,path_dir)
                    while get_digest(path_dir+"/ffmpeg_1.exe")!="a6bead48a441b829f384405e2fba1f210ccfd5360a5c5486ddfa4018b003f1f8":
                          Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_1.exe?raw=true",path_dir)
                    while get_digest(path_dir+"/ffmpeg_2.exe")!="4ea4fbb104a2aabab639e31b12e2a9b34f03b384137ecb523854e3fcc68d0cfd":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_2.exe?raw=true",path_dir)
                    while get_digest(path_dir+"/ffmpeg_3.exe")!="b07361114ec08a740159594cca0963e84d7b866460a63f4bfd9aa1ce5992aee6":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_3.exe?raw=true",path_dir)
                    while get_digest(path_dir+"/ffmpeg_4.exe")!="77f1a97b4d601c60de21dd213a7fd9f8b525ea93d610b9c69c352ff92e3d6c5d":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_4.exe?raw=true",path_dir)
                    while get_digest(path_dir+"/ffmpeg_5.exe")!="414847e555d5f8ece255440738e95acefc2ef6f2b4c1d3be2270c299014f7e81":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_5.exe?raw=true",path_dir)
                    while get_digest(path_dir+"/fs_manifest.csv")!="4db8a65d5442cd00465c40df1dcefc882f24473999e9961919473a9a89f3f59d":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/fs_manifest.csv?raw=true",path_dir)  
                    fs = Filesplit()
                    path_ffmpeg=path_dir+"/ffmpeg.exe"
                    fs.merge(path_dir,path_ffmpeg)
                    while get_digest(path_ffmpeg)!="5ee9f2d89fc5115839a1826f0cb06c52c0ce6bcd0ee76f6f822aa54d14670338":
                       print("Hash wrong \n Merge again ! ")
                       fs.merge(path_dir,path_ffmpeg)
                    cmd="set PATH %PATH%;"+path_dir
                    subprocess.run(cmd,shell=True) 
                    if shutil.which("ffmpeg")!=None:
                       print("Install FFMPEG on your Windows computer is successfully")
                       return path_ffmpeg
                    else:
                        print("Somthing wrong while try to install FFMPEG on your Windows computer")   
                        return False
                         
    if  platform.system()=='Linux':
                if os.path.exists(path_dir+"/ffmpeg")==True:
                    return path_dir+"/ffmpeg"
       
                else :
                   os.makedirs(path_dir)
                   if os.path.exists(path_dir)!=True:
                      print("Cannot create folder to download FFMPEG \n Please check! ") 
                      return False 
                   urls_file_ffmpeg=(["https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/linux/ffmpeg_1?raw=true","https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/linux/ffmpeg_2?raw=true","https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/linux/ffmpeg_3?raw=true","https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/linux/ffmpeg_4?raw=true","https://raw.githubusercontent.com/Kulteam/AutoLazy/main/ffmpeg/linux/fs_manifest.csv"])
                   for path in urls_file_ffmpeg:
                       Download_file_from_direct_link(path,path_dir)
                    
                   while get_digest(path_dir+"/ffmpeg_1")!="beb3b8b3aa72ef1088f8f6be16379177bad2a88801cadf76ed39672394d2198c":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/linux/ffmpeg_1?raw=true",path_dir)
                   while get_digest(path_dir+"/ffmpeg_2")!="0bd6504d35c6ab140e04d0e6c657efc0e1cc4ec05222a258a413a090076919d0":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/linux/ffmpeg_2?raw=true",path_dir)
                   while get_digest(path_dir+"/ffmpeg_3")!="8a365dbe28680de1c3b41b37fb7f6c1df2a980331638430d9e1a868f3f28b42f":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/linux/ffmpeg_3?raw=true",path_dir)
                   while get_digest(path_dir+"/ffmpeg_4")!="ee116f1b63d4d0ccd8aee0811627e5aae3f2bdb66da98854dd19606a411230d9":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/linux/ffmpeg_4?raw=true",path_dir)
                   while get_digest(path_dir+"/fs_manifest.csv")!="58627b1b80094a841630c95a8695a5c488421e42b0de4d9d2b9069c21f1f7be3":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/fs_manifest.csv?raw=true",path_dir)  
                   fs = Filesplit()
                   path_ffmpeg=path_dir+"/ffmpeg"
                   fs.merge(path_dir,path_ffmpeg)
                   while get_digest(path_ffmpeg)!="3ea58083710f63bf920b16c7d5d24ae081e7d731f57a656fed11af0410d4eb48":
                         print("Hash wrong \n Merge again ! ")
                         fs.merge(path_dir,path_ffmpeg)
                   
                   chmod="chmod +x "+path_ffmpeg      
                   subprocess.run(chmod,shell=True) 
                   if os.path.exists(path_ffmpeg)==True:
                       print("Install FFMPEG on your Linux computer is successfully")
                       return path_ffmpeg
                   else:
                        print("Somthing wrong while try to install FFMPEG on your Linux computer")  
                        return False  
    else:
        print("Your system computer not support by this Script \n System Support: \n -Windows \n -Linux ")
        return False
    
def Add_logo_to_video(path_input_video,path_logo,path_output="out_",option="5:5",path_ffmpeg="ffmpeg"):
    
    def run_ffmpeg(path_ffmpeg,path_input_video,path_logo):
        if path_output=="out_":
            path_output=(path_output+filename)
        else:
              
            if os.path.exists(path_output)==True:
       
                
                cmd =(path_ffmpeg+" -y -i '+path_input_video+' -i "+path_logo+" -filter_complex \"overlay="+option+"\""+" -codec:a copy "+path_output)
                subprocess.run(cmd,shell=True)
                
                    return Path(path_output)
                else :
                    return False                
        else:
                if os.path.isdir(path_output)==True:
                    folder_output=Path(path_output)
                    file_output=Path(path_input_video).name
                    path_output=os.path.join(folder_output,file_output)
                else:
                   # os.path.isfile(path_output)==True
                    path_output=path_output

                
                path_ffmpeg=path_ffmpeg
                cmd =(("{} -y -i '{}' -i {} -filter_complex \"overlay={}\" -codec:a copy '{}'").format(path_ffmpeg,path_input_video,path_logo,option,path_output))
                subprocess.run(cmd,shell=True)
                if os.path.exists(path_output)==True:
                    return Path(path_output)
                else :
                    return False
           
    path = Path(path_input_video)
    filename = path.name
    # Check path ffmpeg
    if path_ffmpeg=="ffmpeg":
        if shutil.which(path_ffmpeg)!=None:
            return run_ffmpeg(path_ffmpeg,path_input_video,path_logo)
           
        else:
            print("FFMPEG not install on your computer \n Down and install FFMPEG: ")
            path_ffmpeg=Get_FFMPEG()
            if path_ffmpeg!=False:
                return run_ffmpeg(path_ffmpeg,path_input_video,path_logo) 
            return False             
    else:
            path_ffmpeg=path_ffmpeg
            return run_ffmpeg(path_ffmpeg,path_input_video,path_logo)

def Add_logo_to_videos(list_path_input_or_folder_video,path_logo,folder_output=".",option="5:5",path_ffmpeg="ffmpeg"):

    def is_video_file(path_file):
        if os.path.isfile(path_file):
            file_extension = os.path.splitext(path_file)[1]
            if file_extension.lower() in {'.mp4','.flv','.h264','.avi','.mkv','.mpeg','.mpg','.mov','.m4v','.3gp','.wmv','.vob'}:
                return True
            return False
        return False
    list_result=[]   
    for path_file_or_folder in list_path_input_or_folder_video:
        if os.path.isdir(path_file_or_folder)==True:
            list_files=[os.path.join(path, name) for path, subdirs, files in os.walk(path_file_or_folder) for name in files]
            print(list_files)
            for path in list_files:
                if is_video_file(path)==True:
                    path=os.path.basename(path)
                    print(path)
                    video_path=(Add_logo_to_video(path,path_logo,path_output=folder_output))
                    list_result.append(video_path)
        else:
             if os.path.isfile(path_file_or_folder)==True:
                  if is_video_file(path_file_or_folder)==True:
                       list_result.append(Add_logo_to_video(path_file_or_folder,path_logo,path_output=folder_output))
           
    return list_result            




def Find_file_torrent_from_url(url):
    try:
       reqs = requests.get(url)
    except :
        return False
    soup = BeautifulSoup(reqs.text, 'html.parser')
    root_url = urlparse(url).scheme + '://' + urlparse(url).hostname
    for link in soup.find_all('a'):
        if link.get('href') is None:
            return False
        if link.get('href').endswith('.torrent')==True:
            if link.get('href').startswith('http')==True:
                return link.get('href')
               
            else:
                 return root_url+link.get('href')
    return False 
           
                
def Find_file_torrent_from_urls(list_url):
    list_urls_file=[]
    for url in list_url:
        torrent_url=Find_file_torrent_from_url(url)
        if torrent_url!=False:
            list_urls_file.append(torrent_url)
    if not list_urls_file:
        return False
    else:
        return list_urls_file      

def Get_basic_info_141JAV(url_141jav_com,path_logo,api_key):
    def Get_emble_url_video(torrent_url):
        torrent_file=Download_file_from_TorrentFile(torrent_url)
        video_with_logo=Add_logo_to_video(torrent_file,path_logo)
        return Upload_to_DooStream(video_with_logo,api_key)


    try:
            page = requests.get(url_141jav_com)
            soup = BeautifulSoup(page.content, 'html.parser')
            video_code=soup.find('title').string.replace(" - 141JAV.com - Free JAV Torrents","")
            video_title = soup.find('p', class_="level has-text-grey-dark").string.replace("\n","")
            video_image=soup.find_all(class_="image")[0]['src']
            video_tag=soup.find_all('a',class_="tag is-light")
            video_tags=[]
            for tag in video_tag:
               video_tags.append(tag.string.replace("\n",""))
            actors=soup.find_all('a',class_="panel-block")
            actress=[] 
            for actress_idol in actors:
              actress.append(actress_idol.string.replace("\n",""))
            url_torrent=Find_file_torrent_from_url(url_141jav_com)
            
    except:
        print("Somthing wrong while get infomation from 141jav.com \n Please check again ")
        return False    
    return {"video_title":video_title,"video_code":video_code,"actress":actress,"video_image":video_image,"video_tags":video_tags,"video_torrent_file":url_torrent,"embed_link":Get_emble_url_video(url_torrent)}







def Get_info_video_141JAV(url):
    if Find_file_torrent_from_url(url)!=False:
        pass


                                                    
print("Get link from links.txt \n Please wait..")

link=Add_logo_to_videos(".","logo-s.png","./Out/")
print(link)
