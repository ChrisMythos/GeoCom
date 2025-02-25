# Computational Geometry Algorithms and Visualizations

This repository contains implementations of various computational geometry algorithms with interactive visualizations. The project is designed to help understand and visualize fundamental algorithms in computational geometry.

## Table of Contents

1. [Overview](#overview)
2. [Algorithms Implemented](#algorithms-implemented)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Testing](#testing)
6. [Project Structure](#project-structure)
7. [Documentation](#documentation)

## Overview

This project provides interactive visualizations for several computational geometry algorithms, including:

- Convex Hull algorithms (Graham Scan, Jarvis' March)
- Line Segment Intersection algorithms (Sweep-Line for iso-oriented segments)
- KD-Tree construction and range queries
- Delaunay Triangulation

Each visualization allows users to interact with the algorithm, add points or segments, and observe the algorithm's execution step by step.

## Algorithms Implemented

### 1. Convex Hull Algorithms

- **Graham Scan**: An efficient algorithm for computing the convex hull of a set of points in the plane.
- **Jarvis' March (Gift Wrapping)**: An algorithm for computing the convex hull by finding the most counterclockwise points.

### 2. Line Segment Intersection Algorithms

- **Sweep-Line Algorithm for Iso-Oriented Segments**: An efficient algorithm for finding all intersections among axis-aligned line segments.
- **Sweep-Line Algorithm with AVL Tree**: An implementation using a balanced binary search tree for efficient range queries.

### 3. KD-Tree Construction and Range Queries

- **2D-Tree Construction**: Interactive construction of a balanced 2D-Tree for efficient spatial queries.
- **Range Search**: Implementation of range queries using a 2D-Tree.

### 4. Delaunay Triangulation

- Implementation of the Delaunay triangulation algorithm using the circumcircle property.

## Installation

### Prerequisites

- Python 3.x
- Tkinter (usually included in Python installations)
- NumPy (for some algorithms)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/GeoCom.git
   cd GeoCom
   ```

2. Install required dependencies:

   ```bash
   pip install numpy
   ```

## Usage

Each algorithm has its own visualization script that can be run directly:

### Convex Hull Visualizer

```bash
python src/convex_hull_visualizer.py
```

- Click on the canvas to add points
- Select an algorithm (Graham Scan or Jarvis' March)
- Adjust the visualization delay using the slider
- Click "Compute Convex Hull" to start the algorithm
- Click "Reset" to clear the canvas

### Sweep-Line Algorithm for Iso-Oriented Segments

```bash
python src/intersections_ISO_2D.py
```

- Click on the canvas to add points (two consecutive clicks define a segment)
- Click "Generate Lines" to generate random segments
- Click "Compute Intersections" to start the algorithm
- Adjust the visualization delay using the slider
- Click "Reset" to clear the canvas

### KD-Tree Visualizer

```bash
python src/kd_trees.py
```

- Click on the canvas to add points
- Click "Build KD-Tree" to construct the tree
- Draw a rectangle by clicking and dragging to perform a range query
- Click "Reset" to clear the canvas

## Testing

The project includes a comprehensive test suite to ensure the correctness of the implemented algorithms. The tests are located in the `tests/` directory.

### Running Tests

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

### Test Coverage

The tests cover:

- **Intersection Detection**: Basic intersection detection, handling of parallel and collinear segments, T-junctions, endpoint intersections, numerical precision issues, etc.
- **Sweep Line Algorithm**: Empty, single, and multiple segment cases, grid patterns, star patterns, segments with shared endpoints, etc.
- **AVL Tree**: Tree balancing, insertion and deletion, finding predecessors and successors, range searching.
- **Convex Hull**: Graham scan algorithm, handling of collinear points, duplicate points, various shapes.
- **Delaunay Triangulation**: Circumcircle tests, triangulation of simple point sets, handling of collinear and duplicate points.
- **KD-Tree**: Tree construction, range searching, nearest neighbor searching.

For more details, see the [tests/README.md](tests/README.md) file.

## Project Structure

```text
GeoCom/
├── README.md                       # Main README file
├── README_A3.md                    # Documentation for KD-Tree implementation
├── README_A4.md                    # Documentation for Delaunay triangulation
├── README_intersect2D.md           # Documentation for line segment intersection
├── README_Sweep_Line_with_tree.md  # Documentation for sweep-line with AVL tree
├── requirements.txt                # Project dependencies
├── ExcercisePDFs/                  # Exercise PDFs
│   ├── CompGeoA1.pdf
│   ├── CompGeoA2.pdf
│   ├── CompGeoA3.pdf
│   └── CompGeoA4.pdf
├── src/                            # Source code
│   ├── AVL_tree.py                 # AVL tree implementation
│   ├── convex_hull_visualizer.py   # Convex hull visualization
│   ├── convex_hull.py              # Convex hull algorithms
│   ├── delaunay.py                 # Delaunay triangulation
│   ├── intersec_2D_with_tree.py    # Sweep-line with AVL tree
│   ├── intersec_2D.py              # Basic sweep-line implementation
│   ├── intersections_ISO_2D.py     # Iso-oriented segment intersections
│   ├── intersections2D_arbitrary_segments.py # Arbitrary segment intersections
│   └── kd_trees.py                 # KD-tree implementation
└── tests/                          # Test suite
    ├── README.md                   # Test documentation
    ├── conftest.py                 # Test fixtures and utilities
    ├── intersection_algorithm_test.py # Non-GUI version of intersection algorithm
    ├── kd_trees_test.py            # Non-GUI version of KD-tree
    ├── test_avl_tree.py            # Tests for AVL tree
    ├── test_convex_hull.py         # Tests for convex hull
    ├── test_delaunay.py            # Tests for Delaunay triangulation
    ├── test_intersection_detection.py # Tests for intersection detection
    ├── test_intersections.py       # Tests for line segment intersection
    ├── test_kd_tree.py             # Tests for KD-tree
    └── test_sweep_line_algorithm.py # Tests for sweep-line algorithm
```

## Documentation

Each algorithm has its own README file with detailed explanations:

- [KD-Tree Documentation](README_A3.md)
- [Delaunay Triangulation Documentation](README_A4.md)
- [Line Segment Intersection Documentation](README_intersect2D.md)
- [Sweep-Line with AVL Tree Documentation](README_Sweep_Line_with_tree.md)
