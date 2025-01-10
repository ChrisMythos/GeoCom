from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])


def determine_point_orientation(p1: Point, p2: Point, p3: Point) -> float:
    """
    Gibt den Orientierungswert zurück:
    >0: p1->p2->p3 ist gegen den Uhrzeigersinn
    <0: p1->p2->p3 ist im Uhrzeigersinn
    =0: p1, p2, p3 sind kollinear
    """
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)


def graham_scan(points_input):
    # Graham Scan ohne Visualisierung, gibt die konvexe Hülle als Liste von (x,y)-Tupeln zurück.
    points_sorted = sorted(points_input, key=lambda p: (p.x, p.y))

    lower = []
    for p in points_sorted:
        while (
            len(lower) >= 2
            and determine_point_orientation(lower[-2], lower[-1], p) <= 0
        ):
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points_sorted):
        while (
            len(upper) >= 2
            and determine_point_orientation(upper[-2], upper[-1], p) <= 0
        ):
            upper.pop()
        upper.append(p)

    # Enden entfernen, da sie doppelt vorkommen
    full_hull = lower[:-1] + upper[:-1]
    return full_hull
