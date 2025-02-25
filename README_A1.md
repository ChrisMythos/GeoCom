# Convex Hull Visualizer

## Overview

This application provides an interactive visualization of two popular algorithms for computing the convex hull of a set of points in the 2D plane:

1. **Graham Scan**: An efficient O(n log n) algorithm that sorts points by angle and builds the hull incrementally.
2. **Jarvis' March (Gift Wrapping)**: An O(nh) algorithm where n is the number of points and h is the number of points on the hull, which finds the hull by wrapping a line around the point set.

The convex hull of a set of points is the smallest convex polygon that contains all the points. It can be visualized as the shape formed by stretching a rubber band around the points.

## Features

- **Interactive Point Placement**: Click anywhere on the canvas to add points.
- **Algorithm Selection**: Choose between Graham Scan and Jarvis' March algorithms.
- **Visualization Speed Control**: Adjust the delay between visualization steps.
- **Step-by-Step Visualization**: Watch how each algorithm constructs the convex hull.
- **Reset Functionality**: Clear all points and start over.

## Algorithm Details

### Graham Scan

The Graham Scan algorithm works as follows:

1. Find the point with the lowest y-coordinate (and leftmost if tied).
2. Sort all points by polar angle around this point.
3. Process points in order, maintaining a stack of points on the hull.
4. For each point, check if it makes a counter-clockwise turn with the last two points on the stack.
5. If not, pop the last point from the stack and repeat the check.
6. If yes, push the current point onto the stack.

In this implementation, we use a variant that:

1. Sorts points by x-coordinate (and y-coordinate for ties).
2. Constructs the lower and upper hulls separately.
3. Combines them to form the complete convex hull.

### Jarvis' March (Gift Wrapping)

The Jarvis' March algorithm works as follows:

1. Find the leftmost point (guaranteed to be on the hull).
2. Repeatedly find the point that makes the smallest counter-clockwise angle with the previous hull edge.
3. Continue until returning to the starting point.

This algorithm is simpler but can be slower for large sets of points with many points on the hull.

## Usage

1. **Adding Points**: Click on the canvas to add points.
2. **Selecting an Algorithm**: Use the radio buttons to select either "Graham Scan" or "Jarvis' March".
3. **Adjusting Visualization Speed**: Use the slider to control how quickly the algorithm progresses.
4. **Computing the Convex Hull**: Click the "Compute Convex Hull" button to start the visualization.
5. **Resetting**: Click the "Reset" button to clear all points and start over.

## Visual Elements

- **Black Dots**: Input points.
- **Blue Lines**: Partial hull during construction.
- **Red Lines**: Final convex hull.
- **Green Vertical Line**: Scan line (in Graham Scan).
- **Orange Circle**: Current point on hull (in Jarvis' March).
- **Gray Dashed Line**: Candidate edge (in Jarvis' March).

## Implementation Details

The application is implemented in Python using the Tkinter library for the graphical user interface. The key components include:

- **Point Representation**: Points are stored as (x, y) tuples.
- **Orientation Test**: The `determine_point_orientation` function calculates whether three points make a left turn, right turn, or are collinear.
- **Visualization**: The algorithms are animated step-by-step to help understand how they work.

## Mathematical Background

The core of both algorithms relies on the orientation test, which determines whether three points make a counter-clockwise turn. This is calculated using the cross product:

```
orientation(p1, p2, p3) = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
```

- If orientation > 0: Counter-clockwise turn (left turn)
- If orientation < 0: Clockwise turn (right turn)
- If orientation = 0: Collinear points

## Educational Value

This visualizer is particularly useful for:

- Understanding computational geometry algorithms
- Visualizing how convex hulls are constructed
- Comparing different algorithmic approaches
- Learning about time complexity through visual observation
