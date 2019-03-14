ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F',
			'G', 'H', 'I', 'J', 'K', 'L',
			'M', 'N', 'O', 'P', 'Q', 'R',
			'S', 'T', 'U', 'V', 'W', 'X',
			'Y', 'Z',]

L = len(ALPHABET)

def getNum(letter):
	return ord(letter) - ord('A')

def invEnt(ent):
	# multiplikativni inverz elementa v Z_L

def invKey(k):
	# inverz 2x2 matrike [a,b;c,d]


def Encrypt(b, k):
	c = ''
	# podaljšamo besedilo, če ne ustreza kluču
	if b % 2 != 0:
		b += 'A'
	
	for i in range(len(b) // 2):
		letter1 = getNum(b[2*i])
		letter2 = getNum(b[2*i+1])
		# k je matrika [a, b; c, d], podana s seznamom [a, b, c, d]
		newLetter1 = ALPHABET[(getNum(k[0]) * letter1 + getNum(k[1]) * letter2) % L]
		newLetter2 = ALPHABET[(getNum(k[2]) * letter1 + getNum(k[3]) * letter2) % L]
		c = c + newLetter1 + newLetter2
	
	return c