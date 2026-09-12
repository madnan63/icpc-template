def is_prime_miller_rabin(n):
    if n < 2:
        return False

    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)

    for p in small_primes:
        if n % p == 0:
            return n == p

    d = n - 1
    r = 0

    while d % 2 == 0:
        d //= 2
        r += 1

    # Deterministic for 64-bit integers.
    bases = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)

    for a in bases:
        if a % n == 0:
            continue

        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = x * x % n

            if x == n - 1:
                break
        else:
            return False

    return True
