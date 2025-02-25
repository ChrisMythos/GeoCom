"""
Tests for the KD-Tree implementation.

This module contains tests for the KD-tree data structure used for
efficient spatial queries in computational geometry.
"""

import sys
import os
import unittest
from typing import List, Optional, Tuple

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the KD-tree implementation (using the test version to avoid Tkinter)
from tests.kd_trees_test import Node, Point, construct_balanced_2d_tree, range_search


class TestKDTree(unittest.TestCase):
    """Test cases for the KD-tree implementation."""

    def test_node_creation(self):
        """Test creating a node with a point."""
        point = Point(10, 20)
        node = Node(point=point, axis=0)
        
        self.assertEqual(node.point.x, 10)
        self.assertEqual(node.point.y, 20)
        self.assertEqual(node.axis, 0)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

    def test_node_with_children(self):
        """Test creating a node with children."""
        root = Node(point=Point(10, 20), axis=0)
        left_child = Node(point=Point(5, 15), axis=1)
        right_child = Node(point=Point(15, 25), axis=1)
        
        root.left = left_child
        root.right = right_child
        
        self.assertEqual(root.left.point.x, 5)
        self.assertEqual(root.left.point.y, 15)
        self.assertEqual(root.right.point.x, 15)
        self.assertEqual(root.right.point.y, 25)

    def test_construct_balanced_2d_tree(self):
        """Test the construct_balanced_2d_tree function."""
        # Create a list of points
        points = [
            Point(10, 20),
            Point(5, 15),
            Point(15, 25),
            Point(8, 12),
            Point(12, 22)
        ]
        
        # Sort the points by x and y coordinates
        points_sorted_x = sorted(points, key=lambda p: (p.x, p.y))
        points_sorted_y = sorted(points, key=lambda p: (p.y, p.x))
        
        # Build a balanced tree
        root = construct_balanced_2d_tree(points_sorted_x, points_sorted_y, depth=0)
        
        # Check that the tree is balanced
        self.assertIsNotNone(root)
        self.assertEqual(root.axis, 0)  # Root should split on x-axis
        
        # The root should be the median point by x-coordinate
        median_x = points_sorted_x[len(points_sorted_x) // 2]
        self.assertEqual(root.point.x, median_x.x)
        self.assertEqual(root.point.y, median_x.y)

    def test_range_search(self):
        """Test the range_search function."""
        # Create a simple tree
        root = Node(point=Point(10, 20), axis=0)
        root.left = Node(point=Point(5, 15), axis=1)
        root.right = Node(point=Point(15, 25), axis=1)
        root.left.left = Node(point=Point(3, 10), axis=0)
        root.left.right = Node(point=Point(8, 12), axis=0)
        root.right.left = Node(point=Point(12, 22), axis=0)
        root.right.right = Node(point=Point(18, 28), axis=0)
        
        # Define a search range
        x_min, y_min, x_max, y_max = 4, 11, 13, 23
        
        # Perform the range search
        found_points = range_search(root, x_min, y_min, x_max, y_max)
        
        # Check that the correct points were found
        self.assertEqual(len(found_points), 4)
        self.assertTrue(any(p.x == 5 and p.y == 15 for p in found_points))
        self.assertTrue(any(p.x == 8 and p.y == 12 for p in found_points))
        self.assertTrue(any(p.x == 10 and p.y == 20 for p in found_points))
        self.assertTrue(any(p.x == 12 and p.y == 22 for p in found_points))


if __name__ == '__main__':
    unittest.main()
