"""
Tests for the Convex Hull algorithms.

This module contains tests for the convex hull algorithms, including
Graham Scan and the orientation test function.
"""

import sys
import os
import unittest
from typing import List, Tuple

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the convex hull implementation
from src.convex_hull import determine_point_orientation, graham_scan

# Type alias for a 2D point (x, y)
Point = Tuple[float, float]


class TestConvexHull(unittest.TestCase):
    """Test cases for the convex hull algorithms."""

    def test_determine_point_orientation_counterclockwise(self):
        """Test that the orientation function correctly identifies counter-clockwise turns."""
        # Counter-clockwise turn
        p1 = (0, 0)
        p2 = (1, 0)
        p3 = (0, 1)
        self.assertGreater(determine_point_orientation(p1, p2, p3), 0)

    def test_determine_point_orientation_clockwise(self):
        """Test that the orientation function correctly identifies clockwise turns."""
        # Clockwise turn
        p1 = (0, 0)
        p2 = (0, 1)
        p3 = (1, 0)
        self.assertLess(determine_point_orientation(p1, p2, p3), 0)

    def test_determine_point_orientation_collinear(self):
        """Test that the orientation function correctly identifies collinear points."""
        # Collinear points
        p1 = (0, 0)
        p2 = (1, 1)
        p3 = (2, 2)
        self.assertEqual(determine_point_orientation(p1, p2, p3), 0)

    def test_graham_scan_square(self):
        """Test Graham Scan on a simple square."""
        points = [(0, 0), (1, 0), (1, 1), (0, 1)]
        hull = graham_scan(points)
        
        # The hull should contain all 4 points of the square
        self.assertEqual(len(hull), 4)
        
        # Check that all original points are in the hull
        for point in points:
            self.assertIn(point, hull)

    def test_graham_scan_triangle(self):
        """Test Graham Scan on a triangle."""
        points = [(0, 0), (1, 0), (0, 1)]
        hull = graham_scan(points)
        
        # The hull should contain all 3 points of the triangle
        self.assertEqual(len(hull), 3)
        
        # Check that all original points are in the hull
        for point in points:
            self.assertIn(point, hull)

    def test_graham_scan_with_interior_points(self):
        """Test Graham Scan on a set of points with some interior points."""
        # Square with an interior point
        points = [(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0.5)]
        hull = graham_scan(points)
        
        # The hull should contain only the 4 corner points
        self.assertEqual(len(hull), 4)
        
        # The interior point should not be in the hull
        self.assertNotIn((0.5, 0.5), hull)

    def test_graham_scan_collinear_points(self):
        """Test Graham Scan on a set of points with collinear points."""
        # Points on a line
        points = [(0, 0), (1, 1), (2, 2), (3, 3)]
        hull = graham_scan(points)
        
        # The hull should contain only the endpoints
        self.assertEqual(len(hull), 2)
        self.assertIn((0, 0), hull)
        self.assertIn((3, 3), hull)

    def test_graham_scan_duplicate_points(self):
        """Test Graham Scan on a set of points with duplicate points."""
        # Square with duplicate points
        points = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0), (1, 0)]
        hull = graham_scan(points)
        
        # The hull should contain only the 4 unique corner points
        self.assertEqual(len(hull), 4)

    def test_graham_scan_single_point(self):
        """Test Graham Scan on a single point."""
        points = [(0, 0)]
        
        # This should not raise an exception, but the result may not be meaningful
        # Depending on the implementation, it might return the single point or an empty list
        hull = graham_scan(points)
        
        # Check that the result is a list
        self.assertIsInstance(hull, list)

    def test_graham_scan_two_points(self):
        """Test Graham Scan on two points."""
        points = [(0, 0), (1, 1)]
        
        # This should not raise an exception, but the result may not be meaningful
        # Depending on the implementation, it might return both points or an empty list
        hull = graham_scan(points)
        
        # Check that the result is a list
        self.assertIsInstance(hull, list)

    def test_graham_scan_complex_shape(self):
        """Test Graham Scan on a more complex shape."""
        # A more complex shape with multiple interior points
        points = [
            (0, 0), (2, 0), (4, 0), (4, 2), (4, 4), (2, 4), (0, 4), (0, 2),  # Outer square
            (1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (1, 2)   # Inner points
        ]
        hull = graham_scan(points)
        
        # The hull should contain only the 8 outer points
        self.assertEqual(len(hull), 4)  # Only 4 because the corners are the only extreme points
        
        # Check that all inner points are not in the hull
        inner_points = [(1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (1, 2)]
        for point in inner_points:
            self.assertNotIn(point, hull)

    def test_graham_scan_random_points(self):
        """Test Graham Scan on a set of random points."""
        import random
        
        # Generate 100 random points
        random.seed(42)  # For reproducibility
        points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(100)]
        
        # Compute the convex hull
        hull = graham_scan(points)
        
        # Check that the hull is a subset of the original points
        for point in hull:
            self.assertIn(point, points)
        
        # Check that the hull is convex by verifying that all turns are counter-clockwise
        for i in range(len(hull)):
            p1 = hull[i]
            p2 = hull[(i + 1) % len(hull)]
            p3 = hull[(i + 2) % len(hull)]
            self.assertGreaterEqual(determine_point_orientation(p1, p2, p3), 0)


if __name__ == '__main__':
    unittest.main()
