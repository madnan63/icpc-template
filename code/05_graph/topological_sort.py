from collections import deque


def topological_sort_kahn(graph, n):
    indegree = [0] * (n + 1)

    for u in range(1, n + 1):
        for v in graph[u]:
            indegree[v] += 1

    q = deque()

    for i in range(1, n + 1):
        if indegree[i] == 0:
            q.append(i)

    order = []

    while q:
        u = q.popleft()
        order.append(u)

        for v in graph[u]:
            indegree[v] -= 1

            if indegree[v] == 0:
                q.append(v)

    if len(order) != n:
        return []  # Cycle exists.

    return order
