### -IMPORTS- ###
from itertools import permutations

### -GLOBAL STRUCTURES- ###
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X',
            'Y', 'Z',]

L = len(ALPHABET)

# CALIBRATE AS NEEDED:
## frequency error (based on test example, should not exceed 0.005
TOL = 0.003
## at least how many common words should the text contain
WORD_TOL = 2

# frequency of letters in the English language (in %)
# source: http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
FREQUENCY = {'A': 8.12, 'B': 1.49, 'C': 2.71, 'D': 4.32, 'E': 12.02, 'F': 2.3,
             'G': 2.03, 'H': 5.92, 'I': 7.31, 'J': 0.1, 'K': 0.69, 'L': 3.98,
             'M': 2.61, 'N': 6.95, 'O': 7.68, 'P': 1.82, 'Q': 0.11, 'R': 6.02,
             'S': 6.28, 'T': 9.10, 'U': 2.88, 'V': 1.11, 'W': 2.09, 'X': 0.17,
             'Y': 2.11, 'Z': 0.07}

# some common words, add if needed
WORDLIST = ['THAT', 'THIS', 'ITIS', 'VERY', 'MANY', 'WITH',
            'HAVE', 'WILL', 'YOUR', 'FROM', 'THEY', 'KNOW',
            'BEEN', 'GOOD', 'MUCH', 'SOME', 'TIME', 'ABLE',
            'LIFE', 'LOVE', 'LIVE', 'SELF', 'OVER', 'DONT',
            'MATH']

### -AUXILIARY FUNCTIONS- ###


def giveWord():
        '''Generator of English 4-grams.'''
        for a in range(L):
                for b in range(L):
                        for c in range(L):
                                for d in range(L):
                                        A = ALPHABET[a]
                                        B = ALPHABET[b]
                                        C = ALPHABET[c]
                                        D = ALPHABET[d]
                                        word = A+B+C+D
                                        yield word


def getNum(letter):
        '''Returns index of letter in the alphabet, starting with 0.'''
        return ord(letter) - ord('A')

def extendedEuclid(a, b):
        '''Solve equation ax + by = gcd(a,b). Solution in tuple form (x, y, gcd).'''
        r1, r2, s1, s2, t1, t2 = a, b, 1, 0, 0, 1
        while r2 != 0:
                q = r1 // r2
                r = r1 - q * r2
                s = s1 - q * s2
                t = t1 - q * t2
                r1, r2, s1, s2, t1, t2 = r2, r, s2, s, t2, t
        return (s1 % L, t1 % L, r1)

def invEnt(ent):
	'''Multiplicative inverse of an element in Z_L'''
	return extendedEuclid(ent, L)[0]

def invKey(k):
	'''Inverse of 2x2 matrix [a,b;c,d]'''
	detK = k[0]*k[3] - k[1]*k[2]
	koef = invEnt(detK)
	inv = [koef*k[3] % L, (-1)*koef*k[1] % L, (-1)*koef*k[2] % L, koef*k[0] % L]
	return inv

# not needed in new version of the solution
def prodMat(A, B):
        '''Product A * B.'''
        a = (A[0] * B[0] + A[1] * B[2]) % L
        b = (A[0] * B[1] + A[1] * B[3]) % L
        c = (A[2] * B[0] + A[3] * B[2]) % L
        d = (A[2] * B[1] + A[3] * B[3]) % L
        return [a, b, c, d]

# not needed in new version of the solution
def isInvMat(A):
        '''Checks if the matrix given is invertible'''
        det = A[0] * A[3] - A[1] * A[2]
        return extendedEuclid(det, L)[2] == 1

### -ANALYSIS FUNCTIONS- ###

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

def integrityAnalysis(b):
        '''Checks the integrity of given text as a text written in English.'''
        index = frequencyAnalysis(b)
        if index > TOL:
                return False
        
        counter = 0
        for w in WORDLIST:
                if w in b:
                        counter += 1
        # calibrate this as needed
        if counter >= WORD_TOL:
                return True
        
        return False


def givePerm(k):
        '''Returns a list of key permutations.'''
        return [''.join(p) for p in permutations(k)]


### -MAIN FUNCTIONS- ###

def Encrypt(b, k):
	c = ''
	# add a letter if the length is not even
	if len(b) % 2 != 0:
		b += 'A'

	for i in range(len(b) // 2):
		letter1 = getNum(b[2*i])
		letter2 = getNum(b[2*i+1])
		# k is a matrix [a, b; c, d] given with a list of a [a, b, c, d] structure
		newLetter1 = ALPHABET[(getNum(k[0]) * letter1 + getNum(k[1]) * letter2) % L]
		newLetter2 = ALPHABET[(getNum(k[2]) * letter1 + getNum(k[3]) * letter2) % L]
		c = c + newLetter1 + newLetter2
	return c

def Decrypt(c, k):
	k_num = [getNum(k[0]), getNum(k[1]), getNum(k[2]), getNum(k[3])]
	key_num = invKey(k_num)
	key = [ALPHABET[key_num[0]], ALPHABET[key_num[1]],
               ALPHABET[key_num[2]], ALPHABET[key_num[3]]]
	return Encrypt(c, key)

def BreakHill(c):
        '''Decrypts the Hill cipher using most common 4-grams in the English language.
                The idea is to try all keys until the first one passes the threshold.
                Then frequencies are very similar between a couple of permutations of the
                initial key candidate, meaning we just have to test 4! = 24 possible keys
                and their corresponding plaintext candidates for common words.
                The most prominent second key candidate is also the matrix with switched
                columns, meaning the neighbour plaintext letters are merely transposed
                (so not ruining frequencies)(this was tested on the example given).
                Since the key matrix is ideally not composed of letters close together
                (lest it be too similar to the Vigenere cipher), this greatly reduces
                the number of keys tested.'''
        for key in giveWord():
                successflag = False
                # decrypt c using key candidate
                b = Decrypt(c, key)
                # frequency analysis of the plaintext candidate
                index = frequencyAnalysis(b)
                #print(index)
                if index <= TOL:
                        print('## FOUND KEY CANDIDATE: ', key)
                        k = key
                        print('## CHECKING PERMUTATIONS...')
                        for perm in givePerm(k):
                                btemp = Decrypt(c, list(perm))
                                if integrityAnalysis(btemp):
                                        print('## FOUND KEY: ', perm)
                                        k = perm
                                        success_flag = True
                                        break
                                else:
                                        print('## TESTED: ', perm, '...')
                        if success_flag:
                                break
        print('## DECRYPTED TEXT:')
        print(Decrypt(c, k))
        return (k, Decrypt(c, k))


### -TESTS- ###

c = 'STSQALWTCJMIJMTHNFEBWZTVJWMRNNHPMFICJFNWSZSXGW\
PFHHAJFBNTWZTVTHIRMRCGVRJTAFXBWDIVMFWSNSTVLXIR\
ACANWLYSIYVPJQMQNFLNMRPXSBHMWNJTIYNSZNHPHPIMNZ\
DRWBPPNSHMSBUJMUHZXJHMWPSQHHJBMHHMWMJTAFXBWDIC\
VETVLXIRANXFVETVUDWUHBWHEBMBSXHMWEEEHMANWUJUW\
WHAWWSNWZMLJXVXHWTVJTZZICACHHJTNWWTZRHWWTIYJSS\
UWSNSTVLWWWWHHPNSTVSNWWIYNSSOPFHMWEWHMHHMWNJTI\
YNSXPCQJTOQYFPBQKHMWEWHMHHMWNACHRNWHMWBSZWSIOG\
IICVETVLWWWWHHXANZRVZYWXUMVWZHDJHXAANHRUQZZOUN\
BTZTJFNSBUUMBVZSTTLHZXNWDTZELTVPPAJWTICVETVNNHPM\
FVZYWXUTVXBAJSQIUWWMHHMWNACHTGCTJIRGFCGVGSBYAPQI\
TSDWISVPPNNZMWCIRMSFRSXHMWZEENFGDVBMHSYOYJHPBHLA\
NXNNZVOSUSANTCVTVUMPSIATHYFAHEGCSPBWKNZMFWUYFIK\
XBMHHMWAAZWGJJAHSSWKVJANANXFVMAFSENLHMWBLZNDHM\
SBUJMNALWUFRSXWDMFWSVBTHLLJTYOSQWHYAGJHDJTXNNST\
VMXTVJH'

BreakHill(c)

