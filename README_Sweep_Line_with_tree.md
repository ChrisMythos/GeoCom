
# Axis-Aligned Line Segment Intersections Visualization with AVL Tree

## Introduction
This project is a Python application that visualizes the process of finding all intersections among axis-aligned (horizontal and vertical) line segments using a sweep-line algorithm. The application provides an interactive interface where users can draw segments, generate random segments, and observe the algorithm in action with adjustable visualization speed.

---

## Features
1. **Interactive Drawing:** Users can manually draw horizontal and vertical line segments on the canvas by clicking.
2. **Random Segment Generation:** Generate a set of random horizontal and vertical segments for testing.
3. **Adjustable Visualization Speed:** Control the speed of the algorithm's visualization using a slider.
4. **Visual Feedback:** Observe the scan line moving across the canvas and segments changing color to indicate their status.
5. **Intersection Points:** Intersections are marked on the canvas as red circles.
6. **Intersection Counting:** Displays the total number of intersections found after processing.

---

## Algorithm Overview

### Algorithm 1: Intersect Iso-Oriented Line Segments
**Objective:** Given `n` iso-oriented (axis-aligned) line segments, find all their intersections.

#### Steps:
1. **Initialize Event Queue `Q` with all events sorted by x-coordinate:**
   - Start events (left endpoints) of horizontal segments.
   - End events (right endpoints) of horizontal segments.
   - Vertical segments (treated as events at their x-coordinate).
2. **Initialize Active Segments List `L=∅`:**
   - `L` will store active horizontal segments, sorted by y-coordinate.
3. **Process Events while `Q` is not empty:**
   - Take the next event `p` from `Q`.
   - If `p` is the left endpoint of a horizontal segment `s`:
     - Insert `s` into `L`.
   - Else if `p` is the right endpoint of a horizontal segment `s`:
     - Remove `s` from `L`.
   - Else `p` is a vertical segment:
     - Determine all horizontal segments `t` in `L` where `t.y ∈ [y_low, y_high]` (the y-range of the vertical segment).
     - Report intersections between `t` and the vertical segment.
     - Increment the intersection counter.

---

### Data Structure for Active Segments

#### Active Segments List `L`:
- Implemented as a balanced binary search tree (AVL tree) with successor links.
- Stores active horizontal segments with their y-coordinate as the key.
- Supports efficient insertion, deletion, and range search operations.

---

### Algorithm 2: Find Node with Smallest Key ≥ y
Used during the range search in `L` when processing vertical segments.

#### Objective:
Find the node `p` in a balanced binary search tree with the smallest key `≥y`.

---

## Code Structure

### Dependencies
- Python 3.x
- Tkinter: For creating the graphical user interface.

---

### Main Components

#### Data Classes:
- `Point`: Represents a point with x and y coordinates.
- `Segment`: Represents a line segment with start and end points, orientation, and canvas ID.
- `Event`: Represents an event in the sweep-line algorithm with x-coordinate, event order, and associated segment.

#### Event Queue (`event_queue`):
- A min-heap that stores events sorted by x-coordinate and event type.

#### Active Segments List (`L`):
- Implemented as an AVL tree with successor links.
- Manages active horizontal segments sorted by y-coordinate.

---

## How to Use the Application

### Drawing Segments Manually
1. **Click on the Canvas:** Each click adds a point.
2. **Define Segments:** Two consecutive clicks define a line segment.
3. **Repeat:** Continue clicking to add more segments.

### Generating Random Segments
1. **Click "Generate Lines":** The application will generate a set of random horizontal and vertical segments.

### Starting the Algorithm
1. **Click "Compute Intersections":** Begins processing the events.
2. **Observe:** Watch as the scan line moves across the canvas and intersections are detected.

---

## Visualization Details

### Scan Line
- **Representation:** A vertical red dashed line.
- **Movement:** Moves from left to right across the canvas.

---

## Possible Extensions
1. **Handling More Complex Geometries:** Extend the algorithm to handle non-axis-aligned segments.
2. **Performance Analysis:** Measure the performance of the algorithm with different data structures or optimizations.

---



## Conclusion
This application provides an interactive way to visualize how a sweep-line algorithm can efficiently find intersections among axis-aligned line segments. The implementation of a balanced BST (AVL tree) and intersection counting enhances the educational value of the application.

