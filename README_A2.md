# Line Segment Intersection Visualizer

## Overview

This application provides an interactive visualization of the Bentley-Ottmann sweep-line algorithm for finding all intersections among arbitrary line segments in the 2D plane. The algorithm efficiently finds all intersection points without checking every possible pair of segments, making it suitable for large sets of line segments.

## Features

- **Interactive Segment Drawing**: Click on the canvas to define line segments.
- **Visualization Speed Control**: Adjust the delay between visualization steps.
- **Step-by-Step Visualization**: Watch how the sweep-line algorithm processes events and detects intersections.
- **Reset Functionality**: Clear all segments and start over.

## Algorithm Details

### Bentley-Ottmann Sweep-Line Algorithm

The Bentley-Ottmann algorithm works by sweeping a vertical line from left to right across the plane, processing events in order of their x-coordinates:

1. **Event Types**:
   - **Start Event**: Left endpoint of a segment
   - **End Event**: Right endpoint of a segment
   - **Intersection Event**: Point where two segments intersect

2. **Data Structures**:
   - **Event Queue**: Priority queue of events sorted by x-coordinate
   - **Sweep-Line Status (SSS)**: Balanced binary search tree (AVL tree) that maintains the segments intersecting the sweep line, sorted by y-coordinate

3. **Algorithm Steps**:
   - Initialize the event queue with start and end events for all segments
   - While the event queue is not empty:
     - Process the next event (leftmost in x-coordinate)
     - For start events: Insert the segment into the SSS and check for intersections with neighboring segments
     - For end events: Remove the segment from the SSS and check for new intersections between its neighbors
     - For intersection events: Report the intersection, swap the segments in the SSS, and check for new intersections

4. **Time Complexity**: O((n + k) log n), where n is the number of segments and k is the number of intersections

## Usage

1. **Adding Segments**: Click on the canvas to define the endpoints of line segments. Two consecutive clicks define one segment.
2. **Adjusting Visualization Speed**: Use the slider to control how quickly the algorithm progresses.
3. **Computing Intersections**: Click the "Compute Intersections" button to start the visualization.
4. **Resetting**: Click the "Reset" button to clear all segments and start over.

## Visual Elements

- **Black Lines**: Input line segments.
- **Green Lines**: Active segments currently intersecting the sweep line.
- **Black Lines**: Processed segments.
- **Blue Vertical Line**: Sweep line moving from left to right.
- **Red Circles**: Detected intersection points.

## Implementation Details

The application is implemented in Python using the Tkinter library for the graphical user interface. The key components include:

- **Segment Representation**: Each segment is represented by its start and end points.
- **AVL Tree**: A self-balancing binary search tree implementation for the sweep-line status structure.
- **Event Handling**: Events are processed in order of x-coordinate, with tie-breaking based on event type.
- **Intersection Detection**: Geometric calculations to determine if and where two line segments intersect.

## Mathematical Background

### Line Segment Intersection

Two line segments intersect if they share a common point. The intersection point can be calculated using the parametric form of the line equations:

```
p1 + t1 * (p2 - p1) = p3 + t2 * (p4 - p3)
```

where p1, p2 are the endpoints of the first segment, p3, p4 are the endpoints of the second segment, and t1, t2 are parameters in the range [0, 1].

### Segment Ordering in the SSS

At a given x-coordinate, segments are ordered in the SSS by their y-coordinates at that x-position. For non-vertical segments, the y-coordinate is calculated using the line equation:

```
y = m * (x - x1) + y1
```

where m is the slope of the segment, and (x1, y1) is one of its endpoints.

## Challenges and Solutions

### Numerical Precision

Floating-point calculations can lead to precision issues. The implementation uses a small epsilon value to handle these cases:

```python
epsilon = 1e-9  # Small value for floating-point comparison
```

### Degenerate Cases

The algorithm handles various degenerate cases:
- Vertical segments
- Segments with the same endpoint
- Collinear segments
- Segments that intersect at an endpoint

## Educational Value

This visualizer is particularly useful for:
- Understanding computational geometry algorithms
- Visualizing how the sweep-line paradigm works
- Learning about efficient intersection detection
- Seeing how balanced binary search trees are used in geometric algorithms
