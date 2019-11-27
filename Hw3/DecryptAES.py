import io
import os

from Crypto import Random
from Crypto.Cipher import AES
from PIL import Image


class DecryptAES:
    def __init__(self, decrypt_mode, key):
        self._mode = decrypt_mode
        self._key = key
        self._iv = self._key
        print('[**] Random key is', self._key)

    def decrypt(self, plain_text):
        if self._mode == ECB:
            self._ecb_decrypt(plain_text=plain_text)
        elif self._mode == CBC:
            self._cbc_decrypt(plain_text=plain_text)

    def _ecb_decrypt(self, plain_text):
        count = 0
        count_newline = 0
        cipher = AES.new(self._key, AES.MODE_ECB)
        plainTxt = b''

        # 把不需要加密的部分取出
        while count_newline < 3:
            byte = plain_text[count]
            count += 1
            byte = bytes(chr(byte), encoding='utf-8')
            plainTxt += byte

            if byte == b'\n':
                count_newline += 1

        block_index = 0

        # decrypt
        plain_text = plain_text[count:]
        while block_index < len(plain_text):
            block = plain_text[block_index: block_index + AES.block_size]
            cipher_block = cipher.decrypt(block)
            plainTxt += cipher_block

            block_index += AES.block_size
        self.writeDecryptImg(plainTxt)

    def _cbc_decrypt(self, plain_text):
        count = 0
        count_newline = 0
        cipher = AES.new(self._key, AES.MODE_ECB)
        plainTxt = b''
        prev_ct = self._iv

        # 把不需要加密的部分取出
        while count_newline < 3:
            byte = plain_text[count]
            count += 1
            byte = bytes(chr(byte), encoding='utf-8')
            plainTxt += byte

            if byte == b'\n':
                count_newline += 1

        block_index = 0

        # decrypt
        plain_text = plain_text[count:]
        while block_index < len(plain_text):
            block = plain_text[block_index: block_index + AES.block_size]
            plain_block = cipher.decrypt(block)

            final_block = byte_xor(plain_block, prev_ct)
            prev_ct = final_block
            plainTxt += final_block

            block_index += AES.block_size
        self.writeDecryptImg(plainTxt)

    def writeDecryptImg(self, plainTxt):
        with open("./Hw3/ans.ppm", "wb") as f:
            f.write(plainTxt)
        ppm_picture = './Hw3/ans.ppm'
        output_img = Image.open(ppm_picture)
        output_img.save('./Hw3/ans.png', 'png')


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


ECB = 'ECB'
CBC = 'CBC'


if __name__ == '__main__':
    
    print(os.getcwd())
    key = input('輸入Key: ')
    mode = input('輸入加密的Mode: ')
    #open cipher img
    im = Image.open('./Hw3/result.ppm')
    img_byte_array = io.BytesIO()
    im.save(img_byte_array, format=im.format)
    img_byte_array = img_byte_array.getvalue()

    if mode == ECB:
        decrypt_aes = DecryptAES(decrypt_mode=ECB, key=key)
        decrypt_aes.decrypt(plain_text=img_byte_array)
    elif mode == CBC:
        decrypt_aes = DecryptAES(decrypt_mode=CBC, key=key)
        decrypt_aes.decrypt(plain_text=img_byte_array)
