import sys
#  1. 
#       ip
#  2. 
#       16 time
#       L(n) = R(n-1)
#       R(n) = L(n-1) XOR f( R(n-1), k(n-1) )
#  3.
#       ip(-1)
#

# get input arg
key = sys.argv[1]
plainTxt = sys.argv[2]

Ematrix = [32, 1, 2, 3, 4, 5,\
            4, 5, 6, 7, 8, 9,\
            8, 9,10,11,12,13,\
            12,13,14,15,16,17,\
            16,17,18,19,20,21,\
            20,21,22,23,24,25,\
            24,25,26,27,28,29,\
            28,29,30,31,32, 1]

ipMatrix = [58,50,42,34,26,18,10,2,\
            60,52,44,36,28,20,12,4,\
            62,54,46,38,30,22,14,6,\
            64,56,48,40,32,24,16,8,\
            57,49,41,33,25,17, 9,1,\
            59,51,43,35,27,19,11,3,\
            61,53,45,37,29,21,13,5,\
            63,55,47,39,31,23,15,7]

Pmatrix = [16, 7,20,21,29,12,28,17,\
            1,15,23,26, 5,18,31,10,\
            2, 8,24,14,32,27, 3, 9,\
           19,13,30, 6,22,11, 4,25]

pc1Matrix = [57,49,41,33,25,17, 9, 1,\
             58,50,42,34,26,18,10, 2,\
             59,51,43,35,27,19,11, 3,\
             60,52,44,36,63,55,47,39,\
             31,23,15, 7,62,54,46,38,\
             30,22,14, 6,61,53,45,37,\
             29,21,13, 5,28,20,12, 4]

pc2Matrix = [14,17,11,24, 1, 5,\
              3,28,15, 6,21,10,\
             23,19,12, 4,26, 8,\
             16, 7,27,20,13, 2,\
             41,52,31,37,47,55,\
             30,40,51,45,33,48,\
             44,49,39,56,34,53,\
             46,42,50,36,29,32]

def matrixTransform( oriTxt, matrix ):
    result = []
    for index in matrix:
        result.append(oriTxt[index-1])
    return result


def f(R,key):
    #extend R to 48 bit
    extendedTxt = matrixTransform( R, Ematrix )
    # xor with key
    for index in range(0,48):
        extendedTxt[index] = extendedTxt ^ key[index]
    #s-box
    #TODO:
    #get sBoxResult
    sBoxResult = []

    #p-box
    fResult = matrixTransform( sBoxResult, Pmatrix )
    return fResult

# get key
def k(n):
    pc1KEY = matrixTransform(key, pc1Matrix)
    offset = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
    for index in range(0,28):
        #   c0
        pc1KEY[index] = pc1KEY[(index+ offset[n])%28]
        #   d0
        pc1KEY[index+28] = pc1KEY[28+ (index+ offset[n])%28]
    kn = matrixTransform(pc1KEY, pc2Matrix)
    return kn

######  main   ########

# get 64bit bin plainTxt
plainTxtBin = bin(int(key,16)).strip("0b").zfill(64)

# get string after ip matrix
ipResult = matrixTransform(plainTxtBin, ipMatrix)