# GeoCom Tests

This directory contains tests for the GeoCom computational geometry library. The tests are written using the pytest framework and cover various components of the library.

## Test Structure

The tests are organized by component:

- `test_avl_tree.py`: Tests for the AVL tree implementation
- `test_convex_hull.py`: Tests for the convex hull algorithms
- `test_delaunay.py`: Tests for the Delaunay triangulation
- `test_intersections.py`: Tests for the line segment intersection algorithms
- `test_kd_tree.py`: Tests for the KD-tree implementation
- `conftest.py`: Common fixtures and utilities for tests

## Running the Tests

### Prerequisites

Make sure you have pytest installed:

```bash
pip install pytest
```

Or install all dependencies from the project's requirements.txt:

```bash
pip install -r ../requirements.txt
```

### Running All Tests

From the project root directory:

```bash
pytest tests/
```

### Running Specific Test Files

```bash
pytest tests/test_avl_tree.py
pytest tests/test_convex_hull.py
# etc.
```

### Running Specific Test Functions

```bash
pytest tests/test_avl_tree.py::TestAVLTree::test_insert_single_value
```

### Running Tests with Verbose Output

```bash
pytest -v tests/
```

### Running Tests with Coverage Report

If you have pytest-cov installed:

```bash
pytest --cov=src tests/
```

## Test Coverage

The tests cover the following aspects of the library:

### AVL Tree Tests

- Tree creation and basic operations
- Insertion and deletion of nodes
- Tree balancing (left-left, right-right, left-right, right-left cases)
- Successor pointers
- Range queries

### Convex Hull Tests

- Point orientation determination
- Graham Scan algorithm
- Edge cases (collinear points, duplicate points)
- Random point sets

### Delaunay Triangulation Tests

- Circumcircle test
- Triangulation construction
- Edge cases (collinear points, duplicate points)
- Random point sets

### Line Segment Intersection Tests

- Intersection detection
- Sweep-line algorithm
- Edge cases (parallel segments, collinear segments, T-junctions)
- Segment operations (slope calculation, y-coordinate at x)

### KD-Tree Tests

- Tree creation and basic operations
- Insertion of points
- Nearest neighbor search
- Range queries
- Edge cases (empty tree, points outside range)

## Adding New Tests

When adding new tests:

1. Follow the existing pattern for test files and classes
2. Use descriptive test function names that explain what is being tested
3. Add docstrings to test functions to explain the test purpose
4. Consider adding common fixtures to `conftest.py` if they will be used across multiple test files
5. Ensure tests are deterministic (use fixed seeds for random operations)
