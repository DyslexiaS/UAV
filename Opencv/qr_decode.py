from __future__ import print_function
import numpy as np
import zbar
from PIL import Image

def getQR(img_dir):
    scanner = zbar.ImageScanner()
    scanner.parse_config('enable')
    img = Image.open(img_dir).convert('L')
    width, height = img.size
    qrcode = zbar.Image(width, height, 'Y800', img.tobytes())
    scanner.scan(qrcode)
    data = ''
    for s in qrcode:
        data += s.data
    
    #del img
    print (data)


img_dir = raw_input('Image dir:')
getQR(img_dir)
