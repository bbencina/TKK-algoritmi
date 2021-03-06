### IMPORTS ###
from hashlib import sha1
from random import randint

### AUXILIARY FUNCTIONS ###

def extendedEuclid(a, b, n):
        '''Solve equation ax + by = gcd(a,b). Solution in tuple form (x, y, gcd).'''
        r1, r2, s1, s2, t1, t2 = a, b, 1, 0, 0, 1
        while r2 != 0:
                q = r1 // r2
                r = r1 - q * r2
                s = s1 - q * s2
                t = t1 - q * t2
                r1, r2, s1, s2, t1, t2 = r2, r, s2, s, t2, t
        return (s1 % n, t1 % n, r1)

def invEnt(ent, n):
	'''Multiplicative inverse of an element in Z_n'''
	return extendedEuclid(ent, n, n)[0]

### CRYPTOGRAPHIC FUNCTIONS ###

def sha1hash(s, encoding='utf-8'):
    '''Returns sha1 hash digest of s. On the internet some people
        recommend handling encoding as well.'''
    return sha1(s.encode(encoding)).hexdigest()

def MillerRabin(n, k = 10):
    '''Performs the Miller-Rabin primality test for n with a witness
        loop of k random numbers.'''
    # factoring out powers of 2
    n1 = n-1
    r = 0
    while n1 % 2 == 0:
        n1 = n1 // 2
        r += 1
    d = (n-1) // (2 ** r)
    #print(str(r), str(d))

    # witness loop start
    for i in range(k):
        # random potential witness
        a = randint(2, n-2)
        #print('Testing witness: ' + str(a))
        if extendedEuclid(a, n, n)[2] != 1:
            return False
        #print('Euclid passed...')
        x = pow(a, d, n)
        #print('Generated x...')
        if x == 1 or x == n-1:
            continue
        flag = False
        #print('Checking powers:', end='')
        for j in range(r-1):
            #print('.', end='')
            x = (x ** 2) % n
            if x == n-1:
                flag = True
                break
        #print(' ')
        if not flag:
            return False
    # probably a prime number - increase k or run again to be sure
    return True

def largePrime(b, tries=1000, mrt = 100):
    '''Generates large prime with b bits. Tries k times. Runs primality
        test with mrt random witnesses.'''
    for i in range(tries):
        n = randint(pow(2, b-1), pow(2, b)-1)
        if MillerRabin(n, mrt):
            return n
    return None
        

### MAIN FUNCTIONS ###

# refer to the tests section for some collision (bottom)
def FindCollision11(hs = {}):
    '''Finds 11-hexdec (44-bit) collision of the SHA1 hash function
        exploiting the birthday paradox.'''
    HDICT11 = hs

    # how many searches?
    # the birthday paradox tells us that a 44 bit collision
    # with a 0.5 probability requires approximately
    # N = 1.17*sqrt(2**44) = 5 000 000 hashes
    N = 5*10**6

    #order of search (10^o, 10^O)
    o = 0
    O = 10

    for i in range(N):
        # just some prints to see what is happening and how fast
        if i % 1000 == 0:
            print('.', end='')
        if i % 10000 == 0:
            print('#', end='')
        if i % 100000 == 0:
            print(str(i))
        # random collision candidate
        t = randint(10**o, 10**O)
        h = sha1hash(str(t))
        h11 = h[0:11]
    ##    print('Case ' + str(i) + ': value ' + str(t) + 'with h11 ' + str(h11))
        if h11 in HDICT11 and t != HDICT11[h11]:
            print('Success: ' + str(t) + ' ' + str(HDICT11[h11]))
            return((t, HDICT11[h11]))
        else:
            HDICT11[h11] = t
    return None

def DSA(x):
    '''Generates key for the DSA protocol and signs x.'''
    # generate public key
    print('Generating q and p...')
    while True:
        # generate 160-bit prime q
        q = largePrime(160)
        if q != None:
            pflag = False
            # p has to be 1024-bit and p-1 be divisible by q -> we look at multiples+1
            p = q * (2 ** (1024 - 160)) + 1
            while p < 2**1024:
                # q has to divide p-1
                print('.', end='')
                if MillerRabin(p, 100):
                    pflag = True
                    break
                p = p + q
            if pflag:
                break        
    print('\n')
    print('q: ' + str(q) + ' ' + str(len(bin(q))-2))
    print('p: ' + str(p) + ' ' + str(len(bin(p))-2))
    print('Generating alpha...')
    while True:
        h = randint(2, p-1)
        ee = extendedEuclid(h, p, p)
        # check if h if invertible in Z_p*
        if ee[2] != 1:
            continue
        else:
            alpha = pow(h, (p-1)//q, p)
            if alpha == 1:
                continue
            else:
                break
    print(str(alpha))
    # private key a
    print('Generating private a...')
    a = randint(2, q)
    print(str(a))
    print('Generating beta...')
    beta = pow(alpha, a, p)
    print(str(beta))

    # hashing
    print('Hashing message...')
    hx = sha1hash(str(x))
    hxi = int(hx, 16)
    print('Hash: ' + str(hx) + ' ' + str(hxi))

    print('Generating signature...')
    while True:
        k = randint(2, q-1)
        gamma = pow(alpha, k, p) % q
        invK = invEnt(k, q)
        delta = invK*(hxi + a*gamma) % q
        if gamma != 0 and delta != 0:
            print('Signature generated!')
            print(str(gamma), str(delta))
            return(x, gamma, delta, p, q, alpha, beta)

### TESTS ###
#FindCollision11()

# Success: 6177009668 7240624942
# Success: 8833925530 5823489626
# Success: 2892573859 5237488503
# Success: 892749168 8481945962
# Success: 6164887277 7267728681

(x, gamma, delta, p, q, alpha, beta) = DSA('6177009668 7240624942')

vpisna = '27161070'
hxi = int(sha1hash('6177009668 7240624942'), 16)
prevh = '000000039e94ec13109ac8832961a6840b43f96d'

block = '6177009668 7240624942 '+str(hxi)+'\n'
block += vpisna+' '+str(gamma)+' '+str(delta)+'\n'
block += prevh+'\n'

ext = 1
while True:
    if ext % 10000 == 0:
        print('*', end='')
    if ext % 100000 == 0:
        print(str(ext))
    h = sha1hash(block + str(ext))
    if str(h[0:7]) == '0000000' and str(h[7]) in {'0', '1', '2', '3'}:
        print('SUCCESS!')
        block = block + str(ext)+'\n'+str(h)
        break
    ext += 1

print('Public key:')
print(vpisna)
print(str(p))
print(str(q))
print(str(alpha))
print(str(beta))

print('Block:')
print(block)

#Used:
# block:
##6177009668 7240624942 710437724465732838796243150676983690084454713632
##27161070 35572740014273878021716376396641787002546353081 29541363177467477081296196340063174787441382956
##000000039e94ec13109ac8832961a6840b43f96d
##186497607
##0000000166eea041b704680d5fddabd399827b7d
#signature:
##27161070
##130634324975210040577730967482381803510443864245779770533903382165638782563027356020041956920601637310696184042384831272782060207357997100538591898082441211627715994476033254395721926161685395718968943742169610848790892507681699729170943557190591955302006274353914714393498292699749918190614696596908828051803
##1062040434712509181361880983616129505853767584167
##62591688097636237963315995010928382860532174891728112776508579489523314717852310083674680673369284002260088374012088426767718334326642900065759731047587968430860354713491255894280157538252872389781581209880771269729598354001093650883073640840347973424800946941676207981600436404113942974927952821214790324144
##38346466049004850340831541716113768091927660849743169407481645492304300205429359615264870087782788816209366355857827508431618857881017173190950281813973291611743631474591937396672859573432173123150494005220263201379293825957506942987952694550666369222895004495038490969950570073288136722890453105299629013018
