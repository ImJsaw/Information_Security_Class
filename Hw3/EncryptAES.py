import io
import random
import base64

from PIL import Image

if __name__ == '__main__':
    # initial_vector
    iv = []
    for i in range(0, 128):
        iv.append(random.randint(0, 1))

    # mode = input('輸入加密的Mode')

    im = Image.open('./mypppm.ppm')
    img_byte_arr = io.BytesIO()
    im.save(img_byte_arr, format=im.format)
    img_byte_arr = base64.b16encode(img_byte_arr.getvalue())    # img base16
