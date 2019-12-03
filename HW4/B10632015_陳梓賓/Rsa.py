import math
import random

p = 0
q = 0
n = 0
e = 0
d = 0
phi_n = 0

def init():
    global p,q,n,e,d,phi_n
    print("init")
    # generate prime nember p, q
    p = randomBigPrime()
    print("p : ",p)
    q = randomBigPrime()
    print("q : ",q)
    n = p * q
    print("n : ",n)
    print("len n : ",len(str(n)))
    phi_n = (p-1)*(q-1)
    print("phi n : ",phi_n)
    e = findMinInterprime( phi_n )
    print("e : ",e)
    d = findInverse(e, phi_n)
    print("d : ",d)
    return

def encrypt():
    print("encrypt")
    x = input("input x : ")
    #y = x^e % n
    ##  y = x ^ (e%phi_n)  % n
    y = ( int(x) ** (e % phi_n) ) % n
    print("y : ",y)
    print("n : ",n)
    print("d : ",d)
    return

def decrypt():
    print("decrypt")
    y = int( input("input y : ") )
    
    n = int( input("input n : ") )
    d = int( input("input d : ") )
    #x = y^d % n
    ##  x = y ^ (d%phi_n)  % n
    x = ( y ** d ) % n
    print("x : ",x)
    return

#generate 2 513bit prime ==> 1025 bit n
def randomBigPrime():
    while 1 == 1:
        #get random 513bit big odd number
        bigNum = "1"
        for _ in range(511):
            if random.random() > 0.5:
                bigNum += "1"
            else:
                bigNum += "0"
        bigNum += "1"
        bigNum = int(bigNum)
        #test
        if miller_rabin_test(bigNum, 20) == True:
            return bigNum
        #not prime, do again until find
        continue
    print("WTF???")

#fast base^exp % mod
def square_and_multiply(base, exp, mod):
    #exponent must >= 1
    if exp < 1 :
        return 0
    ans = base
    #get exponent binary & cut biggest bit
    binExp = str("{0:b}".format(exp))[1:]
    for i in binExp:
        ans = (ans **2) % mod
        if i == '1':
            ans = (ans*base) % mod
    return ans

# test n for k times
def miller_rabin_test(n, k):
    if n == 2:
        return True
    if n%2 == 0 :
        return False
    #rewrite n-1 to  2^u * r
    r = n-1
    u = 0
    while r % 2 == 0:
        #need to use // or overflow..
        r //= 2
        u += 1
    #repeat k time test
    for _ in range(k):
        witness = random.randint(2,n-1)
        #use square and multiply to boost
        res = square_and_multiply(witness,r,n)
        #test next witness
        if res == 1 or res == n-1:
            continue
        passFlag = False
        for _ in range(u-1):
            res = (res ** 2) % n
            if res == n-1:
                # pass test
                passFlag = True
                break
        #if pass, test next witness
        if passFlag == True:
            continue
        #test fail. composite confirm
        #print("test fail, witness",witness)
        return False
    print("find!")
    return True

#找到最小互質
def findMinInterprime(a):
    for i in range(2, a):
        if math.gcd(a,i) == 1 :
            return i
    print("not found interprime...")
    return 0

#找到 base^-1
# a^ phi_n = 1 % mod = a ^ (mod-1) = a * a^(mod-2)
# a * a^-1 = 1 %mod
# a^-1 = a^(mod-2) % mod
def findInverse( base , mod ):
    return square_and_multiply(base, mod-2, mod)

#test zone

#quit()
##

mode = input('輸入動作代碼 1/加密 2/解密 :  ')

if mode == "1":
    #init first
    init()
    encrypt()
elif mode == "2":
    decrypt()
    
print("end")