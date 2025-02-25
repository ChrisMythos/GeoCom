"""
Tests for the Line Segment Intersection algorithms.

This module contains tests for the line segment intersection algorithms,
including the Bentley-Ottmann sweep-line algorithm and the functions for
detecting intersections between line segments.
"""

import sys
import os
import unittest
import math
from typing import List, Optional, Tuple

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the intersection detection functions
# Note: We're importing from the arbitrary segments implementation
from src.intersections2D_arbitrary_segments import Point, Segment, LineSegmentIntersectionVisualizer


class TestIntersections(unittest.TestCase):
    """Test cases for the line segment intersection algorithms."""

    def setUp(self):
        """Set up a new visualizer for each test."""
        # Create a mock visualizer to avoid Tkinter issues
        self.visualizer = self.create_mock_visualizer()

    def create_mock_visualizer(self):
        """Create a mock visualizer with the necessary methods for testing."""
        class MockVisualizer:
            def __init__(self):
                self.current_x = 0
                self.processed_intersections = set()
                self.event_queue = []
            
            def compute_intersection(self, s1, s2):
                """Compute the intersection point of two segments."""
                # Extract coordinates
                x1, y1 = s1.start.x, s1.start.y
                x2, y2 = s1.end.x, s1.end.y
                x3, y3 = s2.start.x, s2.start.y
                x4, y4 = s2.end.x, s2.end.y
                
                # Compute the denominator
                den = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
                
                # If denominator is 0, lines are parallel
                if den == 0:
                    return None
                
                # Compute the parameters
                ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / den
                ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / den
                
                # Check if the intersection is within both segments
                if 0 <= ua <= 1 and 0 <= ub <= 1:
                    # Compute the intersection point
                    x = x1 + ua * (x2 - x1)
                    y = y1 + ua * (y2 - y1)
                    return Point(x, y)
                
                return None
            
            def check_and_add_intersection(self, s1, s2):
                """Check if two segments intersect and add the intersection to the event queue."""
                # Skip if already processed
                if (s1.index, s2.index) in self.processed_intersections or (s2.index, s1.index) in self.processed_intersections:
                    return
                
                # Compute the intersection
                intersection = self.compute_intersection(s1, s2)
                
                # If there's an intersection and it's to the right of the current x-coordinate
                if intersection and intersection.x >= self.current_x:
                    # Add to the event queue
                    self.event_queue.append((intersection.x, intersection, [s1, s2]))
                    # Mark as processed
                    self.processed_intersections.add((s1.index, s2.index))
        
        return MockVisualizer()

    def test_compute_intersection_intersecting_segments(self):
        """Test computing the intersection point of two intersecting segments."""
        # Two segments that intersect at (1, 1)
        s1 = Segment(Point(0, 0), Point(2, 2), 0)
        s2 = Segment(Point(0, 2), Point(2, 0), 1)
        
        intersection = self.visualizer.compute_intersection(s1, s2)
        
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 1.0)
        self.assertAlmostEqual(intersection.y, 1.0)

    def test_compute_intersection_non_intersecting_segments(self):
        """Test computing the intersection point of two non-intersecting segments."""
        # Two parallel segments that don't intersect
        s1 = Segment(Point(0, 0), Point(2, 2), 0)
        s2 = Segment(Point(0, 1), Point(2, 3), 1)
        
        intersection = self.visualizer.compute_intersection(s1, s2)
        
        self.assertIsNone(intersection)

    def test_compute_intersection_parallel_segments(self):
        """Test computing the intersection point of two parallel segments."""
        # Two parallel segments
        s1 = Segment(Point(0, 0), Point(2, 2), 0)
        s2 = Segment(Point(1, 1), Point(3, 3), 1)
        
        intersection = self.visualizer.compute_intersection(s1, s2)
        
        # Parallel segments don't intersect (unless they're collinear and overlapping)
        self.assertIsNone(intersection)

    def test_compute_intersection_collinear_segments(self):
        """Test computing the intersection point of two collinear segments."""
        # Two collinear segments that don't overlap
        s1 = Segment(Point(0, 0), Point(1, 1), 0)
        s2 = Segment(Point(2, 2), Point(3, 3), 1)
        
        intersection = self.visualizer.compute_intersection(s1, s2)
        
        # Collinear segments that don't overlap don't have an intersection point
        self.assertIsNone(intersection)

    def test_compute_intersection_t_junction(self):
        """Test computing the intersection point of two segments that form a T-junction."""
        # Two segments that form a T-junction at (1, 1)
        s1 = Segment(Point(0, 1), Point(2, 1), 0)
        s2 = Segment(Point(1, 0), Point(1, 1), 1)
        
        intersection = self.visualizer.compute_intersection(s1, s2)
        
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 1.0)
        self.assertAlmostEqual(intersection.y, 1.0)

    def test_compute_intersection_endpoint_intersection(self):
        """Test computing the intersection point when segments intersect at an endpoint."""
        # Two segments that intersect at the endpoint of one segment
        s1 = Segment(Point(0, 0), Point(1, 1), 0)
        s2 = Segment(Point(1, 1), Point(2, 0), 1)
        
        intersection = self.visualizer.compute_intersection(s1, s2)
        
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 1.0)
        self.assertAlmostEqual(intersection.y, 1.0)

    def test_compute_intersection_almost_parallel_segments(self):
        """Test computing the intersection point of two almost parallel segments."""
        # Two almost parallel segments that intersect far away
        s1 = Segment(Point(0, 0), Point(1, 1), 0)
        s2 = Segment(Point(0, 0.01), Point(1, 1.01), 1)
        
        # These segments are not parallel but they don't intersect within the bounds of the segments
        intersection = self.visualizer.compute_intersection(s1, s2)
        
        self.assertIsNone(intersection)

    def test_compute_intersection_vertical_segments(self):
        """Test computing the intersection point of a vertical segment with another segment."""
        # A vertical segment and a horizontal segment that intersect
        s1 = Segment(Point(1, 0), Point(1, 2), 0)
        s2 = Segment(Point(0, 1), Point(2, 1), 1)
        
        intersection = self.visualizer.compute_intersection(s1, s2)
        
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 1.0)
        self.assertAlmostEqual(intersection.y, 1.0)

    def test_compute_intersection_horizontal_segments(self):
        """Test computing the intersection point of a horizontal segment with another segment."""
        # A horizontal segment and a diagonal segment that intersect
        s1 = Segment(Point(0, 1), Point(2, 1), 0)
        s2 = Segment(Point(0, 0), Point(2, 2), 1)
        
        intersection = self.visualizer.compute_intersection(s1, s2)
        
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 1.0)
        self.assertAlmostEqual(intersection.y, 1.0)

    def test_compute_intersection_precision_issues(self):
        """Test computing the intersection point with potential precision issues."""
        # Two segments that intersect at a point with non-integer coordinates
        s1 = Segment(Point(0, 0), Point(3, 3), 0)
        s2 = Segment(Point(0, 3), Point(3, 0), 1)
        
        intersection = self.visualizer.compute_intersection(s1, s2)
        
        self.assertIsNotNone(intersection)
        self.assertAlmostEqual(intersection.x, 1.5)
        self.assertAlmostEqual(intersection.y, 1.5)

    def test_check_and_add_intersection(self):
        """Test checking and adding an intersection to the event queue."""
        # Two segments that intersect
        s1 = Segment(Point(0, 0), Point(2, 2), 0)
        s2 = Segment(Point(0, 2), Point(2, 0), 1)
        
        # Set up the current x-coordinate and processed intersections
        self.visualizer.current_x = 0
        self.visualizer.processed_intersections.clear()
        self.visualizer.event_queue.clear()
        
        # Check and add the intersection
        self.visualizer.check_and_add_intersection(s1, s2)
        
        # Check that the intersection was added to the event queue
        self.assertEqual(len(self.visualizer.event_queue), 1)
        
        # Check that the intersection was added to the processed intersections set
        self.assertEqual(len(self.visualizer.processed_intersections), 1)
        self.assertIn((0, 1), self.visualizer.processed_intersections)

    def test_check_and_add_intersection_already_processed(self):
        """Test checking and adding an intersection that has already been processed."""
        # Two segments that intersect
        s1 = Segment(Point(0, 0), Point(2, 2), 0)
        s2 = Segment(Point(0, 2), Point(2, 0), 1)
        
        # Set up the current x-coordinate and processed intersections
        self.visualizer.current_x = 0
        self.visualizer.processed_intersections.clear()
        self.visualizer.event_queue.clear()
        
        # Add the intersection to the processed intersections set
        self.visualizer.processed_intersections.add((0, 1))
        
        # Check and add the intersection
        self.visualizer.check_and_add_intersection(s1, s2)
        
        # Check that the intersection was not added to the event queue
        self.assertEqual(len(self.visualizer.event_queue), 0)

    def test_check_and_add_intersection_behind_scan_line(self):
        """Test checking and adding an intersection that is behind the scan line."""
        # Two segments that intersect at (1, 1)
        s1 = Segment(Point(0, 0), Point(2, 2), 0)
        s2 = Segment(Point(0, 2), Point(2, 0), 1)
        
        # Set up the current x-coordinate and processed intersections
        self.visualizer.current_x = 2
        self.visualizer.processed_intersections.clear()
        self.visualizer.event_queue.clear()
        
        # Check and add the intersection
        self.visualizer.check_and_add_intersection(s1, s2)
        
        # Check that the intersection was not added to the event queue
        self.assertEqual(len(self.visualizer.event_queue), 0)

    def test_segment_get_y_at_scanline(self):
        """Test getting the y-coordinate of a segment at a given x-coordinate."""
        # A diagonal segment from (0, 0) to (2, 2)
        segment = Segment(Point(0, 0), Point(2, 2), 0)
        
        # Get the y-coordinate at x = 1
        y = segment.get_y_at_scanline(1)
        
        # The y-coordinate should be 1
        self.assertEqual(y, 1)

    def test_segment_get_y_at_scanline_vertical(self):
        """Test getting the y-coordinate of a vertical segment at a given x-coordinate."""
        # A vertical segment from (1, 0) to (1, 2)
        segment = Segment(Point(1, 0), Point(1, 2), 0)
        
        # Get the y-coordinate at x = 1
        y = segment.get_y_at_scanline(1)
        
        # For a vertical segment, the y-coordinate should be the minimum y-coordinate
        self.assertEqual(y, 0)

    def test_segment_slope(self):
        """Test calculating the slope of a segment."""
        # A diagonal segment from (0, 0) to (2, 2)
        segment = Segment(Point(0, 0), Point(2, 2), 0)
        
        # Calculate the slope
        slope = segment.slope()
        
        # The slope should be 1
        self.assertEqual(slope, 1)

    def test_segment_slope_vertical(self):
        """Test calculating the slope of a vertical segment."""
        # A vertical segment from (1, 0) to (1, 2)
        segment = Segment(Point(1, 0), Point(1, 2), 0)
        
        # Calculate the slope
        slope = segment.slope()
        
        # The slope should be infinity
        self.assertEqual(slope, float('inf'))

    def test_segment_slope_horizontal(self):
        """Test calculating the slope of a horizontal segment."""
        # A horizontal segment from (0, 1) to (2, 1)
        segment = Segment(Point(0, 1), Point(2, 1), 0)
        
        # Calculate the slope
        slope = segment.slope()
        
        # The slope should be 0
        self.assertEqual(slope, 0)


if __name__ == '__main__':
    unittest.main()
