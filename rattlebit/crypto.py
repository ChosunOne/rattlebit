import random
import math

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
def miller_rabin(n, k, primes):
    if n < 2: return False
    for p in primes:
        if n < p * p: return True
        if n % p == 0: return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
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
    digits = list(map(int, str(bin(k))[2:]))
    subscript = 1
    for digit in digits[1:]:
        U, V = U*V % n, (pow(V, 2, n) - 2*pow(Q, subscript, n)) % n
        subscript *= 2
        if digit == 1:
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

    for r in xrange(s):
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
        if not trial_division(n, primes):
            return False

        # Check if number is a perfect square
        if is_square(n):
            return False

        # Run the Miller-Rabin Primality Test
        if not miller_rabin(n, 128, primes):
            return False

        # Run the Lucas Probable Prime Test
        if not lucas_probable_prime(n):
            return False

        return True

# Generate a big stongly probable prime
def gen_big_prime(bits):
    n = random.getrandbits(bits)
    primes = primes_sieve(1000)

    tries = 0
    while not is_prime(n, primes):
        n = random.getrandbits(bits)
        tries += 1
        if tries % 100 == 0:
            print(tries, n)

    return n

zz = gen_big_prime(256)
zzz = gen_big_prime(3072)
print()