# Pattern: T T T T F F F F
# Finds the maximum x for which check(x) is True.

def check(x):
    return ...

l = ...
r = ...
ans = -1

while l <= r:
    m = (l + r) // 2

    if check(m):
        ans = m
        l = m + 1
    else:
        r = m - 1

print(ans)
