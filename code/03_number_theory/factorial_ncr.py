MOD = 10**9 + 7


def build_factorials(n):
    fact = [1] * (n + 1)
    inv_fact = [1] * (n + 1)

    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact[n] = pow(fact[n], MOD - 2, MOD)

    for i in range(n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    return fact, inv_fact


def nCr(n, r, fact, inv_fact):
    if r < 0 or r > n:
        return 0

    return (
        fact[n]
        * inv_fact[r] % MOD
        * inv_fact[n - r] % MOD
    )


# Example:
# fact, inv_fact = build_factorials(2000)
# print(nCr(n, r, fact, inv_fact))
