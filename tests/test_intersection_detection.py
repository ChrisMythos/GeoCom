"""
Tests for the line segment intersection detection algorithm.

This module contains tests for the basic intersection detection functionality,
focusing on the compute_intersection method and various edge cases.
"""

import unittest
import math
from typing import List, Tuple

from tests.intersection_algorithm_test import Point, Segment, IntersectionDetector


class TestIntersectionDetection(unittest.TestCase):
    """Test cases for the line segment intersection detection algorithm."""

    def setUp(self):
        """Set up a new intersection detector for each test."""
        self.detector = IntersectionDetector()

    def test_basic_intersection(self):
        """Test a basic intersection between two segments."""
        # Two segments that intersect at (1, 1)
        s1 = Segment(Point(0, 0), Point(2, 2), 0)
        s2 = Segment(Point(0, 2), Point(2, 0), 1)
        
        intersection = self.detector.compute_intersection(s1, s2)
        
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 1.0)
        self.assertAlmostEqual(intersection.y, 1.0)

    def test_no_intersection(self):
        """Test segments that don't intersect."""
        # Two parallel segments that don't intersect
        s1 = Segment(Point(0, 0), Point(2, 2), 0)
        s2 = Segment(Point(0, 1), Point(2, 3), 1)
        
        intersection = self.detector.compute_intersection(s1, s2)
        
        self.assertIsNone(intersection)

    def test_parallel_segments(self):
        """Test parallel segments."""
        # Two parallel segments
        s1 = Segment(Point(0, 0), Point(2, 2), 0)
        s2 = Segment(Point(1, 1), Point(3, 3), 1)
        
        intersection = self.detector.compute_intersection(s1, s2)
        
        # Parallel segments don't intersect (unless they're collinear and overlapping)
        self.assertIsNone(intersection)

    def test_collinear_non_overlapping_segments(self):
        """Test collinear segments that don't overlap."""
        # Two collinear segments that don't overlap
        s1 = Segment(Point(0, 0), Point(1, 1), 0)
        s2 = Segment(Point(2, 2), Point(3, 3), 1)
        
        intersection = self.detector.compute_intersection(s1, s2)
        
        # Collinear segments that don't overlap don't have an intersection point
        self.assertIsNone(intersection)

    def test_t_junction_intersection(self):
        """Test segments that form a T-junction."""
        # Two segments that form a T-junction at (1, 1)
        s1 = Segment(Point(0, 1), Point(2, 1), 0)
        s2 = Segment(Point(1, 0), Point(1, 1), 1)
        
        intersection = self.detector.compute_intersection(s1, s2)
        
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 1.0)
        self.assertAlmostEqual(intersection.y, 1.0)

    def test_endpoint_intersection(self):
        """Test segments that intersect at an endpoint."""
        # Two segments that intersect at the endpoint of one segment
        s1 = Segment(Point(0, 0), Point(1, 1), 0)
        s2 = Segment(Point(1, 1), Point(2, 0), 1)
        
        intersection = self.detector.compute_intersection(s1, s2)
        
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 1.0)
        self.assertAlmostEqual(intersection.y, 1.0)

    def test_shared_endpoint(self):
        """Test segments that share an endpoint."""
        # Two segments that share an endpoint at (1, 1)
        s1 = Segment(Point(0, 0), Point(1, 1), 0)
        s2 = Segment(Point(1, 1), Point(2, 2), 1)
        
        intersection = self.detector.compute_intersection(s1, s2)
        
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 1.0)
        self.assertAlmostEqual(intersection.y, 1.0)

    def test_almost_parallel_segments(self):
        """Test almost parallel segments."""
        # Two almost parallel segments that don't intersect within the bounds
        s1 = Segment(Point(0, 0), Point(1, 1), 0)
        s2 = Segment(Point(0, 0.01), Point(1, 1.01), 1)
        
        intersection = self.detector.compute_intersection(s1, s2)
        
        self.assertIsNone(intersection)

    def test_vertical_horizontal_intersection(self):
        """Test intersection between vertical and horizontal segments."""
        # A vertical segment and a horizontal segment that intersect
        s1 = Segment(Point(1, 0), Point(1, 2), 0)
        s2 = Segment(Point(0, 1), Point(2, 1), 1)
        
        intersection = self.detector.compute_intersection(s1, s2)
        
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 1.0)
        self.assertAlmostEqual(intersection.y, 1.0)

    def test_precision_issues(self):
        """Test intersection with potential precision issues."""
        # Two segments that intersect at a point with non-integer coordinates
        s1 = Segment(Point(0, 0), Point(3, 3), 0)
        s2 = Segment(Point(0, 3), Point(3, 0), 1)
        
        intersection = self.detector.compute_intersection(s1, s2)
        
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 1.5)
        self.assertAlmostEqual(intersection.y, 1.5)

    def test_very_small_segments(self):
        """Test intersection between very small segments."""
        # Two very small segments that intersect
        s1 = Segment(Point(0.0001, 0.0001), Point(0.0002, 0.0002), 0)
        s2 = Segment(Point(0.0001, 0.0002), Point(0.0002, 0.0001), 1)
        
        intersection = self.detector.compute_intersection(s1, s2)
        
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 0.00015)
        self.assertAlmostEqual(intersection.y, 0.00015)

    def test_very_large_segments(self):
        """Test intersection between very large segments."""
        # Two very large segments that intersect
        s1 = Segment(Point(0, 0), Point(1e6, 1e6), 0)
        s2 = Segment(Point(0, 1e6), Point(1e6, 0), 1)
        
        intersection = self.detector.compute_intersection(s1, s2)
        
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 5e5)
        self.assertAlmostEqual(intersection.y, 5e5)

    def test_near_miss_intersection(self):
        """Test segments that almost intersect but don't."""
        # Two segments that almost intersect
        s1 = Segment(Point(0, 0), Point(1, 1), 0)
        s2 = Segment(Point(0, 0.01), Point(0.99, 1), 1)
        
        intersection = self.detector.compute_intersection(s1, s2)
        
        self.assertIsNone(intersection)

    def test_multiple_intersections_naive(self):
        """Test finding multiple intersections using the naive approach."""
        # Create a simple configuration with known intersections
        self.detector.add_segment(Point(0, 0), Point(2, 2))  # Segment 0
        self.detector.add_segment(Point(0, 2), Point(2, 0))  # Segment 1
        self.detector.add_segment(Point(1, 0), Point(1, 2))  # Segment 2
        
        # Find intersections using the naive approach
        intersections = self.detector.find_all_intersections_naive()
        
        # There should be 3 intersections:
        # - Segment 0 and Segment 1 at (1, 1)
        # - Segment 0 and Segment 2 at (1, 1)
        # - Segment 1 and Segment 2 at (1, 1)
        self.assertEqual(len(intersections), 3)
        
        # All intersections should be at (1, 1)
        for point in intersections:
            self.assertAlmostEqual(point.x, 1.0)
            self.assertAlmostEqual(point.y, 1.0)

    def test_grid_pattern_naive(self):
        """Test finding intersections in a grid pattern using the naive approach."""
        # Create a 3x3 grid of horizontal and vertical segments
        # Horizontal segments
        for i in range(3):
            self.detector.add_segment(Point(0, i), Point(2, i))
        
        # Vertical segments
        for i in range(3):
            self.detector.add_segment(Point(i, 0), Point(i, 2))
        
        # Find intersections using the naive approach
        intersections = self.detector.find_all_intersections_naive()
        
        # There should be 9 intersections (3x3 grid)
        self.assertEqual(len(intersections), 9)
        
        # Check that all expected intersection points are found
        expected_points = []
        for i in range(3):
            for j in range(3):
                expected_points.append((i, j))
        
        for point in intersections:
            self.assertTrue((round(point.x), round(point.y)) in expected_points)


if __name__ == '__main__':
    unittest.main()
