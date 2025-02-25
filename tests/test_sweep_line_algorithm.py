"""
Tests for the Bentley-Ottmann sweep-line algorithm.

This module contains tests for the sweep-line algorithm for finding
all intersections among arbitrary line segments.
"""

import unittest
import random
import math
from typing import List, Set, Tuple

from tests.intersection_algorithm_test import Point, Segment, IntersectionDetector


class TestSweepLineAlgorithm(unittest.TestCase):
    """Test cases for the sweep-line algorithm."""

    def setUp(self):
        """Set up a new intersection detector for each test."""
        self.detector = IntersectionDetector()

    def test_no_segments(self):
        """Test with no segments."""
        # No segments added
        intersections = self.detector.find_intersections()
        
        # There should be no intersections
        self.assertEqual(len(intersections), 0)

    def test_single_segment(self):
        """Test with a single segment."""
        # Add a single segment
        self.detector.add_segment(Point(0, 0), Point(1, 1))
        
        # Find intersections
        intersections = self.detector.find_intersections()
        
        # There should be no intersections
        self.assertEqual(len(intersections), 0)

    def test_two_non_intersecting_segments(self):
        """Test with two non-intersecting segments."""
        # Add two non-intersecting segments
        self.detector.add_segment(Point(0, 0), Point(1, 1))
        self.detector.add_segment(Point(2, 2), Point(3, 3))
        
        # Find intersections
        intersections = self.detector.find_intersections()
        
        # There should be no intersections
        self.assertEqual(len(intersections), 0)

    def test_two_intersecting_segments(self):
        """Test with two intersecting segments."""
        # Add two intersecting segments
        self.detector.add_segment(Point(0, 0), Point(2, 2))
        self.detector.add_segment(Point(0, 2), Point(2, 0))
        
        # Find intersections
        intersections = self.detector.find_intersections()
        
        # There should be one intersection at (1, 1)
        self.assertEqual(len(intersections), 1)
        self.assertAlmostEqual(intersections[0].x, 1.0)
        self.assertAlmostEqual(intersections[0].y, 1.0)

    def test_three_segments_with_common_intersection(self):
        """Test with three segments that all intersect at the same point."""
        # Add three segments that all intersect at (1, 1)
        self.detector.add_segment(Point(0, 0), Point(2, 2))  # Diagonal
        self.detector.add_segment(Point(0, 2), Point(2, 0))  # Diagonal
        self.detector.add_segment(Point(1, 0), Point(1, 2))  # Vertical
        
        # Find intersections
        intersections = self.detector.find_intersections()
        
        # There should be 3 intersections (each pair of segments)
        # All at the same point (1, 1)
        self.assertEqual(len(intersections), 3)
        
        # All intersections should be at (1, 1)
        for point in intersections:
            self.assertAlmostEqual(point.x, 1.0)
            self.assertAlmostEqual(point.y, 1.0)

    def test_grid_pattern(self):
        """Test with a grid pattern of segments."""
        # Create a 3x3 grid of horizontal and vertical segments
        # Horizontal segments
        for i in range(3):
            self.detector.add_segment(Point(0, i), Point(2, i))
        
        # Vertical segments
        for i in range(3):
            self.detector.add_segment(Point(i, 0), Point(i, 2))
        
        # Find intersections
        intersections = self.detector.find_intersections()
        
        # There should be 9 intersections (3x3 grid)
        self.assertEqual(len(intersections), 9)
        
        # Check that all expected intersection points are found
        expected_points = []
        for i in range(3):
            for j in range(3):
                expected_points.append((i, j))
        
        for point in intersections:
            self.assertTrue((round(point.x), round(point.y)) in expected_points)

    def test_star_pattern(self):
        """Test with a star pattern of segments."""
        # Create a star pattern with 8 segments all intersecting at the center
        center = Point(1, 1)
        num_segments = 8
        
        for i in range(num_segments):
            angle = 2 * 3.14159 * i / num_segments
            end_x = 1 + 2 * math.cos(angle)
            end_y = 1 + 2 * math.sin(angle)
            self.detector.add_segment(center, Point(end_x, end_y))
        
        # Find intersections
        intersections = self.detector.find_intersections()
        
        # There should be (8 choose 2) = 28 intersections
        # But they're all at the same point (1, 1)
        self.assertEqual(len(intersections), 28)
        
        # All intersections should be at (1, 1)
        for point in intersections:
            self.assertAlmostEqual(point.x, 1.0)
            self.assertAlmostEqual(point.y, 1.0)

    def test_all_parallel_segments(self):
        """Test with all parallel segments."""
        # Add several parallel segments
        for i in range(5):
            self.detector.add_segment(Point(0, i), Point(2, i))
        
        # Find intersections
        intersections = self.detector.find_intersections()
        
        # There should be no intersections
        self.assertEqual(len(intersections), 0)

    def test_all_vertical_segments(self):
        """Test with all vertical segments."""
        # Add several vertical segments
        for i in range(5):
            self.detector.add_segment(Point(i, 0), Point(i, 2))
        
        # Find intersections
        intersections = self.detector.find_intersections()
        
        # There should be no intersections
        self.assertEqual(len(intersections), 0)

    def test_random_segments(self):
        """Test with random segments and compare with naive approach."""
        # Set a random seed for reproducibility
        random.seed(42)
        
        # Generate 20 random segments
        for _ in range(20):
            x1 = random.uniform(0, 10)
            y1 = random.uniform(0, 10)
            x2 = random.uniform(0, 10)
            y2 = random.uniform(0, 10)
            self.detector.add_segment(Point(x1, y1), Point(x2, y2))
        
        # Find intersections using the sweep-line algorithm
        sweep_intersections = self.detector.find_intersections()
        
        # Find intersections using the naive approach
        naive_intersections = self.detector.find_all_intersections_naive()
        
        # The number of intersections should be the same
        self.assertEqual(len(sweep_intersections), len(naive_intersections))
        
        # Convert to sets of (x, y) tuples for comparison
        sweep_points = {(round(p.x, 9), round(p.y, 9)) for p in sweep_intersections}
        naive_points = {(round(p.x, 9), round(p.y, 9)) for p in naive_intersections}
        
        # The sets of intersection points should be the same
        self.assertEqual(sweep_points, naive_points)

    def test_segments_with_shared_endpoints(self):
        """Test with segments that share endpoints."""
        # Create a sequence of segments that share endpoints
        self.detector.add_segment(Point(0, 0), Point(1, 1))
        self.detector.add_segment(Point(1, 1), Point(2, 0))
        self.detector.add_segment(Point(2, 0), Point(3, 1))
        self.detector.add_segment(Point(3, 1), Point(4, 0))
        
        # Find intersections
        intersections = self.detector.find_intersections()
        
        # There should be 3 intersections (at the shared endpoints)
        self.assertEqual(len(intersections), 3)
        
        # Check that all expected intersection points are found
        expected_points = [(1, 1), (2, 0), (3, 1)]
        
        for point in intersections:
            self.assertTrue((round(point.x), round(point.y)) in expected_points)

    def test_segments_with_multiple_intersections(self):
        """Test with segments that have multiple intersections."""
        # Create a configuration where a segment intersects multiple other segments
        self.detector.add_segment(Point(0, 1), Point(4, 1))  # Horizontal segment
        self.detector.add_segment(Point(1, 0), Point(1, 2))  # Vertical segment 1
        self.detector.add_segment(Point(2, 0), Point(2, 2))  # Vertical segment 2
        self.detector.add_segment(Point(3, 0), Point(3, 2))  # Vertical segment 3
        
        # Find intersections
        intersections = self.detector.find_intersections()
        
        # There should be 3 intersections
        self.assertEqual(len(intersections), 3)
        
        # Check that all expected intersection points are found
        expected_points = [(1, 1), (2, 1), (3, 1)]
        
        for point in intersections:
            self.assertTrue((round(point.x), round(point.y)) in expected_points)

    def test_compare_with_naive_approach(self):
        """Test that the sweep-line algorithm finds the same intersections as the naive approach."""
        # Create a complex configuration
        # Horizontal segments
        for i in range(5):
            self.detector.add_segment(Point(0, i), Point(4, i))
        
        # Vertical segments
        for i in range(5):
            self.detector.add_segment(Point(i, 0), Point(i, 4))
        
        # Diagonal segments
        self.detector.add_segment(Point(0, 0), Point(4, 4))
        self.detector.add_segment(Point(0, 4), Point(4, 0))
        
        # Find intersections using the sweep-line algorithm
        sweep_intersections = self.detector.find_intersections()
        
        # Find intersections using the naive approach
        naive_intersections = self.detector.find_all_intersections_naive()
        
        # The number of intersections should be the same
        self.assertEqual(len(sweep_intersections), len(naive_intersections))
        
        # Convert to sets of (x, y) tuples for comparison
        sweep_points = {(round(p.x, 9), round(p.y, 9)) for p in sweep_intersections}
        naive_points = {(round(p.x, 9), round(p.y, 9)) for p in naive_intersections}
        
        # The sets of intersection points should be the same
        self.assertEqual(sweep_points, naive_points)


if __name__ == '__main__':
    unittest.main()
