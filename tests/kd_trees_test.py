"""
A simplified version of the KD-tree implementation for testing purposes.

This module contains only the necessary classes and functions for testing,
without the Tkinter-related code that would create a window.
"""

from dataclasses import dataclass


@dataclass
class Point:
    """Represents a point with x and y coordinates."""
    x: int
    y: int


class Node:
    """Node class for the 2D-tree."""

    def __init__(self, point=None, left=None, right=None, axis=0):
        self.point = point    # Point at this node
        self.left = left      # Left subtree
        self.right = right    # Right subtree
        self.axis = axis      # Current axis: 0 for x, 1 for y


def preprocessing(points):
    """Sort the points by x and y coordinates."""
    points_sorted_x = sorted(points, key=lambda point: (point.x, point.y))
    points_sorted_y = sorted(points, key=lambda point: (point.y, point.x))
    return points_sorted_x, points_sorted_y


def construct_balanced_2d_tree(points_sorted_x, points_sorted_y, depth):
    """Recursively construct a balanced 2D-tree with additional checks."""
    if not points_sorted_x or not points_sorted_y:
        return None

    if len(points_sorted_x) == 1:
        return Node(point=points_sorted_x[0], axis=depth % 2)

    axis = depth % 2  # 0 for x, 1 for y

    if axis == 0:
        median = len(points_sorted_x) // 2
        median_point = points_sorted_x[median]
        left_points_x = points_sorted_x[:median]
        right_points_x = points_sorted_x[median+1:]

        # Sort the Y points by the X median
        # If the point equals the X median, use the Y median
        left_points_y = [p for p in points_sorted_y if p.x < median_point.x or (
            p.x == median_point.x and p.y < median_point.y)]
        right_points_y = [p for p in points_sorted_y if p.x > median_point.x or (
            p.x == median_point.x and p.y > median_point.y)]

    else:  # y-axis
        median = len(points_sorted_y) // 2
        median_point = points_sorted_y[median]
        # Store the points to the left and right of the median point
        left_points_y = points_sorted_y[:median]
        right_points_y = points_sorted_y[median+1:]

        # Sort the X points by the Y median
        # If the point equals the median, use the X median
        left_points_x = [p for p in points_sorted_x if p.y < median_point.y or (
            p.y == median_point.y and p.x < median_point.x)]
        right_points_x = [p for p in points_sorted_x if p.y > median_point.y or (
                          p.y == median_point.y and p.x > median_point.x)]

    # Termination condition: No more points left
    if not left_points_x and not right_points_x:
        return Node(point=median_point, axis=axis)

    # Create the node with the median point and the current axis
    node = Node(
        point=median_point,
        axis=axis
    )
    # Recursive call for left and right subtrees with the filtered point sets
    node.left = construct_balanced_2d_tree(
        left_points_x, left_points_y, depth + 1)
    node.right = construct_balanced_2d_tree(
        right_points_x, right_points_y, depth + 1)

    return node


def range_search(node, x_min, y_min, x_max, y_max, found_points=None):
    """Recursive range search algorithm in a k-d tree for 2D points."""
    if found_points is None:
        found_points = []

    if node is None:
        # If the current node is empty, end the search in this path
        return

    x = node.point.x  # x-coordinate of the point in the current node
    y = node.point.y  # y-coordinate of the point in the current node

    # If the point of the current node is in the search range, add it to the output
    if x_min <= x <= x_max and y_min <= y <= y_max:
        found_points.append(node.point)

    # Axis of the division in the current node (0 for x-axis, 1 for y-axis)
    axis = node.axis

    if axis == 0:  # x-axis
        # Decision which child nodes to search based on x-value
        if x_min <= x:
            # Search left recursively
            range_search(node.left, x_min, y_min, x_max, y_max, found_points)
        if x <= x_max:
            # Search right recursively
            range_search(node.right, x_min, y_min, x_max, y_max, found_points)
    else:  # y-axis
        # Decision which child nodes to search based on y-value
        if y_min <= y:
            # Search left recursively
            range_search(node.left, x_min, y_min, x_max, y_max, found_points)
        if y <= y_max:
            # Search right recursively
            range_search(node.right, x_min, y_min, x_max, y_max, found_points)

    return found_points
