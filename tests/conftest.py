"""
Pytest configuration file for the GeoCom test suite.

This file contains fixtures and utilities that are shared across multiple test files.
"""

import sys
import os
import pytest
from typing import List, Tuple

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def sample_points() -> List[Tuple[float, float]]:
    """
    Fixture providing a sample set of 2D points for testing.
    
    Returns:
        A list of (x, y) coordinate tuples
    """
    return [
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1),
        (0.5, 0.5)
    ]


@pytest.fixture
def sample_segments() -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """
    Fixture providing a sample set of line segments for testing.
    
    Returns:
        A list of segments, where each segment is a tuple of two (x, y) points
    """
    return [
        ((0, 0), (1, 1)),    # Diagonal segment
        ((0, 1), (1, 0)),    # Diagonal segment (intersects with the first one)
        ((0.5, 0), (0.5, 1)),  # Vertical segment
        ((0, 0.5), (1, 0.5))   # Horizontal segment
    ]


@pytest.fixture
def complex_points() -> List[Tuple[float, float]]:
    """
    Fixture providing a more complex set of 2D points for testing.
    
    Returns:
        A list of (x, y) coordinate tuples
    """
    return [
        (0, 0), (2, 0), (4, 0), (6, 0),  # Points on x-axis
        (0, 2), (2, 2), (4, 2), (6, 2),  # Points 2 units above x-axis
        (0, 4), (2, 4), (4, 4), (6, 4),  # Points 4 units above x-axis
        (0, 6), (2, 6), (4, 6), (6, 6),  # Points 6 units above x-axis
    ]


@pytest.fixture
def collinear_points() -> List[Tuple[float, float]]:
    """
    Fixture providing a set of collinear points for testing edge cases.
    
    Returns:
        A list of (x, y) coordinate tuples that all lie on a straight line
    """
    return [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4)
    ]


@pytest.fixture
def duplicate_points() -> List[Tuple[float, float]]:
    """
    Fixture providing a set of points with duplicates for testing edge cases.
    
    Returns:
        A list of (x, y) coordinate tuples with some duplicates
    """
    return [
        (0, 0),
        (1, 0),
        (0, 1),
        (0, 0),  # Duplicate
        (1, 0)   # Duplicate
    ]


@pytest.fixture
def random_points(seed: int = 42, count: int = 20) -> List[Tuple[float, float]]:
    """
    Fixture providing a set of random points for testing.
    
    Args:
        seed: Random seed for reproducibility
        count: Number of points to generate
        
    Returns:
        A list of (x, y) coordinate tuples
    """
    import random
    random.seed(seed)
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(count)]
