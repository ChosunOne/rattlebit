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
def miller_rabin(n, k):
    b = n - 1
    r = 0

    # Find largest power of 2 factor
    while b % 2 == 0:
        r += 1
        b /= 2

    d = int((n - 1) / 2**r)
    for z in range(0, k):
        continue_witness = False
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for zz in range(0, r - 1):
            x = x**2 % n
            if x == 1:
                return False
            if x == n - 1:
                continue_witness = True
                break
        if not continue_witness:
            return False
    return True

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
    while jacobi(D, n) != -1:
        D = -(D + 2) if D > 0 else -(D - 2)
    return D

# Determine if n is a Lucas Probable Prime
def lucas_probable_prime(n, P, Q, D):
    pass

def is_prime(n):
        # Test by trial division
        if not trial_division(n, primes):
            return False

        # Check if number is a perfect square
        if is_square(n):
            return False

        # Run the Miller-Rabin Primality Test
        if not miller_rabin(n, 100):
            return False

        # Find D from the Jacobi Symbol and prepare for Lucas test
        D = find_jacobi(n)
        P = 1
        Q = (1 - D) / 4

        if not lucas_probable_prime(n, P, Q, D):
            return False

        return True

# Generate a big stongly probably prime
def gen_big_prime(bits, primes):
    n = random.getrandbits(bits)

    while not is_prime(n):
        n = random.getrandbits(bits)

    return n
