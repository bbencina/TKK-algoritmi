### IMPORTS ###
import time

### GLOBAL STRUCTURES ###
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X',
            'Y', 'Z',]

L = len(ALPHABET)

# frequency of letters in the English language (in %)
# source: http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
FREQUENCY = {'A': 8.12, 'B': 1.49, 'C': 2.71, 'D': 4.32, 'E': 12.02, 'F': 2.3,
             'G': 2.03, 'H': 5.92, 'I': 7.31, 'J': 0.1, 'K': 0.69, 'L': 3.98,
             'M': 2.61, 'N': 6.95, 'O': 7.68, 'P': 1.82, 'Q': 0.11, 'R': 6.02,
             'S': 6.28, 'T': 9.10, 'U': 2.88, 'V': 1.11, 'W': 2.09, 'X': 0.17,
             'Y': 2.11, 'Z': 0.07}

# wordlists of common words divided by context
# all words are at least 4 letters (20 bits) long for better matching

# some of the most common words in the English language
# compiled by me with help by:
# src: https://en.wikipedia.org/wiki/Most_common_words_in_English
WORDLIST_COMMON = ['THAT', 'THIS', 'ITIS', 'VERY', 'MANY',
            'HAVE', 'WILL', 'YOUR', 'FROM', 'THEY', 'KNOW',
            'BEEN', 'GOOD', 'MUCH', 'SOME', 'TIME', 'ABLE',
            'LIFE', 'LOVE', 'LIVE', 'SELF', 'OVER', 'DONT',
            'WITH', 'WOULD', 'THERE', 'THEIR', 'WHAT', 'ABOUT',
            'WHICH', 'WHEN', 'THAN', 'THEN', 'MAKE', 'LIKE',
            'TIME', 'JUST', 'TAKE', 'PEOPLE', 'INTO', 'YEAR',
            'COULD', 'THEM', 'OTHER', 'LOOK', 'ONLY', 'COME',
            'THINK', 'ALSO', 'BACK', 'AFTER', 'WORK', 'FIRST',
            'WELL', 'EVEN', 'WANT', 'BECAUSE', 'CAUSE', 'THESE',
            'GIVE', 'MOST', 'PERSON', 'THING', 'WORLD', 'HAND',
            'PART', 'CHILD', 'WOMAN', 'WOMEN', 'PLACE', 'WEEK',
            'CASE', 'POINT', 'GOVERNMENT', 'COMPANY', 'NUMBER',
            'GROUP', 'PROBLEM', 'FACT', 'LAST', 'LONG', 'GREAT',
            'LITTLE', 'RIGHT', 'HIGH', 'DIFFERENT', 'SMALL', 'LARGE',
            'NEXT', 'EARLY', 'YOUNG', 'IMPORTANT', 'PUBLIC',
            'PRIVATE', 'SAME']

# some common scientific words, mainly containing common word endings
# compiled by me with help by:
# src: https://www.enchantedlearning.com/wordlist/science.shtml
WORDLIST_PROF = ['GRAPHY', 'OLOGY', 'MATH', 'SCIENCE', 'PROFESSOR',
                 'EXPERIMENT', 'WARE', 'THESIS', 'ATORY', 'THEORY',
                 'FIELD']

WORDLIST = WORDLIST_COMMON + WORDLIST_PROF


### AUXILIARY FUNCTIONS ###
def getNum(letter):
        '''Returns index of letter in the alphabet, starting with 0.'''
        return ord(letter) - ord('A')

def decToBin(n, size = 5):
    '''Returns a string binary representation of n in 5 binary places format.'''
    binary = ''
    while n >= 1:
        binary += str(n % 2)
        n = n // 2
    binary = binary[::-1]
    head = '0' * (size-len(binary))
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

def allBitSeq(n):
        '''Generator that returns all bit sequences from 0 to 2^n -1.
                Sequences will always have n places.'''
        seq = '0' * n
        yield seq
        for i in range(0, 2**n -1):
                d = int(binToDec(seq))
                d += 1
                seq = str(decToBin(d, n))
                yield seq

def wordToBits(w):
        bits = ''
        for c in w:
                b = decToBin(getNum(c))
                bits += b
        return bits

def breakInFive(b):
        '''Breaks bit sequence into groups of five.'''
        sez = []
        for i in range(len(b) // 5):
                group = b[5*i:5*i+5]
                sez.append(group)
        return sez

def bitsToWord(b):
        sez = breakInFive(b)
        w = ''
        for c in sez:
                try:
                        w += ALPHABET[binToDec(c)]
                except:
                        print('IndexOutOfBounds: Try a different key.')
                        return None
        return w

### ANALYSIS FUNCTIONS ###

def matching(seq1, seq2):
        '''Returns percentage of matching bits in the two sequences.'''
        if len(seq1) != len(seq2):
                print('MatchError: Sequences matched must be of same length.')
                return None
        count = 0
        for i in range(len(seq1)):
                if seq1[i] == seq2[i]:
                        count += 1
        return count / len(seq1)

### MAIN FUNCTIONS ###

def LFSR_1(s,n):
        '''Generates lfsr1 sequence with seed s of length n.
                Length of seed will always be 5 and n>5.
                x[i+5] = x[i+2] + x[i]'''
        zap = s
        for i in range(len(s),n):
                bit = (int(zap[i-2]) + int(zap[i-5])) % 2
                zap += str(bit)
        return zap

def LFSR_2(s,n):
        '''Generates lfsr2 sequence with seed s of length n.
                Length of seed will always be 7 and n>7.
                x[i+7] = x[i+1] + x[i]'''
        zap = s
        for i in range(len(s),n):
                bit = (int(zap[i-1]) + int(zap[i-7])) % 2
                zap += str(bit)
        return zap

def LFSR_3(s,n):
        '''Generates lfsr3 sequence with seed s of length n.
                Length of seed will always be 11 and n>11.
                x[i+11] = x[i+2] + x[i]'''
        zap = s
        for i in range(len(s),n):
                bit = (int(zap[i-2]) + int(zap[i-11])) % 2
                zap += str(bit)
        return zap

def Geffe(x1, x2, x3):
        '''Geffe's generator. Let x1, x2 and x3 be lfsr
                sequences of same length, generated
                by generators above. Then
                z = x1*x2 + x2*x3 + x3 (mod 2).'''
        zap = ''
        n = len(x1)
        if len(x1) != len(x2) or len(x1) != len(x3):
                print('GeneratorError: Lfsr sequences must be of same size.')
                return None
        for i in range(n):
                bit = int(x1[i])*int(x2[i]) + int(x2[i])*int(x3[i]) + int(x3[i])
                zap += str(bit % 2)
        return zap

def BreakGeffe(c):
        w = 'CRYPTOGRAPHY'
        b = wordToBits(w)
        n = len(b)
        z = xor(b, c[:len(b)])

        x1s = []
        for seed in allBitSeq(5):
                x = LFSR_1(seed, n)
                m_coef = matching(x, z)
##                print("Testing1: ", seed, m_coef)
                if m_coef > 0.7:
                        print('Success in LFSR1, seed: ', seed)
                        x1s.append(seed)

        x3s = []
        for seed in allBitSeq(11):
                x = LFSR_3(seed, n)
                m_coef = matching(x, z)
##                print("Testing3: ", seed, m_coef)
                if m_coef > 0.7:
                        print('Success in LFSR3, seed: ', seed)
                        x3s.append(seed)

        x2 = None
        for seed in allBitSeq(7):
                for x1 in x1s:
                        for x3 in x3s:
                                x = LFSR_2(seed, n)
                                z_cand = Geffe(LFSR_1(x1, n), x, LFSR_3(x3, n))
                                if z_cand == z:
                                        x2 = seed
                                        l = len(c)
                                        key = Geffe(LFSR_1(x1, l), LFSR_2(x2, l), LFSR_3(x3, l))
                                        plaintext = xor(c, key)
                                        print('Key found: ', x1, x2, x3)
                                        print('Decrypted text:')
                                        print(bitsToWord(plaintext))
                                        return (x1, x2, x3)
        print('DecipheringError: Something went wrong.')
        return None


### TESTS ###

file_name = 'geffe.txt'
ciphertext = ''
with open(file_name, 'r') as dat:
        ciphertext = dat.read()

BreakGeffe(ciphertext)
