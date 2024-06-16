import base64
import lzma
import numpy as np
import cv2
import json
from pyzbar.pyzbar import decode
import ast
import pyboof as pb

# pb.__init_memmap()

cap = cv2.VideoCapture("output.mp4")
detector = pb.FactoryFiducial(np.uint8).qrcode()

base64_data = [None] * 50000
seq_count = 0
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    frame_count += 1

    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        boof_img = pb.ndarray_to_boof(gray)

        detector.detect(boof_img)
        for qr in detector.detections:
            data = qr.message.replace("'", "\"")
            json_obj = json.loads(data) #ast.literal_eval(qr.message.encode('utf-8'))

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

