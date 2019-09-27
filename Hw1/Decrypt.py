import sys

CAESAR = 'caesar'
PLAYFAIR = 'playfair'
VERNAM = 'vernam'
ROW = 'row'
RAIL_FENCE = 'rail_fence'

cipher = sys.argv[1]


class WrongInputException(Exception):
    pass


class Decryptor:
    def __init__(self, key: str, cipher_text: str):
        self.cipher_text = cipher_text.lower()
        self.key = key

    def caesar_decrypt(self) -> str:
        if int(self.key) < 0 or int(self.key) > 26:
            raise WrongInputException()

        ans_text = ''
        for c in self.cipher_text:
            # ord() means the ascii_code of the char, e.g. ord('a') == 97
            origin_ascii_code = ord(c) - int(self.key)
            if origin_ascii_code < ord('a'):
                origin_ascii_code = ord('z') - (ord('a') - origin_ascii_code - 1)

            # chr() means the char of the ascii_code, e.g. chr(97) == 'a'
            ans_text += chr(origin_ascii_code)
        return ans_text

    def playfair_decrypt(self) -> str:
        pass

    def vernam_decrypt(self) -> str:
        pass

    def row_decrypt(self) -> str:
        pass

    def rail_fence_decrypt(self) -> str:
        pass


print(f'cipher:{sys.argv[1]}, key:{sys.argv[2]}, cipher_text:{sys.argv[3]}')

decryptor = Decryptor(key=sys.argv[2], cipher_text=sys.argv[3])
if cipher == CAESAR:
    origin_text = decryptor.caesar_decrypt()
elif cipher == PLAYFAIR:
    origin_text = decryptor.playfair_decrypt()
elif cipher == VERNAM:
    origin_text = decryptor.vernam_decrypt()
elif cipher == ROW:
    origin_text = decryptor.row_decrypt()
elif cipher == RAIL_FENCE:
    origin_text = decryptor.rail_fence_decrypt()
else:
    raise WrongInputException()

print(origin_text)

