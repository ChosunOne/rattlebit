import random
import math
import time

# Bitcoin Parameters
BITCOIN_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC2F  
BITCOIN_A = 0
BITCOIN_B = 7
BITCOIN_G = 0x0279BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
BITCOIN_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
BITCOIN_H = 1


# Sieve of Eratosthenes
def primes_sieve(limit):
    a = [True] * limit                          # Initialize the primality list
    a[0] = a[1] = False

    for (i, isprime) in enumerate(a):
        if isprime:
            yield i
            for n in range(i*i, limit, i):     # Mark factors non-prime
                a[n] = False

# Quick test by trial division of small primes
def trial_division(n, primes):
    for x in primes:
        if n % x == 0:
            return False
    return True

# Miller-Rabin Primality Test
def miller_rabin(n, k):
    # Optimization Variables
    rrange = random.randrange
    m = n - 1

    if n < 2:
        return False
    r, s = 0, m
    while not s & 1:
        r += 1
        s //= 2
    for _ in range(k):
        a = rrange(2, m)
        x = pow(a, s, n)
        if x == 1 or x == m:
            continue
        for __ in range(r - 1):
            x = pow(x, 2, n)
            if x == m:
                break
        else:
            return False
    return True

# Find the integer square root of a number
def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

# Check if number is a perfect square
def is_square(n):
    if isqrt(n)**2 == n:
        return True
    else:
        return False

# Return the Jacobi Symbol of two numbers
def jacobi(D, n):
    if n <= 0 or n % 2 == 0:
        return 0
    j = 1
    if D < 0:
        D = -D
        if n % 4 == 3:
            j = -j
    while D != 0:
        while D % 2 == 0:
            D /= 2
            if n % 8 == 3 or n % 8 == 5:
                j = -j
        D, n = n, D
        if D % 4 == 3 and n % 4 == 3:
            j = -j
        D = D % n
    if n == 1:
        return j
    else:
        return 0

# Find the first D that is == -1 for n
def find_jacobi(n):
    D = 5
    if n % 2 == 0:
        return 0
    while jacobi(D, n) != -1:
        D = -(D + 2) if D > 0 else -(D - 2)
    return D

def U_V_subscript(k, n, U, V, P, Q, D):
    k, n, U, V, P, Q, D = map(int, (k, n, U, V, P, Q, D))
    digits = bin(k)[2:]
    subscript = 1
    ___ = 0
    for digit in digits[1:]:
        ___ += 1
        if ___ % 25 == 0: print(___)
        U = U*V % n
        V = (pow(V, 2, n) - 2*pow(Q, subscript, n)) % n
        subscript *= 2
        if digit == '1':
            if not (P*U + V) & 1:
                if not (D*U + P*V) & 1:
                    U, V = (P*U + V) >> 1, (D*U + P*V) >> 1
                else:
                    U, V = (P*U + V) >> 1, (D*U + P*V + n) >> 1
            elif not (D*U + P*V) & 1:
                U, V = (P*U + V + n) >> 1, (D*U + P*V) >> 1
            else:
                U, V = (P*U + V + n) >> 1, (D*U + P*V + n) >> 1
            subscript += 1
            U, V = U % n, V % n
    return U, V

def lucas_pp(n, D, P, Q):                                                                                                                                                                                                                         
    """Perform the Lucas probable prime test"""
    U, V = U_V_subscript(n+1, n, 1, P, P, Q, D)

    if U != 0:
        return False

    d = n + 1
    s = 0
    while not d & 1:
        d = d >> 1
        s += 1

    U, V = U_V_subscript(n+1, n, 1, P, P, Q, D)

    if U == 0:
        return True

    for r in range(s):
        U, V = (U*V) % n, (pow(V, 2, n) - 2*pow(Q, d*(2**r), n)) % n
        if V == 0:
            return True

    return False

# Determine if n is a Lucas Probable Prime
def lucas_probable_prime(n):
    if 0 < n < 4:
        return True

    # Find D from the Jacobi Symbol and prepare for Lucas test
    D = find_jacobi(n)
    P = 1
    Q = int((1 - D) / 4)

    return lucas_pp(n, D, P, Q)

def is_prime(n, primes):
    # Test by trial division
    trial = trial_division(n, primes)
    if not trial:
        return False

    # Check if number is a perfect square
    square = is_square(n)
    if square:
        return False

    # Run the Miller-Rabin Primality Test
    start = time.time()
    miller_rabin_prime = miller_rabin(n, 64)
    print('Miller-Rabin: {}'.format(time.time() - start))
    if not miller_rabin_prime:
        return False

    # Run the Lucas Probable Prime Test
    start = time.time()
    lucas = lucas_probable_prime(n)
    print('Lucas: {}'.format(time.time() - start))
    if not lucas:
        return False

    return True

# Generate a big stongly probable prime
def gen_big_prime(bits):
    n = random.getrandbits(bits)
    primes = primes_sieve(100000)
    prime = False

    tries = 0
    while not prime:
        prime = is_prime(n, primes)
        n = random.getrandbits(bits)

    return n

# Add two points for ECC
def point_add(p, x1, x2, y1, y2):
    λ = (y2 - y1 / x2 - x1) % p
    x3 = (λ**2 - x1 - x2) % p
    y3 = (λ * (x1 - x3) - y1) % p
    return (x3, y3)

# Double a point for ECC
def point_double(p, a, x, y):
    λ = ((3 * x**2 + a)/(2 * y)) % p
    x3 = (λ**2 - 2 * x) % p
    y3 = (λ * (x - x3) - y) % p
    return (x3, y3)

# Generate an ECDSA public key from a private key with given curve parameters
def ec_pub_key(priv_key, p, a, b, G, n, h):
    pass

    