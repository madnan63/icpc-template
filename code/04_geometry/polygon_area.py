def polygon_area(points):
    n = len(points)
    area2 = 0

    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]

        area2 += x1 * y2 - y1 * x2

    return abs(area2) / 2
