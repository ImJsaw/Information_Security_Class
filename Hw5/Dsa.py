import random


class DSA:
    def __init__(self):
        print("-------------------------------------- init -------------------------------------")
        # generate prime number p, q
        self.p, self.q = self._generate_p_and_q()
        print(self.q)

    def _generate_p_and_q(self):
        while True:
            q = get_random_big_prime(bit_no=160)
            
            continue

def get_random_big_prime(bit_no):
    while 1 == 1:
        big_no = "1"
        for _ in range(bit_no-2):
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


if __name__ == '__main__':

    # mode = input('輸入指令 encrypt/加密 decrypt/解密 :  ')

    dsa = DSA()
