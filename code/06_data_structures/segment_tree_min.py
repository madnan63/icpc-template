def build(arr):
    n = len(arr)
    size = 1

    while size < n:
        size *= 2

    tree = [float('inf')] * (2 * size)

    for i in range(n):
        tree[size + i] = arr[i]

    for i in range(size - 1, 0, -1):
        tree[i] = min(tree[2 * i], tree[2 * i + 1])

    return tree, size


def query(tree, size, l, r):
    # Inclusive range [l, r].
    l += size
    r += size

    ans = float('inf')

    while l <= r:
        if l % 2 == 1:
            ans = min(ans, tree[l])
            l += 1

        if r % 2 == 0:
            ans = min(ans, tree[r])
            r -= 1

        l //= 2
        r //= 2

    return ans


def update(tree, size, pos, val):
    pos += size
    tree[pos] = val
    pos //= 2

    while pos >= 1:
        tree[pos] = min(tree[2 * pos], tree[2 * pos + 1])
        pos //= 2
