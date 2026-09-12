def bin_exp(a, b):
    result = 1

    while b > 0:
        if b % 2 == 1:
            result *= a

        a *= a
        b //= 2

    return result


def bin_exp_mod(a, b, mod):
    result = 1
    a %= mod

    while b > 0:
        if b % 2 == 1:
            result = result * a % mod

        a = a * a % mod
        b //= 2

    return result
