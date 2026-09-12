# Pattern: F F F F T T T T
# Finds the minimum x for which check(x) is True.

def check(x):
    return ...

l = ...
r = ...
ans = -1

while l <= r:
    m = (l + r) // 2

    if check(m):
        ans = m
        r = m - 1
    else:
        l = m + 1

print(ans)
