# GRID BFS / ITERATIVE DFS - O(rows * cols).
# 0-based coordinates (row, col); '#' is a wall, all others passable.
# Uses FOUR directions; add diagonals to DIRS for 8-direction movement.
# Grid must be non-empty, rectangular, and use strings or char lists.

from collections import deque

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def grid_bfs(grid, sr, sc):
    # Shortest unweighted distances + parents from (sr, sc).
    n, m = len(grid), len(grid[0])
    dist = [[-1] * m for _ in range(n)]
    parent = [[None] * m for _ in range(n)]
    if grid[sr][sc] == '#':
        return dist, parent

    dist[sr][sc] = 0
    q = deque([(sr, sc)])

    while q:
        r, c = q.popleft()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < n and 0 <= nc < m
                    and grid[nr][nc] != '#'
                    and dist[nr][nc] == -1):
                dist[nr][nc] = dist[r][c] + 1
                parent[nr][nc] = (r, c)
                q.append((nr, nc))

    return dist, parent


def grid_path(parent, sr, sc, tr, tc):
    # Reconstruct coordinates after grid_bfs; [] if unreachable.
    path = []
    cur = (tr, tc)
    while cur is not None:
        path.append(cur)
        if cur == (sr, sc):
            return path[::-1]
        r, c = cur
        cur = parent[r][c]
    return []


def grid_dfs(grid, sr, sc, seen):
    # Mark one connected open component; return its size.
    n, m = len(grid), len(grid[0])
    if grid[sr][sc] == '#' or seen[sr][sc]:
        return 0

    seen[sr][sc] = True
    stack = [(sr, sc)]
    count = 0

    while stack:
        r, c = stack.pop()
        count += 1
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < n and 0 <= nc < m
                    and grid[nr][nc] != '#'
                    and not seen[nr][nc]):
                seen[nr][nc] = True
                stack.append((nr, nc))
    return count


def count_rooms(grid):
    # Count 4-connected open regions; 'seen' shared across DFS runs.
    n, m = len(grid), len(grid[0])
    seen = [[False] * m for _ in range(n)]
    rooms = 0
    for r in range(n):
        for c in range(m):
            if grid_dfs(grid, r, c, seen):
                rooms += 1
    return rooms


# Example:
# grid = ["..#.", ".##.", "...#"]
# dist, parent = grid_bfs(grid, 0, 0)
# print(dist[2][2])  # 4
# print(grid_path(parent, 0, 0, 2, 2))
# print(count_rooms(grid))  # 2
