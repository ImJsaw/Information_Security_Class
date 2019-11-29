import io
import sys
from pathlib import Path

from Crypto import Random
from Crypto.Cipher import AES
from PIL import Image


class EncryptAES:
    def __init__(self, encrypt_mode):
        self._mode = encrypt_mode
        self._key = Random.new().read(AES.block_size)
        self._iv = self._key

        key_path = Path(__file__).parent / 'key.txt'
        with open(key_path, 'wb') as f:
            f.write(self._key)

    def encrypt(self, plain_text):
        if self._mode == ECB:
            self._ecb_encrypt(plain_text=plain_text)
        elif self._mode == CBC:
            self._cbc_encrypt(plain_text=plain_text)
        elif self._mode == CUSTOM:
            self._custom_encrypt(plain_text=plain_text)

    def _ecb_encrypt(self, plain_text):
        count = 0
        count_newline = 0
        cipher = AES.new(self._key, AES.MODE_ECB)
        cipher_text = b''

        # 把不需要加密的部分取出
        while count_newline < 3:
            byte = plain_text[count]
            count += 1
            byte = bytes(chr(byte), encoding='utf-8')
            cipher_text += byte

            if byte == b'\n':
                count_newline += 1

        block_index = 0

        # encrypt
        plain_text = plain_text[count:]

        while len(plain_text) % AES.block_size != 0:
            plain_text += b'\x00'

        while block_index < len(plain_text):
            block = plain_text[block_index: block_index + AES.block_size]
            cipher_block = cipher.encrypt(block)
            cipher_text += cipher_block

            block_index += AES.block_size

        self._write_image(cipher_text)

    def _cbc_encrypt(self, plain_text):
        count = 0
        count_newline = 0
        cipher = AES.new(self._key, AES.MODE_ECB)
        cipher_text = b''
        prev_ct = self._iv

        # 把不需要加密的部分取出
        while count_newline < 3:
            byte = plain_text[count]
            count += 1
            byte = bytes(chr(byte), encoding='utf-8')
            cipher_text += byte

            if byte == b'\n':
                count_newline += 1

        block_index = 0

        # encrypt
        plain_text = plain_text[count:]

        while len(plain_text) % AES.block_size != 0:
            plain_text += b'\x00'

        while block_index < len(plain_text):
            block = plain_text[block_index: block_index + AES.block_size]
            final_block = byte_xor(block, prev_ct)

            cipher_block = cipher.encrypt(final_block)
            prev_ct = cipher_block
            cipher_text += cipher_block

            block_index += AES.block_size

        self._write_image(cipher_text)

    def _custom_encrypt(self, plain_text):
        count = 0
        count_newline = 0
        cipher = AES.new(self._key, AES.MODE_ECB)
        cipher_text = b''
        prev_ct = self._iv
        # cast key to bin
        binKey = bin(int.from_bytes(self._key, byteorder=sys.byteorder))[2:]

        # 把不需要加密的部分取出
        while count_newline < 3:
            byte = plain_text[count]
            count += 1
            byte = bytes(chr(byte), encoding='utf-8')
            cipher_text += byte

            if byte == b'\n':
                count_newline += 1

        block_index = 0

        # encrypt
        plain_text = plain_text[count:]

        while len(plain_text) % AES.block_size != 0:
            plain_text += b'\x00'

        while block_index < len(plain_text):
            block = plain_text[block_index: block_index + AES.block_size]
            final_block = byte_xor(block, prev_ct)

            cipher_block = cipher.encrypt(final_block)

            if(binKey[int((block_index/AES.block_size)%len(binKey))] == '0'):
                prev_ct = cipher_block
            else:
                prev_ct = cipher_block[1:] + b'\x00'

            cipher_text += cipher_block

            block_index += AES.block_size

        self._write_image(cipher_text)

    @staticmethod
    def _write_image(cipher_text):
        ppm_path = Path(__file__).parent / 'result.ppm'
        with open(ppm_path, "wb") as f:
            f.write(cipher_text)

        ppm_picture = ppm_path
        output_img = Image.open(ppm_picture)

        result_path = Path(__file__).parent / 'result.png'
        output_img.save(result_path, 'png')


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


ECB = 'ECB'
CBC = 'CBC'
CUSTOM = 'CST'


if __name__ == '__main__':
    mode = input('輸入加密的Mode: ')

    path = Path(__file__).parent / 'mypppm.ppm'
    im = Image.open(path)
    img_byte_array = io.BytesIO()
    im.save(img_byte_array, format=im.format)
    img_byte_array = img_byte_array.getvalue()

    if mode == ECB:
        encrypt_aes = EncryptAES(encrypt_mode=ECB)
        encrypt_aes.encrypt(plain_text=img_byte_array)
    elif mode == CBC:
        encrypt_aes = EncryptAES(encrypt_mode=CBC)
        encrypt_aes.encrypt(plain_text=img_byte_array)
    elif mode == CUSTOM:
        encrypt_aes = EncryptAES(encrypt_mode=CUSTOM)
        encrypt_aes.encrypt(plain_text=img_byte_array)
