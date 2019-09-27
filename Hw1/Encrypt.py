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
        ans_txt = ''
        for c in self.plainTxt:
            #change to int, then back to char after calc
            index = char2int(c) + int(self.key)
            ans_txt += int2char(index)
        return ans_txt

class PlayfairEncryptor(BaseEncryptor):
    def encrypt(self):
        pass

class VernamEncryptor(BaseEncryptor):
    def encrypt(self):
        pass

class RowEncryptor(BaseEncryptor):
    def encrypt(self):
        pass

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

