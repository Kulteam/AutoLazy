import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import os, time
import json
def Upload_to_DooStream(list_files,api_key):
    #list_results=[]
    extensions_video_file = ['.mp4','.flv','.h264','.avi','.mkv','.mpeg','.mpg','.mov','.m4v','.3gp','.wmv','.vob']
    list_path_video = [s for s in list_files if any(xs in s for xs in extensions_video_file)]
     
    # list all the files from a given path
    #files_to_upload = os.listdir(file_path)
    # tqdm is used as a context manager
    with tqdm(total=len(list_path_video), desc="Uploading", initial=0, unit_scale=True, colour='green') as bar:
        with ThreadPoolExecutor(max_workers=20) as executor:
            for path_video in list_path_video:
               
                with open((path_video), 'rb') as f:
                    files = {'file': (path_video, f.read())}
                
                    url=('https://doodapi.com/api/upload/server?key='+api_key)
                    r=requests.get(url).text
                    y = json.loads(r)
                    upload_url= (y["result"])
                    url=(upload_url+'?'+api_key)
                   
                    data = {
                    "api_key": api_key
                             }
                    futures = executor.submit(requests.post,
                                              url=url,data=data,files=files)
                    if as_completed(futures):
                        pbar.update(1)
                        time.sleep(0.02)
    #return list_results
Upload_to_DooStream(["D:\Project\AutoLazy\FC2-PPV-2539191\hhd800.com@FC2-PPV-2539191.mp4","D:\Project\AutoLazy\REBD-615\hhd800.com@REBD-615.mp4"],"83898e7z7wd2f0nv0jb60")
