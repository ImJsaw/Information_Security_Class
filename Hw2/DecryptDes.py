import sys
from typing import List, Tuple

FP_Matrix = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25,
]

IP_Matrix = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7,
]

PC_1_Matrix = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4,
]

PC_2_Matrix = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32,
]

E_Matrix = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1,
]

S_Box_1 = [
    14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
    0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
    4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
    15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13,
]

S_Box_2 = [
    15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
    3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
    0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
    13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9,
]

S_Box_3 = [
    10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
    13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
    13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
    1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12,
]

S_Box_4 = [
    7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
    13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
    10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
    3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14,
]

S_Box_5 = [
    2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
    14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
    4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
    11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3,
]

S_Box_6 = [
    12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
    10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
    9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
    4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13,
]

S_Box_7 = [
    4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
    13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
    1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
    6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12,
]

S_Box_8 = [
    13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
    1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
    7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
    2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11,
]

P_Box = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25,
]


class Key:
    def __init__(self, hex_key: str):
        self.key = self._hex_key_to_binary_key(hex_key)
        self.key_offset = [0, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
        self.offset_time = 0

    def offset(self):
        c, d = self._divide_into_two_part()

        offset_no = self.key_offset[self.offset_time]
        while offset_no != 0:
            char = c.pop(-1)
            c.insert(0, char)
            char = d.pop(-1)
            d.insert(0, char)
            offset_no -= 1

        self.key = c
        self.key.extend(d)
        self.offset_time += 1

    def _divide_into_two_part(self):
        c = list(self.key[:28])
        d = list(self.key[28:])
        return c, d

    def get_pc_2(self):
        result_key_matrix = []
        for index in PC_2_Matrix:
            result_key_matrix.append(self.key[index - 1])

        return result_key_matrix

    def turn_to_pc_1(self):
        result_key_matrix = []
        for index in PC_1_Matrix:
            result_key_matrix.append(self.key[index - 1])

        self.key = result_key_matrix

    @staticmethod
    def _hex_key_to_binary_key(hex_key):
        hex_int = int(hex_key, 16)
        return '{0:b}'.format(hex_int)


class CipherText:
    def __init__(self, hex_cipher_text: str):
        self.cipher_text = self._hex_cipher_to_binary_cipher(hex_cipher_text)

    def turn_to_fp(self):
        result_cipher_text_matrix = []
        for index in FP_Matrix:
            result_cipher_text_matrix.append(self.cipher_text[index - 1])

        self.cipher_text = result_cipher_text_matrix

    def set_cipher_text_by(self, left: List, right: List):
        result_cipher_text_matrix = []
        result_cipher_text_matrix.extend(left)
        result_cipher_text_matrix.extend(right)

        self.cipher_text = result_cipher_text_matrix

    def divide_into_left_and_right(self) -> Tuple[List, List]:
        assert isinstance(self.cipher_text, List)
        left = self.cipher_text[32:]
        right = self.cipher_text[:32]

        return left, right

    def turn_to_ip(self):
        result_cipher_text_matrix = []
        for index in IP_Matrix:
            result_cipher_text_matrix.append(self.cipher_text[index - 1])

        self.cipher_text = result_cipher_text_matrix

    @staticmethod
    def _hex_cipher_to_binary_cipher(hex_cipher_text):
        hex_int = int(hex_cipher_text, 16)
        return '{0:b}'.format(hex_int).zfill(64)


class Decryptor:
    def __init__(self, hex_key: str, hex_cipher_text: str):
        self.key = Key(hex_key)
        self.cipher_text = CipherText(hex_cipher_text)

    def decrypt(self):
        # init
        self.key.turn_to_pc_1()
        self.cipher_text.turn_to_ip()

        for i in range(16):
            self.key.offset()

            k = self.key.get_pc_2()
            l, r = self.cipher_text.divide_into_left_and_right()
            f = self._f_function(l, k)
            result = self._do_xor(r, f)

            if i == 15:
                self.cipher_text.set_cipher_text_by(result, l)
            else:
                self.cipher_text.set_cipher_text_by(l, result)
            # self.cipher_text.set_cipher_text_by(l, result)

        self.cipher_text.turn_to_fp()
        text_int = int(''.join(self.cipher_text.cipher_text), 2)
        return hex(text_int)

    def _f_function(self, left, k) -> List:
        left = self._expanse(left)
        result = self._do_xor(left, k)
        result = self._s_box(result)
        result = self._p_box(result)

        return result

    @staticmethod
    def _p_box(result):
        result_matrix = []
        for index in P_Box:
            result_matrix.append(result[index - 1])

        return result_matrix

    def _s_box(self, result):
        result_list = []
        result_list.extend(self._get_s_box_output(result[:6], S_Box_1))
        result_list.extend(self._get_s_box_output(result[6:12], S_Box_2))
        result_list.extend(self._get_s_box_output(result[12:18], S_Box_3))
        result_list.extend(self._get_s_box_output(result[18:24], S_Box_4))
        result_list.extend(self._get_s_box_output(result[24:30], S_Box_5))
        result_list.extend(self._get_s_box_output(result[30:36], S_Box_6))
        result_list.extend(self._get_s_box_output(result[36:42], S_Box_7))
        result_list.extend(self._get_s_box_output(result[42:], S_Box_8))

        return result_list

    @staticmethod
    def _get_s_box_output(ip, s_box_matrix) -> List:
        row_no = int(f'{ip[0]}{ip[5]}', 2)
        col_no = int(''.join(ip[1:5]), 2)

        output_no = s_box_matrix[row_no * 16 + col_no]
        return list('{0:b}'.format(output_no).zfill(4))

    @staticmethod
    def _expanse(left) -> List:
        result_left_text_matrix = []
        for index in E_Matrix:
            result_left_text_matrix.append(left[index - 1])

        return result_left_text_matrix

    @staticmethod
    def _do_xor(a, b) -> List:
        result_list = []
        for index in range(len(a)):
            if a[index] == b[index]:
                result_list.append('0')
            else:
                result_list.append('1')

        return result_list


if __name__ == '__main__':
    key = sys.argv[1]
    cipher_text = sys.argv[2]
    print(key, cipher_text)

    decryptor = Decryptor(hex_key=key, hex_cipher_text=cipher_text)
    print(decryptor.decrypt())
