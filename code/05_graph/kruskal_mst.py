# KRUSKAL'S MINIMUM SPANNING TREE - O(E log E).
# UNDIRECTED weighted graph with vertices 1..n.
# edges = [(u, v, w), ...]; supports negative weights.
# Returns (MST total weight, chosen edges).
# If disconnected: returns (None, spanning-forest edges).
# Uses local DSU (path compression + union by size), no OOP.

def kruskal(n, edges):
    parent = list(range(n + 1))
    sz = [1] * (n + 1)

    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u

    total = 0
    chosen = []

    for u, v, w in sorted(edges, key=lambda e: e[2]):
        a, b = find(u), find(v)
        if a == b:
            continue
        if sz[a] < sz[b]:
            a, b = b, a
        parent[b] = a
        sz[a] += sz[b]
        total += w
        chosen.append((u, v, w))

        if len(chosen) == n - 1:
            break

    if len(chosen) != n - 1:
        return None, chosen
    return total, chosen


# Example:
# edges = [(1,2,4), (1,3,1), (2,3,2), (2,4,3), (3,4,7)]
# cost, mst_edges = kruskal(4, edges)
# print(cost)  # 6
# print(mst_edges)  # [(1,3,1), (2,3,2), (2,4,3)]
#
# A spanning tree has exactly n-1 selected edges.
# Kruskal is for undirected graphs, not directed shortest paths.
