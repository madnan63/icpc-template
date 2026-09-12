from math import isqrt

N = 10**6 + 9

spf = list(range(N + 1))

for i in range(2, isqrt(N) + 1):
    if spf[i] == i:
        for j in range(i * i, N + 1, i):
            if spf[j] == j:
                spf[j] = i


def factorize(n):
    res = []

    while n > 1:
        p = spf[n]
        res.append(p)
        n //= p

    return res


# Example for many queries:
# q = int(input())
# for _ in range(q):
#     n = int(input())
#     print(factorize(n))
