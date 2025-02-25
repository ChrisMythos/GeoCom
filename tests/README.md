# GeoCom Tests

This directory contains comprehensive tests for the GeoCom computational geometry library.

## Test Structure

The tests are organized by component:

- **test_avl_tree.py**: Tests for the AVL tree implementation
- **test_convex_hull.py**: Tests for the convex hull algorithm
- **test_delaunay.py**: Tests for the Delaunay triangulation algorithm
- **test_intersections.py**: Tests for the original line segment intersection implementation
- **test_intersection_detection.py**: Tests for the intersection detection functionality
- **test_sweep_line_algorithm.py**: Tests for the Bentley-Ottmann sweep-line algorithm
- **test_kd_tree.py**: Tests for the KD-tree implementation

## Test Utilities

- **intersection_algorithm_test.py**: A non-GUI version of the line segment intersection algorithm for testing
- **kd_trees_test.py**: A non-GUI version of the KD-tree implementation for testing
- **conftest.py**: Common fixtures and utilities for tests

## Running Tests

You can run all tests with:

```bash
python -m pytest
```

Or run specific test files:

```bash
python -m pytest tests/test_intersection_detection.py
```

Or run specific test cases:

```bash
python -m pytest tests/test_intersection_detection.py::TestIntersectionDetection::test_basic_intersection
```

Use the `-v` flag for verbose output:

```bash
python -m pytest -v
```

## Test Coverage

The tests cover:

### Intersection Detection
- Basic intersection detection between two segments
- Handling of parallel and collinear segments
- T-junctions and endpoint intersections
- Numerical precision issues
- Very small and very large segments
- Shared endpoints

### Sweep Line Algorithm
- Empty, single, and multiple segment cases
- Grid patterns and star patterns
- Segments with shared endpoints
- Segments with multiple intersections
- Comparison with naive approach

### AVL Tree
- Tree balancing (left-left, left-right, right-left, right-right rotations)
- Insertion and deletion
- Finding predecessors and successors
- Range searching

### Convex Hull
- Graham scan algorithm
- Handling of collinear points
- Handling of duplicate points
- Various shapes (triangles, squares, complex shapes)

### Delaunay Triangulation
- Circumcircle tests
- Triangulation of simple point sets
- Handling of collinear and duplicate points

### KD-Tree
- Tree construction
- Range searching
- Nearest neighbor searching

## Notes

- The tests use a simplified version of the algorithms without GUI components to make testing easier.
- Some tests compare the results of the optimized algorithms with naive implementations to ensure correctness.
- The tests include edge cases and stress tests to ensure the algorithms are robust.
