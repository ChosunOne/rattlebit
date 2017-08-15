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

# Generate the kth term of the Lucas Sequence (inefficient but right)
def lucas_term_u(P, Q, k):
    U = [0, 1]
    for x in range(2, k + 1):
        term = P * U[x - 1] - Q * U[x - 2]
        U += [int(term)]
    return U

# Generate the 2k+1 term of the Lucas sequence U
def lucas_term_u_2k1(D, P, Q, U, V, k):
    double_u = lucas_term_u_double(U, V)
    double_v = lucas_term_v_double(V, Q,k)
    term = int((P * double_u + double_v) / 2)
    return term
    
# Calculate the 2kth term of the Lucas sequence U
def lucas_term_u_double(U, V):
    term = int(U * V)
    return term

# Generate the 2k+1 term of the Lucas sequence V
def lucas_term_v_2k1(D, P, Q, U, V, k):
    double_u = lucas_term_u_double(U, V)
    double_v = lucas_term_v_double(V, Q, k)
    term = int((D * double_u + P * double_v) / 2)
    return term

# Calculate the 2kth term of the Lucas sequence V
def lucas_term_v_double(V, Q, k):
    term = int(pow(V, 2) - 2 * pow(Q, k))
    return term

# Calculate the required terms to reach needed term
def calc_terms(n):
    binary = "{0:b}".format(n)
    terms = [1]
    term = 1
    for x in range(1, len(binary)):
        bit = binary[x]
        if bit == '0':
            term *= 2
        else:
            term *= 2
            terms += [term]
            term += 1
        terms += [term]
    return terms

# Determine if n is a Lucas Probable Prime
def lucas_probable_prime(n):
    if 0 < n < 4:
        return True

    # Find D from the Jacobi Symbol and prepare for Lucas test
    D = find_jacobi(n)
    P = 1
    Q = (1 - D) / 4
    Dn = n + 1

    # Setup computation accelerated by binary expansion of terms
    binary = "{0:b}".format(Dn)
    U = 1
    V = P
    k = 1

    # TODO: Delete Debug counters
    debug_terms = [1]
    debug_u = [U]
    debug_v = [V]
    debug_u_correct = [U]

    # Find the Un+1 and Vn+1 terms of the Lucas Sequence
    for x in range(1, len(binary)):
        bit = binary[x]
        if bit == '0':
            U = lucas_term_u_double(U, V)
            V = lucas_term_v_double(V, Q, k)
            k *= 2
            debug_terms += [k]
            debug_u += [U]
            debug_v += [V]
            debug_u_correct += [lucas_term_u(P, Q, k)[-1]]
        else:
            old_U = U
            U = lucas_term_u_2k1(D, P, Q, U, V, k)
            V = lucas_term_v_2k1(D, P, Q, old_U, V, k)
            debug_u += [U]
            debug_v += [V]
            k *= 2
            debug_terms += [k]
            k += 1
            debug_terms += [k]
            debug_u_correct += [lucas_term_u(P, Q, k)[-1]]
    
    test = pow(U, 1, n)

    if test != 0:
        return False

    #if V % n != 2 * Q:
        #return False

    return True
            
primes = [x for x in primes_sieve(1000)]
bad = False
for p in primes:
    if not lucas_probable_prime(p):
        bad = True

print()
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

        # Run the Lucas Probable Prime Test
        if not lucas_probable_prime(n):
            return False

        return True

# Generate a big stongly probably prime
def gen_big_prime(bits, primes):
    n = random.getrandbits(bits)

    while not is_prime(n):
        n = random.getrandbits(bits)

    return n
