import io
from pathlib import Path

from Crypto.Cipher import AES
from PIL import Image


class DecryptAES:
    def __init__(self, decrypt_mode, key):
        self._mode = decrypt_mode
        self._key = key
        self._iv = self._key
        print('[**] Random key is', self._key)

    def decrypt(self, cipher_text):
        if self._mode == ECB:
            self._ecb_decrypt(cipher_text=cipher_text)
        elif self._mode == CBC:
            self._cbc_decrypt(cipher_text=cipher_text)
        elif self._mode == CBC_F:
            self._cbc_feedback_decrypt(cipher_text=cipher_text)

    def _ecb_decrypt(self, cipher_text):
        count = 0
        count_newline = 0
        cipher = AES.new(self._key, AES.MODE_ECB)
        plainTxt = b''

        # 把不需要加密的部分取出
        while count_newline < 3:
            byte = cipher_text[count]
            count += 1
            byte = bytes(chr(byte), encoding='utf-8')
            plainTxt += byte

            if byte == b'\n':
                count_newline += 1

        block_index = 0

        # decrypt
        cipher_text = cipher_text[count:]
        while block_index < len(cipher_text):
            block = cipher_text[block_index: block_index + AES.block_size]
            cipher_block = cipher.decrypt(block)
            plainTxt += cipher_block

            block_index += AES.block_size
        self.writeDecryptImg(plainTxt)

    def _cbc_decrypt(self, cipher_text):
        count = 0
        count_newline = 0
        cipher = AES.new(self._key, AES.MODE_ECB)
        plainTxt = b''
        prev_ct = self._iv

        # 把不需要加密的部分取出
        while count_newline < 3:
            byte = cipher_text[count]
            count += 1
            byte = bytes(chr(byte), encoding='utf-8')
            plainTxt += byte

            if byte == b'\n':
                count_newline += 1

        block_index = 0

        # decrypt
        cipher_text = cipher_text[count:]
        while block_index < len(cipher_text):
            block = cipher_text[block_index: block_index + AES.block_size]
            plain_block = cipher.decrypt(block)

            # xor with prev cipher txt
            final_block = byte_xor(plain_block, prev_ct)
            prev_ct = block
            plainTxt += final_block

            block_index += AES.block_size
        self.writeDecryptImg(plainTxt)

    def _cbc_feedback_decrypt(self, cipher_text):
        count = 0
        count_newline = 0
        cipher = AES.new(self._key, AES.MODE_ECB)
        plainTxt = b''
        prev_ct = self._iv

        # 把不需要加密的部分取出
        while count_newline < 3:
            byte = cipher_text[count]
            count += 1
            byte = bytes(chr(byte), encoding='utf-8')
            plainTxt += byte

            if byte == b'\n':
                count_newline += 1

        block_index = 0

        # decrypt
        cipher_text = cipher_text[count:]
        while block_index < len(cipher_text):
            block = cipher_text[block_index: block_index + AES.block_size]
            plain_block = cipher.decrypt(block)

            # xor with prev cipher txt
            final_block = byte_xor(plain_block, prev_ct)
            prev_ct = block[1:] + b'\x00'
            plainTxt += final_block

            block_index += AES.block_size
        self.writeDecryptImg(plainTxt)

    def writeDecryptImg(self, plainTxt):
        ans_path = Path(__file__).parent / 'ans.ppm'
        with open(ans_path, "wb") as fp:
            fp.write(plainTxt)

        ppm_picture = ans_path
        output_img = Image.open(ppm_picture)

        result_path = Path(__file__).parent / 'ans.png'
        output_img.save(result_path, 'png')


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


ECB = 'ECB'
CBC = 'CBC'
CBC_F = 'CBC_F'


if __name__ == '__main__':
    
    mode = input('輸入加密的Mode: ')
    #open cipher img
    path = Path(__file__).parent / 'result.ppm'
    im = Image.open(path)
    img_byte_array = io.BytesIO()
    im.save(img_byte_array, format=im.format)
    img_byte_array = img_byte_array.getvalue()

    path = Path(__file__).parent / 'key.txt'
    with open(path, 'rb') as f:
        key = f.read()

    if mode == ECB:
        decrypt_aes = DecryptAES(decrypt_mode=ECB, key=key)
        decrypt_aes.decrypt(cipher_text=img_byte_array)
    elif mode == CBC:
        decrypt_aes = DecryptAES(decrypt_mode=CBC, key=key)
        decrypt_aes.decrypt(cipher_text=img_byte_array)
    elif mode == CBC_F:
        decrypt_aes = DecryptAES(decrypt_mode=CBC_F, key=key)
        decrypt_aes.decrypt(cipher_text=img_byte_array)
