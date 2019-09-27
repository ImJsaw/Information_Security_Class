import abc
import sys

CAESAR = 'caesar'
PLAYFAIR = 'playfair'
VERNAM = 'vernam'
ROW = 'row'
RAIL_FENCE = 'rail_fence'

cipher = sys.argv[1]


class WrongInputException(Exception):
    pass


class BaseDecryptor:
    def __init__(self, key: str, cipher_text: str):
        self.key = key
        self.cipher_text = cipher_text

    @abc.abstractmethod
    def decrypt(self):
        pass


class CaesarDecryptor(BaseDecryptor):
    def decrypt(self):
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


class PlayfairDecryptor(BaseDecryptor):
    def decrypt(self) -> str:
        pass


class VernamDecryptor(BaseDecryptor):
    def decrypt(self) -> str:
        pass


class RowDecryptor(BaseDecryptor):
    def decrypt(self) -> str:
        pass


class RailFenceDecryptor(BaseDecryptor):
    def decrypt(self) -> str:
        pass


print(f'cipher:{sys.argv[1]}, key:{sys.argv[2]}, cipher_text:{sys.argv[3]}')

if cipher == CAESAR:
    caesar_decryptor = CaesarDecryptor(key=sys.argv[2], cipher_text=sys.argv[3])
    origin_text = caesar_decryptor.decrypt()
elif cipher == PLAYFAIR:
    playfair_decryptor = PlayfairDecryptor(key=sys.argv[2], cipher_text=sys.argv[3])
    origin_text = playfair_decryptor.decrypt()
elif cipher == VERNAM:
    vernam_decryptor = VernamDecryptor(key=sys.argv[2], cipher_text=sys.argv[3])
    origin_text = vernam_decryptor.decrypt()
elif cipher == ROW:
    row_decryptor = RowDecryptor(key=sys.argv[2], cipher_text=sys.argv[3])
    origin_text = row_decryptor.decrypt()
elif cipher == RAIL_FENCE:
    rail_fence_decryptor = RailFenceDecryptor(key=sys.argv[2], cipher_text=sys.argv[3])
    origin_text = rail_fence_decryptor.decrypt()
else:
    raise WrongInputException()

print(origin_text)

