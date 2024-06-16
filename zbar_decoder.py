import base64
import lzma
import numpy as np
import cv2
import json
from pyzbar.pyzbar import decode
import ast

cap = cv2.VideoCapture("output.mp4")

base64_data = [None] * 50000
seq_count = 0
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    frame_count += 1

    if ret:
        decoded_obj = decode(frame)
        
#        print(f"frame: {frame_count} {repr(decoded_obj)}")
        for obj in decoded_obj:
            json_obj = ast.literal_eval(obj.data.decode('utf-8'))

            if base64_data[json_obj["seq"]] is None:
                print(f'frame: {frame_count} {json_obj["seq"]}')
                base64_data[json_obj["seq"]] = json_obj["data"]
                seq_count += 1
            

    else:
        break

cap.release()
print(f"total frame processed {frame_count}")

for i in range(seq_count):
    if base64_data[i] is None:
        print(f"seq {i} is empty :(")

encoded_data = ''.join(base64_data[:seq_count])
com_data = base64.b64decode(encoded_data)
dec_data = lzma.decompress(com_data)

with open("output.pdf", "wb") as bin_file:
    bin_file.write(dec_data)

