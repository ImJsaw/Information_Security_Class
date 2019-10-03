import abc
import sys
from typing import List

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
        self.cipher_text = cipher_text.lower()

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
    def __init__(self, key: str, cipher_text: str):
        super(PlayfairDecryptor, self).__init__(key, cipher_text)
        self.matrix = []

    def decrypt(self) -> str:
        self.make_matrix()
        text = self.get_origin_char()
        return text

    def make_matrix(self):
        self.key = self.key.lower()
        for char in self.key:
            if char == 'j':
                char = 'i'

            if char not in self.matrix:
                self.matrix.append(char)

        for alpha_code in range(ord('a'), ord('z') + 1):
            char = chr(alpha_code)
            if char == 'j':
                char = 'i'

            if char not in self.matrix:
                self.matrix.append(char)

            if len(self.matrix) >= 25:
                break

    def get_origin_char(self) -> str:
        origin_str = ''

        for char_index in range(0, len(self.cipher_text), 2):
            char1 = self.cipher_text[char_index]
            char2 = self.cipher_text[char_index + 1]

            index1 = self._get_matrix_index_by(char1)
            index2 = self._get_matrix_index_by(char2)

            # same column
            if index1 % 5 == index2 % 5:
                char1 = self._get_matrix_char_by(index1 + 20)
                char2 = self._get_matrix_char_by(index2 + 20)
            # same row
            elif int(index1 / 5) == int(index2 / 5):
                char1 = self._get_matrix_char_by((index1 + 4) % 5 + self._get_row_index_by(index1) * 5)
                char2 = self._get_matrix_char_by((index2 + 4) % 5 + self._get_row_index_by(index2) * 5)
            else:
                char1 = self._get_matrix_char_by(index2 % 5 + self._get_row_index_by(index1) * 5)
                char2 = self._get_matrix_char_by(index1 % 5 + self._get_row_index_by(index2) * 5)

            # if char2 == 'x':
            #     char2 = char1

            origin_str += char1 + char2

        return origin_str

    def _get_matrix_index_by(self, char) -> int:
        return self.matrix.index(char)

    def _get_matrix_char_by(self, index) -> str:
        return self.matrix[index % 25]

    @staticmethod
    def _get_row_index_by(index) -> int:
        return index // 5

    def _get_head_by(self, index) -> int:
        return int(index / 5) * 5


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

