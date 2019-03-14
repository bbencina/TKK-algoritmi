ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F',
			'G', 'H', 'I', 'J', 'K', 'L',
			'M', 'N', 'O', 'P', 'Q', 'R',
			'S', 'T', 'U', 'V', 'W', 'X',
			'Y', 'Z',]

L = len(ALPHABET)

def getNum(letter):
	return ord(letter) - ord('A')

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

