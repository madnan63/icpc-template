# BIPARTITE CHECK / BFS 2-COLORING - O(V + E).
# Undirected graph, vertices 1..n; graph[u] = [neighbors].
# Handles disconnected components, odd cycles and self-loops.
# Colors: -1 = unvisited, 0/1 = opposite partitions.

from collections import deque


def bipartite_coloring(n, graph):
    # Return color array, or None if the graph is not bipartite.
    color = [-1] * (n + 1)

    for start in range(1, n + 1):
        if color[start] != -1:
            continue
        color[start] = 0
        q = deque([start])

        while q:
            u = q.popleft()
            for v in graph[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return None

    return color


def is_bipartite(n, graph):
    return bipartite_coloring(n, graph) is not None


# Example:
# graph = [[], [2, 3], [1, 4], [1, 4], [2, 3]]
# print(is_bipartite(4, graph))  # True
# print(bipartite_coloring(4, graph))  # e.g. [-1,0,1,1,0]
#
# A graph is bipartite iff it has no odd cycle.
# Use the colors to construct the two vertex groups.
