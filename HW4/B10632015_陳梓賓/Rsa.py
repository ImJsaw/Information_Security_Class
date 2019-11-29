import math

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
    #q = randomPrime()
    q = 3
    n = p * q
    phi_n = (p-1)*(q-1)
    e = findMinInterprime( phi_n )
    d = findInverse(e, phi_n)
    print(p,q,n,e,d)
    return

def encrypt():
    print("encrypt")
    x = input("input x : ")
    plainTxt = []
    cipherTxt = []
    for i in x:
        print("ori : ",i," ascii : ",ord(i))
        plainTxt.append(ord(i))
        yD = ( ord(i) ** (e % phi_n) ) % n
        cipherTxt.append(yD)
    print(plainTxt)
    x = int(x)
    #y = x^e % n
    ##  y = x ^ (e%phi_n)  % n
    y = ( x ** (e % phi_n) ) % n
    print("y : ",y)
    return

def decrypt():
    print("decrypt")
    y = int( input("input y : ") )
    #x = y^d % n
    ##  x = y ^ (d%phi_n)  % n
    x = ( y ** (d % phi_n) ) % n
    print("x : ",x)
    return

def randomPrime():
    #TODO:
    return 11

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

#init first
init()

if mode == "1":
   encrypt()
elif mode == "2":
    decrypt()
    
print("end")