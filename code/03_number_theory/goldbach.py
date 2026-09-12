def goldbach(n, is_prime):
    # is_prime should be a sieve/list where is_prime[x]
    # tells whether x is prime.
    if n < 4 or n % 2 != 0:
        return None

    for p in range(2, n // 2 + 1):
        if is_prime[p] and is_prime[n - p]:
            return p, n - p

    return None
