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
    p = randomPrime()
    q = randomPrime()
    n = p * q
    phi_n = (p-1)*(q-1)
    e = findMinInterprime( phi_n )
    d = findInverse(e, phi_n)
    print("p q n e d")
    print(p,q,n,e,d)
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

def randomPrime():
    min = 2
    max  = 100
    # random choose prime between the range
    primes = [i for i in range(min,max) if isPrime(i)]
    return random.choice(primes)

def isPrime(primeTesting):
    #test every num < test^0.5
    for i in range(1, math.ceil( primeTesting ** 0.5 + 0.1 )):
        if math.gcd(i, primeTesting) != 1:
            return False
    return True

#找到最小互質
def findMinInterprime(a):
    for i in range(2, a):
        if math.gcd(a,i) == 1 :
            return i
    print("not found interprime...")
    return 0

#找到 base^-1
def findInverse( base , mod ):
    for i in range(2, mod):
        if (base * i) % mod == 1 :
            return i
    print("not found inverse... mod",mod)
    return 0

mode = input('輸入動作代碼 1/加密 2/解密 :  ')

if mode == "1":
    #init first
    init()
    encrypt()
elif mode == "2":
    decrypt()
    
print("end")