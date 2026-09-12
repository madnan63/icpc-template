N = 200005

bit = [0] * (N + 1)


def update(i, val):
    while i <= N:
        bit[i] += val
        i += i & -i


def query(i):
    ans = 0

    while i > 0:
        ans += bit[i]
        i -= i & -i

    return ans


def range_query(l, r):
    return query(r) - query(l - 1)
