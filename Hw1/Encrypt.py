import abc
import sys

CAESAR = 'caesar'
PLAYFAIR = 'playfair'
VERNAM = 'vernam'
ROW = 'row'
RAIL_FENCE = 'rail_fence'

#get arg
cipher = sys.argv[1]
key = sys.argv[2]
plainTxt = sys.argv[3]

# converter between char & index
def char2int(char):
    return ord(char)-ord('a')
def int2char(i):
    index = (i+26)%26 + ord('a')
    return chr(index)




class WrongInputException(Exception):
    pass

class BaseEncryptor:
    def __init__(self, key: str, plainTxt: str):
        self.key = key
        self.plainTxt = plainTxt
    #抽象
    @abc.abstractmethod
    def encrypt(self):
        pass

class CaesarEncryptor(BaseEncryptor):
    def encrypt(self):
        if int(self.key) < 0 or int(self.key) > 26:
            raise WrongInputException()
        cipherTxt = ''
        for c in self.plainTxt:
            #change to int, then back to char after calc
            index = char2int(c) + int(self.key)
            cipherTxt += int2char(index)
        return cipherTxt

class PlayfairEncryptor(BaseEncryptor):
    a2z = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    matrix = []
    #ignore duplicated char & blank, then put str into matrix
    def putMatrix(self, rawStr):
        for char in rawStr:
            # i/j considered same
            if char.upper() == 'J':
                c = 'I'
            else:
                c = char.upper()
            if c not in self.matrix and c != ' ':
                self.matrix.append(c)
        pass
    
    def processPlainTxt(self):
        ans = ""
        for char in self.plainTxt:
            # divide same letter in a block
            if ans != "" and char.upper() == ans[-1] and len(ans) %2 == 1:
                ans += "X"
            # ignore blank
            if char != ' ':
                ans += char.upper()
        # plaintxt len can't be odd
        if len(ans) %2 == 1:
            ans += "X"
        return ans
    # matrix index & char converter
    def getMatrixIndex(self, char):
        if char.upper() == 'J':
            c = 'I'
        else:
            c = char.upper()
        return self.matrix.index(c)   
    def getMatrixChar(self, index):
        return self.matrix[index%25]
    
    #get the row head index in matrix
    def getHead(self, index):
        return int(index/5)*5

    # func for single block
    def playfairFunc(self, char1, char2):
        # change to index
        index1 = self.getMatrixIndex(char1)
        index2 = self.getMatrixIndex(char2)
        ans = ""
        # same column
        if index1%5 == index2%5:
            ans = self.getMatrixChar(index1+5) + self.getMatrixChar(index2+5)
        # same row
        elif int(index1/5) == int(index2/5):
            ans = self.getMatrixChar(self.getHead(index1) + (index1%5+1)%5 ) + self.getMatrixChar(self.getHead(index2) + (index2%5+1)%5 )
        # got a square (horizon)
        else:
            ans = self.getMatrixChar(self.getHead(index1) + index2%5 ) + self.getMatrixChar(self.getHead(index2) + index1%5 )
        return ans

    def encrypt(self):
        self.putMatrix(self.key)
        self.putMatrix(self.a2z)
        processedPlainTxt = self.processPlainTxt()
        cipherTxt = ""
        for index in range(int(len(processedPlainTxt)/2)):
            cipherTxt += self.playfairFunc( processedPlainTxt[index*2], processedPlainTxt[index*2+1] )
        return cipherTxt

class VernamEncryptor(BaseEncryptor):
    def encrypt(self):
        self.key += self.plainTxt
        cipherTxt = ''
        for index in range(len(self.plainTxt)):
            index = char2int(self.plainTxt[index]) + char2int(self.key[index])
            cipherTxt += int2char(index)
        return cipherTxt.upper()

class RowEncryptor(BaseEncryptor):
    # rearrange index for easier handle data
    def rowIndex(self):
        order = []
        for num in range(len(self.key)+1):
            for index in range(len(self.key)):
                if(int(self.key[index]) == num):
                    order.append(index)
        return order
    
    def encrypt(self):
        cipherTxt = ''
        keyLen = len(self.key)
        rowIndex = self.rowIndex()
        for index in range(keyLen):
            for row in range(int(len(self.plainTxt)/keyLen-0.00001)+1):
                cipherTxt += plainTxt[row * keyLen + rowIndex[index]]
        return cipherTxt

class RailFenceEncryptor(BaseEncryptor):
    def encrypt(self):
        pass

if cipher == CAESAR:
    cipherTxt = CaesarEncryptor(key=sys.argv[2], plainTxt=sys.argv[3]).encrypt()

elif cipher == PLAYFAIR:
    cipherTxt = PlayfairEncryptor(key=sys.argv[2], plainTxt=sys.argv[3]).encrypt()

elif cipher == VERNAM:
    cipherTxt = VernamEncryptor(key=sys.argv[2], plainTxt=sys.argv[3]).encrypt()
    
elif cipher == ROW:
    cipherTxt = RowEncryptor(key=sys.argv[2], plainTxt=sys.argv[3]).encrypt()

elif cipher == RAIL_FENCE:
    cipherTxt = RailFenceEncryptor(key=sys.argv[2], plainTxt=sys.argv[3]).encrypt()

else:
    print("w")
    raise WrongInputException()

print(cipherTxt)

