import random
from hashlib import sha1


class DSA:
    def _init(self):
        print("-------------------------------------- init -------------------------------------")
        # generate prime number p, q
        self.p, self.q = self._generate_p_and_q()
        print(f'p:{self.p}\nq:{self.q}')
        self.a = self._generate_a()
        print(f'a:{self.a}')
        self.d = random.randint(1, self.q)
        #print(f'd:{self.d}')
        self.b = self._generate_b()
        print(f'b:{self.b}')
        self.ke = random.randint(1, self.q)
        #print(f'ke:{self.ke}')

    def sign(self):
        self._init()
        print("-------------------------------------- sign ------------------------------------")
        x = input("Enter plain_text : ").encode('utf-8')

        r = self._generate_r()
        print(f'r:{r}')
        s = self._generate_s(r, x)
        print(f's:{s}')

    @staticmethod
    def verify():
        print("-------------------------------------- verify -------------------------------------")
        p = int(input('Enter p : '))
        q = int(input('Enter q : '))
        a = int(input('Enter a : '))
        b = int(input('Enter b : '))
        r = int(input('Enter r : '))
        s = int(input('Enter s : '))

        x = input('Enter plain_text : ').encode('utf-8')

        w = find_inverse(s, q)

        h = int(sha1(x).hexdigest(), 16)
        v =  ( (square_and_multiply(a, (w * h) % q, p) * square_and_multiply(b, (w *r) % p, p) ) %p ) % q
        #v = (a ** (w * h % q) * (b ** (w * r % p))) % q
        print(f'v:{v}')
        print(f'r:{r}')

    def _generate_s(self, r, plain_text):
        h = int(sha1(plain_text).hexdigest(), 16)
        s = ((h + self.d * r) * find_inverse(self.ke, self.q)) % self.q
        return s

    def _generate_r(self):
        r = square_and_multiply(self.a, self.ke, self.p)
        #r = square_and_multiply(r, 1, self.q)
        return r%self.q

    def _generate_b(self):
        b = square_and_multiply(self.a, self.d, self.p)
        return b

    def _generate_a(self):
        h = random.randint(1, self.p - 1)
        exp = (self.p - 1) // self.q
        a = square_and_multiply(h, exp, self.p)
        return a

    @staticmethod
    def _generate_p_and_q() -> tuple:
        while True:
            q = get_random_big_prime(bit_no=160)

            big_no = ''
            # generate 864 bits big number
            for _ in range(864):
                big_no += '1'
            big_no = int(big_no, 2)

            big_no_base = ''
            for _ in range(863):
                big_no_base += '1'
            big_no_base = int(big_no_base, 2)

            for i in range(big_no_base, big_no):
                p = q * i + 1
                if miller_rabin_test(p, 300):
                    return p, q

            print('p not found')


def get_random_big_prime(bit_no):
    while 1 == 1:
        big_no = "1"
        for _ in range(bit_no - 2):
            if random.random() > 0.5:
                big_no += "1"
            else:
                big_no += "0"
        big_no += "1"
        big_no = int(big_no, 2)
        if miller_rabin_test(big_no, 300):
            return big_no
        continue


def miller_rabin_test(n, k):
    r = n - 1
    u = 0
    while r % 2 == 0:
        r //= 2
        u += 1

    for _ in range(k):
        witness = random.randint(2, n - 1)
        res = square_and_multiply(witness, r, n)

        if res == 1 or res == n - 1:
            continue

        pass_flag = False
        for _ in range(u - 1):
            res = (res ** 2) % n
            if res == n - 1:
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
            ans = (ans * base) % mod
    return ans


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x


def find_inverse(base, mod):
    _, x, _ = extended_gcd(base, mod)
    return x % mod


if __name__ == '__main__':
    mode = input('輸入指令 0/sign 1/verify :  ')

    dsa = DSA()
    if mode == '0':
        dsa.sign()
    elif mode == '1':
        dsa.verify()
