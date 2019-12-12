import math
import random


class RSA:
    def __init__(self):
        print("-------------------------------------- init -------------------------------------")
        # generate prime number p, q
        self.p = get_random_big_prime()
        print("p : ", self.p)
        self.q = get_random_big_prime()
        print("q : ", self.q)
        self.n = self.p * self.q
        print("n : ", self.n)
        self.phi_no = (self.p - 1) * (self.q - 1)
        print("phi no : ", self.phi_no)
        self.e = find_min_inter_prime(self.phi_no)
        print("e : ", self.e)
        self.d = find_base_inverse(self.e, self.phi_no)
        print("d : ", self.d)

    def encrypt(self):
        print("------------------------------------ encrypt ------------------------------------")
        x = input("input plain_text : ")

        plain_text = ""
        for i in x:
            plain_text += str("{0:08b}".format(ord(i)))
        plain_number = int(plain_text, 2)

        y = square_and_multiply(plain_number, self.e % self.phi_no, self.n)

        print("cipher_text : ", y)
        print("n : ", self.n)
        print("d : ", self.d)
        return

    @staticmethod
    def decrypt():
        print("------------------------------------ decrypt ------------------------------------")
        y = int(input("enter cipher_text : "))
        n = int(input("enter n : "))
        d = int(input("enter d : "))

        x = square_and_multiply(y, d, n)

        cipher_str = str("{0:b}".format(x))
        cipher_index = 0
        plain_text = ""

        need_to_padding = 8 - len(cipher_str) % 8
        cipher_str = cipher_str.zfill(len(cipher_str) + need_to_padding)
        while cipher_index < len(cipher_str):
            char_binary_str = cipher_str[cipher_index: cipher_index + 8]
            cipher_index += 8
            char_ascii = int(char_binary_str, 2)
            char = chr(char_ascii)
            plain_text += char
        print("plainTxt : ", plain_text)
        return


def find_min_inter_prime(a):
    for i in range(2, a):
        if math.gcd(a, i) == 1:
            return i
    print("inter_prime not found")
    return 0


def find_base_inverse(base, mod):
    _, x, _ = extended_gcd(base, mod)
    return x % mod


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x


def get_random_big_prime():
    while 1 == 1:
        big_no = "1"
        for _ in range(510):
            if random.random() > 0.5:
                big_no += "1"
            else:
                big_no += "0"
        big_no += "1"
        big_no = int(big_no,2)
        if miller_rabin_test(big_no, 300):
            return big_no
        continue


def miller_rabin_test(n, k):
    r = n-1
    u = 0
    while r % 2 == 0:
        r //= 2
        u += 1

    for _ in range(k):
        witness = random.randint(2, n-1)
        res = square_and_multiply(witness, r, n)

        if res == 1 or res == n-1:
            continue

        pass_flag = False
        for _ in range(u-1):
            res = (res ** 2) % n
            if res == n-1:
                pass_flag = True
                break
        if pass_flag:
            continue
        return False
    return True


def square_and_multiply(base, exp, mod):
    if exp < 1:
        return 0
    ans = base
    bin_exp = str("{0:b}".format(exp))[1:]
    for i in bin_exp:
        ans = (ans ** 2) % mod
        if i == '1':
            ans = (ans*base) % mod
    return ans


ENCRYPT = 'encrypt'
DECRYPT = 'decrypt'


if __name__ == '__main__':

    mode = input('輸入指令 encrypt/加密 decrypt/解密 :  ')

    rsa = RSA()

    if mode == ENCRYPT:
        rsa.encrypt()
    elif mode == DECRYPT:
        rsa.decrypt()
