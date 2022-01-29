from clint.textui.progress import Bar as ProgressBar
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

import requests


def create_callback(encoder):
    encoder_len = encoder.len
    bar = ProgressBar(expected_size=encoder_len, filled_char='=')

    def callback(monitor):
        bar.show(monitor.bytes_read)

    return callback


def create_upload():
    return MultipartEncoder({
        'token': 'Su5O4wFHEiOQIA4wlu08CHnFakp6vv5Y',
        
        'file': ('2.mp4', open('2.mp4', 'rb'), 'video/mp4'),
       
                   
        })


if __name__ == '__main__':
    encoder = create_upload()
    callback = create_callback(encoder)
    monitor = MultipartEncoderMonitor(encoder, callback)
    r = requests.post('https://store2.gofile.io/uploadFile', data=monitor,
                      headers={'Content-Type': monitor.content_type})
    print('\nUpload finished! (Returned status {0} {1})'.format(
        r.status_code, r.reason
        ))

    
    
    
    
//////////////


from pathlib import Path
from tqdm import tqdm

import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

def upload_file(upload_url, fields, filepath):

    path = Path(filepath)
    total_size = path.stat().st_size
    filename = path.name

    with tqdm(
        desc=filename,
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        with open(filepath, "rb") as f:
            fields["file"] = (filepath, f)
            e = MultipartEncoder(fields=fields)
            m = MultipartEncoderMonitor(
                e, lambda monitor: bar.update(monitor.bytes_read - bar.n)
            )
            headers = {"Content-Type": m.content_type}
            requests.post(upload_url, data=m, headers=headers)


upload_url = 'https://jo283m.dood.video/upload/01?83898e7z7wd2f0nv0jb60'
fields = {
  "api_key": '83898e7z7wd2f0nv0jb60',
  #"field2": value2
}
filepath = 'hhd800.com@SIRO-4769.mp4'

upload_file(upload_url, fields, filepath)      
    
