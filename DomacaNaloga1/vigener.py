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

FREQ = 0.065


def getNum(letter):
	return ord(letter) - ord('A')


def partText(b, n):
	partition = [''] * n
	for i in range(len(b)):
		partition[i % n] += b[i]
	return partition

def indexOfCor(txt):
	ents = {}
	for i in range(len(txt)):
		if txt[i] in ents:
			ents[txt[i]] += 1
		else:
			ents[txt[i]] = 1
	index = 0
	for ent in ents:
		index += (ents[ent]/len(txt)) ** 2
	return index

def Encrypt(b, k):
	c = ''
	for i in range(len(b)):
		key = getNum(k[i % len(k)])
		letter = getNum(b[i])
		newLetter = ALPHABET[(letter + key) % L]
		c += newLetter
	return c

def Decrypt(c, k):
	b = ''
	for i in range(len(c)):
		key = getNum(k[i % len(k)])
		letter = getNum(c[i])
		newLetter = ALPHABET[(L + letter - key) % L]
		b += newLetter
	return b

def findKeyLen(c):
	for i in range(1, len(c)+1):
		partition = partText(c, i)
		flag = False
		for j in range(i):
			ic = indexOfCor(partition[j])
			if ic > FREQ:
				flag = True
			else:
				flag = False
				break
		if flag:
			return i
	return None

def BreakVigenere(c):
	keyLen = findKeyLen(c)
	partition = partText(c, keyLen)
	key = ''
	for part in partition:
		frequenies = {}
		for letter in ALPHABET:
			frequenies[letter] = 0
		indexOfError = 100
		error = ''
		for k in ALPHABET:
			dec = Decrypt(part, k)
			for letter in dec:
				frequenies[letter] += 1
			index = 0
			for l in ALPHABET:
				index += (FREQUENCY[l] / 100 - frequenies[l] / len(part)) ** 2
			if index < indexOfError:
				indexOfError = index
				error = k
			for letter in ALPHABET:
				frequenies[letter] = 0
		key += error
	return key, Decrypt(c, key)
