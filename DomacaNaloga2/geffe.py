### IMPORTS ###

### GLOBAL STRUCTURES ###
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X',
            'Y', 'Z',]

L = len(ALPHABET)

### AUXILIARY FUNCTIONS ###
def getNum(letter):
        '''Returns index of letter in the alphabet, starting with 0.'''
        return ord(letter) - ord('A')

def decToBin(n):
    '''Returns a string binary representation of n in 5 binary places format.'''
    binary = ''
    while n >= 1:
        binary += str(n % 2)
        n = n // 2
    binary = binary[::-1]
    head = '0' * (5-len(binary))
    binary = head + binary
    return binary

def binToDec(b):
    '''Returns a decimal representation (int) of the string binary b.'''
    d = 0
    for i in range(len(b)):
        if int(b[i]) == 0:
            continue
        else:
            d += 2 ** (len(b)-i-1)
    return d

def xor(b1, b2):
    '''Takes in 2 binary strings of same length, returns xor of them.'''
    if len(b1) != len(b2):
        print('XOR_Lenght_Error: Strings of binaries must be of same length!')
        return None
    b = ''
    for i in range(len(b1)):
        if b1[i] == b2[i]:
            b += '0'
        else:
            b += '1'
    return b

### MAIN FUNCTIONS ###


### TESTS ###

eight = decToBin(8)
six = decToBin(6)
thirty = decToBin(30)
print(eight)
print(six)
print(thirty)

print(binToDec(eight))
print(binToDec(six))
print(binToDec(thirty))

print(xor('11111','00000'))
print(xor('11111','11111'))
print(xor('11111','1111'))
