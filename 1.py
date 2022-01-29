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
