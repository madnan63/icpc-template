def dfs_max_depth(start, graph):
    visited = {start}
    stack = [(start, 1)]
    max_depth = 0

    while stack:
        node, depth = stack.pop()
        max_depth = max(max_depth, depth)

        for nei in graph.get(node, []):
            if nei not in visited:
                visited.add(nei)
                stack.append((nei, depth + 1))

    return max_depth
