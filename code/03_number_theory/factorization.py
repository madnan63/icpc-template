from collections import defaultdict
from math import isqrt


def factors(n):
    fact = defaultdict(int)

    while n % 2 == 0:
        fact[2] += 1
        n //= 2

    p = 3
    while p <= isqrt(n):
        while n % p == 0:
            fact[p] += 1
            n //= p
        p += 2

    if n > 1:
        fact[n] += 1

    return fact


def num_divisors(n):
    fact = factors(n)
    ans = 1

    for power in fact.values():
        ans *= power + 1

    return ans


def sum_divisors(n):
    fact = factors(n)
    ans = 1

    for p, power in fact.items():
        ans *= (p ** (power + 1) - 1) // (p - 1)

    return ans
