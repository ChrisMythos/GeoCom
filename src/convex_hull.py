"""
Convex Hull Algorithms

This module implements algorithms for computing the convex hull of a set of points
in the 2D plane. The convex hull is the smallest convex polygon that contains all
the points in a given set.

Currently implemented algorithms:
- Graham Scan: An efficient O(n log n) algorithm for computing the convex hull
"""

from typing import List, Tuple, TypeVar

# Type alias for a 2D point (x, y)
Point = Tuple[float, float]


def determine_point_orientation(p1: Point, p2: Point, p3: Point) -> float:
    """
    Determine the orientation of three points in the 2D plane.
    
    This function calculates the cross product of vectors p1->p2 and p1->p3
    to determine the orientation of the three points.
    
    Args:
        p1: The first point as a tuple (x, y)
        p2: The second point as a tuple (x, y)
        p3: The third point as a tuple (x, y)
        
    Returns:
        float: A positive value if the points make a counter-clockwise turn,
               a negative value if they make a clockwise turn,
               and zero if the points are collinear.
    """
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])


def graham_scan(points_input: List[Point]) -> List[Point]:
    """
    Compute the convex hull of a set of points using the Graham Scan algorithm.
    
    The Graham Scan algorithm works by first sorting the points by x-coordinate
    (and by y-coordinate in case of a tie), then constructing the upper and lower
    hulls separately by processing the points in order.
    
    Time complexity: O(n log n) where n is the number of input points.
    Space complexity: O(n)
    
    Args:
        points_input: A list of points, where each point is a tuple (x, y)
        
    Returns:
        A list of points forming the convex hull in counter-clockwise order
    """
    # Sort the points by x-coordinate, and by y-coordinate in case of a tie
    points_sorted = sorted(points_input, key=lambda p: (p[0], p[1]))
    
    # Construct the lower hull
    lower = []
    for p in points_sorted:
        # While the last two points and the current point do not make a counter-clockwise turn,
        # remove the last point from the lower hull
        while (
            len(lower) >= 2
            and determine_point_orientation(lower[-2], lower[-1], p) <= 0
        ):
            lower.pop()
        lower.append(p)
    
    # Construct the upper hull
    upper = []
    for p in reversed(points_sorted):
        # While the last two points and the current point do not make a counter-clockwise turn,
        # remove the last point from the upper hull
        while (
            len(upper) >= 2
            and determine_point_orientation(upper[-2], upper[-1], p) <= 0
        ):
            upper.pop()
        upper.append(p)
    
    # Combine the lower and upper hulls to form the complete convex hull
    # Remove the last point from each hull as they are duplicated
    full_hull = lower[:-1] + upper[:-1]
    return full_hull


# Example usage
if __name__ == "__main__":
    # Example points
    points = [(0, 0), (1, 0), (2, 1), (1, 2), (0, 2), (0, 1)]
    
    # Compute the convex hull
    hull = graham_scan(points)
    
    print("Input points:", points)
    print("Convex hull:", hull)
