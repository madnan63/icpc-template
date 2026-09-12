import heapq


def dijkstra(n, graph, start=1):
    INF = float('inf')

    dist = [INF] * (n + 1)
    parent = [-1] * (n + 1)

    dist[start] = 0
    pq = [(0, start)]

    while pq:
        curr_dist, u = heapq.heappop(pq)

        if curr_dist != dist[u]:
            continue

        for v, weight in graph[u]:
            new_dist = curr_dist + weight

            if new_dist < dist[v]:
                dist[v] = new_dist
                parent[v] = u
                heapq.heappush(pq, (new_dist, v))

    return dist, parent


def restore_path(parent, target):
    path = []

    while target != -1:
        path.append(target)
        target = parent[target]

    path.reverse()
    return path
