ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F',
			'G', 'H', 'I', 'J', 'K', 'L',
			'M', 'N', 'O', 'P', 'Q', 'R',
			'S', 'T', 'U', 'V', 'W', 'X',
			'Y', 'Z',]

L = len(ALPHABET)

def getNum(letter):
	return ord(letter) - ord('A')

def extendedEuclid(a, b):
        '''Reši enačbo ax + by = gcd(a,b). Poda rešitev v obliki (x, y, gcd).'''
        r1, r2, s1, s2, t1, t2 = a, b, 1, 0, 0, 1
        while r2 != 0:
                q = r1 // r2
                r = r1 - q * r2
                s = s1 - q * s2
                t = t1 - q * t2
                r1, r2, s1, s2, t1, t2 = r2, r, s2, s, t2, t
        return (s1 % L, t1 % L, r1)

def invEnt(ent):
	# multiplikativni inverz elementa v Z_L
	return extendedEuclid(ent, L)[0]

def invKey(k):
	# inverz 2x2 matrike [a,b;c,d]
	detK = k[0]*k[3] - k[1]*k[2]
	koef = invEnt(detK)
	inv = [koef*k[3] % L, (-1)*koef*k[1] % L, (-1)*koef*k[2] % L, koef*k[0] % L]
	return inv


def Encrypt(b, k):
	c = ''
	# podaljšamo besedilo, če ne ustreza kluču
	if len(b) % 2 != 0:
		b += 'A'

	for i in range(len(b) // 2):
		letter1 = getNum(b[2*i])
		letter2 = getNum(b[2*i+1])
		# k je matrika [a, b; c, d], podana s seznamom [a, b, c, d]
		newLetter1 = ALPHABET[(getNum(k[0]) * letter1 + getNum(k[1]) * letter2) % L]
		newLetter2 = ALPHABET[(getNum(k[2]) * letter1 + getNum(k[3]) * letter2) % L]
		c = c + newLetter1 + newLetter2
	return c

def Decrypt(c, k):
	k_num = [getNum(k[0]), getNum(k[1]), getNum(k[2]), getNum(k[3])]
	key_num = invKey(k_num)
	key = [ALPHABET[key_num[0]], ALPHABET[key_num[1]], ALPHABET[key_num[2]], ALPHABET[key_num[3]]]
	return Encrypt(c, key)
