from array import array

LIMIT = 10**6 + 7


def sieve_bytearray(n):
    # Index i represents odd number 2*i + 1.
    size = (n + 1) // 2
    sieve = bytearray(b"\x01") * size

    if size:
        sieve[0] = 0  # 1 is not prime

    limit = int(n**0.5)

    for p in range(3, limit + 1, 2):
        if sieve[p // 2]:
            start = (p * p) // 2
            count = ((size - 1 - start) // p) + 1
            sieve[start::p] = b"\x00" * count

    return sieve


a = sieve_bytearray(LIMIT)

primes = array('I')

if LIMIT >= 2:
    primes.append(2)

for i in range(1, len(a)):
    if a[i]:
        primes.append(2 * i + 1)


def is_prime(x):
    # Requires x <= LIMIT.
    if x == 2:
        return True
    if x < 2 or x % 2 == 0:
        return False

    return bool(a[x // 2])
