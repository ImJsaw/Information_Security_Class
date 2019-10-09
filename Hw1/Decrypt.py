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
    def __init__(self, key: str, cipher_text: str):
        super(VernamDecryptor, self).__init__(key, cipher_text)

    def decrypt(self) -> str:
        origin_str = ''
        self.key = self.key.lower()
        len_key = len(self.key)
        count = 0
        for char in self.cipher_text:
            if count >= len_key:
                self.key += origin_str[count - len_key]
            origin_str += self._get_origin_char(text_char=char, key_char=self.key[count])
            count += 1
        return origin_str.lower()

    def _get_origin_char(self, text_char, key_char) -> str:
        text = ord(text_char) - ord('a')
        key = ord(key_char) - ord('a')
        origin_char = chr(ord('a') + (text ^ key))

        return origin_char


class RowDecryptor(BaseDecryptor):
    def decrypt(self) -> str:
        num_of_row = len(self.cipher_text) // len(self.key)

        origin_str_list = []
        for char in self.key:
            col_no = int(char)
            str_begin = (col_no - 1) * num_of_row
            str_end = col_no * num_of_row
            origin_str_list.append(self.cipher_text[str_begin:str_end])

        origin_str = ''
        for i in range(num_of_row):
            for s in origin_str_list:
                origin_str += s[i]

        return origin_str


class RailFenceDecryptor(BaseDecryptor):
    def __init__(self, key: str, cipher_text: str):
        super(RailFenceDecryptor, self).__init__(key, cipher_text)
        self.key = key

    def decrypt(self) -> str:
        cycle = (int(self.key) * 2 - 2)
        num_of_cycle = len(self.cipher_text) // cycle
        remainder_of_cycle = len(self.cipher_text) % cycle
        cycle_list = [num_of_cycle + 1] * remainder_of_cycle + [num_of_cycle] * (cycle - remainder_of_cycle)
        for i in range(int(self.key) - 2):
            cycle_list[1 + i] += cycle_list.pop(-1 - i)

        diff_list = [0]
        for i in range(len(cycle_list) - 1):
            diff_list.append(cycle_list[i])
            diff_list[i + 1] += diff_list[i]

        origin_str = ''
        for i in range(len(self.cipher_text)):
            row_ptr = i % cycle

            if row_ptr == 0:
                index = i // cycle
                origin_str += self.cipher_text[index]

            elif row_ptr == int(self.key) - 1:
                index = i // cycle + diff_list[row_ptr]
                origin_str += self.cipher_text[index]

            elif row_ptr > int(self.key) - 1:
                index = (i // cycle) * 2 + 1 + diff_list[(int(self.key) - 1) * 2 - row_ptr]
                origin_str += self.cipher_text[index]
            else:
                index = (i // cycle) * 2 + diff_list[row_ptr]
                origin_str += self.cipher_text[index]

        return origin_str


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

