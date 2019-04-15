### IMPORTS ###
import time

### GLOBAL STRUCTURES ###
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X',
            'Y', 'Z',]

L = len(ALPHABET)

# tolerance for frequency analysis - calibrate as needed
TOL = 0.05

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
                 'WARE', 'THESIS', 'ATORY', 'THEORY',
                 'FIELD', 'CATION', 'GRAPH', 'INFORMATION']

WORDLIST = WORDLIST_COMMON + WORDLIST_PROF

# the wordlist should have longer words first, as they are more reliable
# statistically and consume less iterations through text
WORDLIST.sort(key = lambda s:len(s))
WORDLIST = WORDLIST[::-1]


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
        '''Turns letters into a bit sequence of 5 bits per letter.'''
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
        '''Inverse of wordToBits. Suppose every letter takes 5 bits of space.
                Turns such bit sequences back into letters.'''
        sez = breakInFive(b)
        w = ''
        for c in sez:
                try:
                        w += ALPHABET[binToDec(c)]
                except:
##                        print('IndexOutOfBounds: Try a different key.')
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

def frequencyAnalysis(b):
        '''Returns index of error of given text based on the known frequencies
                of letters in the English language.'''
        frequencies = {}
        for letter in ALPHABET:
                frequencies[letter] = 0
        for l in b:
                frequencies[l] += 1
        index = 0
        for l in ALPHABET:
                index += (FREQUENCY[l] / 100 - frequencies[l] / len(b)) ** 2
        return index

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

# NOTES:
# - The main difference between the memory-heavy and time-heavy version is
#   that the memory heavy version generates all lfsr sequences  prior to
#   the correlation attack but then only searches through them using
#   a native hash map implementation (dictionary) whereas the time-heavy
#   version generates sequences of necesarry length during the attack.
# - One of main consequences of this is that the memory-heavy version
#   works fast on longer words (hence the sorting of the wordlist by
#   length in descending order), yet works painfully slow on slow words.
#   The time-heavy version works with about the same speed regardless
#   of word length but is a bit slower on average.

# time-heavy version
def BreakGeffe(c, WLIST = WORDLIST):
        '''Performs a know-plaintext correlation attack on the Geffe generator.
                Rolls every word in the wordlist through the ciphertext,
                calculates the key candidate and uses the statistical weakness
                of the generator function to calculate the key.
                We notice the plaintext guess was wrong when turning bits to
                letters leads to an indexation error or with the help of
                frequency analysis.
                If the wordlist contains only one word we know for sure is at the
                very begining of the text, this function is equivalent to a basic
                correlation attack. Thus as we know the word 'CRYPTOGRAPHY' is the
                first word of our plaintext, one can substitute WORDLIST for
                ['CRYPTOGRAPHY'] and yield positive results.'''
        for w in WLIST:
                b = wordToBits(w)
                n = len(b)
                # if the word is longer than the ciphertext then it's surely not
                # in the text
                if len(c) < n:
                        continue
                print('Testing word: ', w)
                # rolling the word over the ciphertext
                for i in range(len(c)//5 - n//5 + 1):
                        print('.', end='')
                        # key candidate at the current marker of length n
                        z = xor(b, c[i*5:n+i*5])

                        # correlation attack:
                        # which x1 match z cca. 3/4 of the time?
                        x1s = []
                        for seed in allBitSeq(5):
                                x = LFSR_1(seed, n+i*5)
                                m_coef = matching(x[i*5:n+i*5], z)
                ##                print("Testing1: ", seed, m_coef)
                                if m_coef > 0.7:
##                                        print('Success in LFSR1, seed: ', seed)
                                        x1s.append(seed)

                        # which x3 match z cca. 3/4 of the time?
                        x3s = []
                        for seed in allBitSeq(11):
                                x = LFSR_3(seed, n+i*5)
                                m_coef = matching(x[i*5:n+i*5], z)
                ##                print("Testing3: ", seed, m_coef)
                                if m_coef > 0.74:
##                                        print('Success in LFSR3, seed: ', seed)
                                        x3s.append(seed)

                        # now for the final key piece: x2
                        x2 = None
                        for seed in allBitSeq(7):
                                for x1 in x1s:
                                        for x3 in x3s:
                                                x = LFSR_2(seed, n+i*5)
                                                # make key candidate for current (x1, x2, x3)
                                                z_cand = Geffe(LFSR_1(x1, n+i*5), x, LFSR_3(x3, n+i*5))
                                                # does it match the guessed key?
                                                if z_cand[i*5:n+i*5] == z:
                                                        x2 = seed
                                                        l = len(c)
                                                        # make key for the whole ciphertext
                                                        key = Geffe(LFSR_1(x1, l), LFSR_2(x2, l), LFSR_3(x3, l))
                                                        # decrypt with calculated key
                                                        plaintext_bit = xor(c, key)
                                                        # check for errors
                                                        try:
                                                                # does it transate to letters?
                                                                # not all bit combinations are valid
                                                                # as an alphabet index
                                                                plaintext = bitsToWord(plaintext_bit)
                                                                # if it succeded, check if the language
                                                                # is English
                                                                index = frequencyAnalysis(plaintext)
                                                                if index > TOL:
                                                                        continue
                                                        except:
                                                                continue
                                                        # if all is well then return
                                                        print('\nKey found: ', x1, x2, x3)
                                                        print('Decrypted text:')
                                                        print(plaintext)
                                                        return (x1, x2, x3, plaintext)
        print('DecipheringError: Something went wrong. Try updating the wordlist or lowering the tolerance.')
        return None

# memory-heavy version
def BreakGeffe2(c, WLIST = WORDLIST):
        '''Performs a know-plaintext correlation attack on the Geffe generator.
                Rolls every word in the wordlist through the ciphertext,
                calculates the key candidate and uses the statistical weakness
                of the generator function to calculate the key.
                We notice the plaintext guess was wrong when turning bits to
                letters leads to an indexation error or with the help of
                frequency analysis.
                If the wordlist contains only one word we know for sure is at the
                very begining of the text, this function is equivalent to a basic
                correlation attack. Thus as we know the word 'CRYPTOGRAPHY' is the
                first word of our plaintext, one can substitute WORDLIST for
                ['CRYPTOGRAPHY'] and yield positive results.'''
        print('Generating lfsr sequences...')
        lfsr1 = {}
        lfsr2 = {}
        lfsr3 = {}
        for seed in allBitSeq(5):
                x = LFSR_1(seed, len(c))
                lfsr1[seed] = x
        for seed in allBitSeq(7):
                x = LFSR_2(seed, len(c))
                lfsr2[seed] = x
        for seed in allBitSeq(11):
                x = LFSR_3(seed, len(c))
                lfsr3[seed] = x
        for w in WLIST:
                b = wordToBits(w)
                n = len(b)
                # if the word is longer than the ciphertext then it's surely not
                # in the text
                if len(c) < n:
                        continue
                print('Testing word: ', w)
                # rolling the word over the ciphertext
                for i in range(len(c)//5 - n//5 + 1):
                        print('.', end='')
                        # key candidate at the current marker of length n
                        z = xor(b, c[i*5:n+i*5])

                        # correlation attack:
                        # which x1 match z cca. 3/4 of the time?
                        x1s = []
                        for s in lfsr1:
                                m_coef = matching(lfsr1[s][i*5:n+i*5], z)
                ##                print("Testing1: ", seed, m_coef)
                                if m_coef > 0.7:
##                                        print('Success in LFSR1, seed: ', seed)
                                        x1s.append(s)

                        # which x3 match z cca. 3/4 of the time?
                        x3s = []
                        for s in lfsr3:
                                m_coef = matching(lfsr3[s][i*5:n+i*5], z)
                ##                print("Testing3: ", seed, m_coef)
                                if m_coef > 0.74:
##                                        print('Success in LFSR3, seed: ', seed)
                                        x3s.append(s)

                        # now for the final key piece: x2
                        x2 = None
                        for s in lfsr2:
                                for s1 in x1s:
                                        for s3 in x3s:
                                                # make key candidate for current (x1, x2, x3)
                                                z_cand = Geffe(lfsr1[s1], lfsr2[s], lfsr3[s3])
                                                # does it match the guessed key?
                                                if z_cand[i*5:n+i*5] == z:
                                                        l = len(c)
                                                        # make key for the whole ciphertext
                                                        key = z_cand
                                                        # decrypt with calculated key
                                                        plaintext_bit = xor(c, key)
                                                        # check for errors
                                                        try:
                                                                # does it transate to letters?
                                                                # not all bit combinations are valid
                                                                # as an alphabet index
                                                                plaintext = bitsToWord(plaintext_bit)
                                                                # if it succeded, check if the language
                                                                # is English
                                                                index = frequencyAnalysis(plaintext)
                                                                if index > TOL:
                                                                        continue
                                                        except:
                                                                continue
                                                        # if all is well then return
                                                        print('\nKey found: ', s1, s, s3)
                                                        print('Decrypted text:')
                                                        print(plaintext)
                                                        return (s1, s, s3, plaintext)
                print('\n')
        print('DecipheringError: Something went wrong. Try updating the wordlist or lowering the tolerance.')
        return None


### TESTS ###

file_name = 'geffe.txt'
ciphertext = ''
with open(file_name, 'r') as dat:
        ciphertext = dat.read()

# FIRST THE MEMORY-HEAVY VERSION
# works great on longer words but is painfully slow on shorter ones

# proof it works
print('## TEST 1:')
BreakGeffe2(ciphertext, ['CRYPTOGRAPHY'])

# longer words
print('## TEST 2:')
BreakGeffe2(ciphertext)

# SECOND THE TIME-HEAVY VERSION

# proof it works
print('## TEST 3:')
BreakGeffe(ciphertext, ['CRYPTOGRAPHY'])


# Interesting:
# While attacking with the word 'prior' did not yield positive results,
# the word 'the' succeded almost instantly (first occurance) despite being
# only 3 letters long and not at all specific to the text.
print('## TEST 4:')
BreakGeffe(ciphertext, ['THE'] + WORDLIST)

# if you like waiting
print('## TEST 5:')
BreakGeffe(ciphertext)
