# GENERAL ITERATIVE DFS - O(V + E), 1-based vertices.
# graph[u] = [neighbors]; directed or undirected.
# Returns DFS visit order, parent array, depth array (0 at start).
# Unreachable vertices have parent = depth = -1.
# Mark visited ON POP; reversed neighbors give recursive-style order.

def dfs(n, graph, start=1):
    seen = [False] * (n + 1)
    parent = [-1] * (n + 1)
    depth = [-1] * (n + 1)
    order = []
    stack = [(start, -1, 0)]  # node, parent, depth

    while stack:
        u, p, d = stack.pop()
        if seen[u]:
            continue
        seen[u] = True
        parent[u] = p
        depth[u] = d
        order.append(u)

        for v in reversed(graph[u]):
            if not seen[v]:
                stack.append((v, u, d + 1))

    return order, parent, depth


def connected_components(n, graph):
    # UNDIRECTED graph only; returns a list of components.
    seen = [False] * (n + 1)
    components = []

    for start in range(1, n + 1):
        if seen[start]:
            continue
        seen[start] = True
        stack = [start]
        component = []

        while stack:
            u = stack.pop()
            component.append(u)
            for v in graph[u]:
                if not seen[v]:
                    seen[v] = True
                    stack.append(v)

        components.append(component)

    return components


# Example:
# graph = [[], [2], [1, 3], [2], [5], [4]]
# order, parent, depth = dfs(5, graph, 1)
# print(order)  # [1, 2, 3]
# print(depth[3])  # 2
# print(len(connected_components(5, graph)))  # 2
#
# DFS tree depth is NOT a general graph's longest-path length.
# For connected components in a directed graph, use SCC algorithms instead.
