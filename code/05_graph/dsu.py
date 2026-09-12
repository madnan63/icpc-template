parent = []
size = []


def dsu_init(n):
    global parent, size

    parent = list(range(n + 1))
    size = [1] * (n + 1)


def find(u):
    root = u

    while parent[root] != root:
        root = parent[root]

    while u != root:
        nxt = parent[u]
        parent[u] = root
        u = nxt

    return root


def union(u, v):
    u = find(u)
    v = find(v)

    if u == v:
        return False

    if size[u] < size[v]:
        u, v = v, u

    parent[v] = u
    size[u] += size[v]

    return True
