import cv2
import lzma
import base64
import qrcode
import numpy as np
from PIL import Image
from multiprocessing import Pool
import math



def init():
    # Step 1: Read the file as binary
    print("Reading file...")
    with open('encoder.py', 'rb') as file:
        binary_data = file.read()
    print(f"Read {len(binary_data)} bytes.")   

    # compress the data
    compressed_data = lzma.compress(binary_data)
    print(f"compressed bin {len(compressed_data)} bytes.")

    # Step 2: Convert binary data to base64
    print("Converting to base64...")
    base64_data = base64.b64encode(compressed_data).decode('utf-8')
    print(f"base64 has {math.ceil(len(base64_data)/200)} seq")

    return base64_data



def create_qr_code(param):
    # Step 3: Create multiple QR codes
     # Create a Video from QR codes
    chunk, base64_data = param
    seq_count = chunk//200

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=40,
        border=20, # to avoid vlc status overlay top right
    )
    
    payload = { "seq" : seq_count, "data": base64_data[chunk:chunk + 200] }
    qr.add_data((payload))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    resized_img = img.resize((200,200), Image.LANCZOS)

    f = (np.uint8(np.array(resized_img)) * 255)
    # out.write(f)
    # qr_codes[seq_count] = f

    print(f"seq: {seq_count} chunk {chunk}")
    return f

   

if __name__ == '__main__':

    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, (200, 200), False)
    qr_codes = [None] * 55000

    data = init()
    white_image = np.zeros((200, 200, 255), dtype=np.uint8)

    with Pool(7) as p:
        frames = p.map(create_qr_code, [(i, data) for i in range(0, len(data), 200)])

    for i in frames:
        out.write(white_image)
        out.write(white_image)
        out.write(white_image)
        out.write(i)

    for x in range(0, 30):
        out.write(white_image)

    out.release()



