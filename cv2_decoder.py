import base64
import lzma
import numpy as np
import cv2
import json
from pyzbar.pyzbar import decode
import ast

qcd = cv2.QRCodeDetector()
cap = cv2.VideoCapture("output.mp4")

base64_data = [None] * 50
seq_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    seq_count += 1
    if ret:
        ret, info, points, _ = qcd.detectAndDecodeMulti(frame)
        print(f"ret {ret}, {repr(info)}")
        if ret:
            if len(info) > 2:
                print(seq_count)
                print(info)

    else:
        break

cap.release()

print(repr(base64_data))

encoded_data = ''.join(base64_data[:seq_count])
com_data = base64.b64decode(encoded_data)
dec_data = lzma.decompress(com_data)

with open("output.pdf", "wb") as bin_file:
    bin_file.write(dec_data)

