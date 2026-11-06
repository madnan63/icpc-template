# BFS - shortest paths in an UNWEIGHTED graph (O(V + E)).
# 1-based nodes: graph[u] = [v1, v2, ...].
# Works for directed or undirected edges.
# dist[v] = -1 means unreachable; parent[v] = -1 for the source/unreached.

from collections import deque


def bfs(n, graph, start=1):
    dist = [-1] * (n + 1)
    parent = [-1] * (n + 1)
    q = deque([start])
    dist[start] = 0

    while q:
        u = q.popleft()
        for v in graph[u]:
            if dist[v] != -1:
                continue
            dist[v] = dist[u] + 1
            parent[v] = u
            q.append(v)

    return dist, parent


def bfs_path(parent, start, target):
    # Return the source-to-target path; [] if unreachable.
    path = []
    u = target
    while u != -1:
        path.append(u)
        if u == start:
            return path[::-1]
        u = parent[u]
    return []


# Example (undirected):
# graph = [[], [2, 3], [1, 4], [1], [2], []]
# dist, parent = bfs(5, graph, 1)
# print(dist[4])                 # 2
# print(bfs_path(parent, 1, 4))  # [1, 2, 4]
# print(dist[5])                 # -1
#
# Note: For non-negative weighted edges, use Dijkstra instead.
