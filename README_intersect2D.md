
# Sweep-Line Algorithm Visualization

## Introduction
The purpose of this application is to demonstrate how a sweep-line algorithm can efficiently find all intersections among a set of axis-aligned line segments. The visualization helps in understanding the algorithm's steps and how data structures are used to optimize the process.

---

## Features
1. **Interactive Drawing:** Users can manually draw horizontal and vertical line segments on the canvas by clicking.
2. **Random Segment Generation:** Generate a set of random horizontal and vertical segments for testing.
3. **Adjustable Visualization Speed:** Control the speed of the algorithm's visualization using a slider.
4. **Visual Feedback:** Observe the scan line moving across the canvas and segments changing color to indicate their status.
5. **Intersection Points:** Intersections are marked on the canvas as red circles.

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

---

## Data Structure for Active Segments

### Active Segments List `L`:
- Stores active horizontal segments with their y-coordinate as the key.
- Supports efficient insertion, deletion, and range search operations.

### Algorithm 2: Find Node with Smallest Key ≥ y
Used during the range search in `L` when processing vertical segments.

**Objective:** Find the node `p` in a balanced binary search tree with the smallest key `≥y`.

---

## Code Structure

### Dependencies
- Python 3.x
- Tkinter: For creating the graphical user interface.

### Main Components

#### Data Classes:
- `Point`: Represents a point with x and y coordinates.
- `Segment`: Represents a line segment with start and end points, orientation, and canvas ID.
- `Event`: Represents an event in the sweep-line algorithm with x-coordinate, event order, and associated segment.

#### Event Queue (`event_queue`):
- A min-heap that stores events sorted by x-coordinate and event type.

#### Active Segments List (`L`):
- A list that maintains active horizontal segments sorted by y-coordinate using the bisect module for efficient insertion and range queries.

#### Functions:
- `add_point(event)`: Handles mouse clicks to draw segments.
- `add_segment(start, end)`: Adds a segment to the canvas and the segments list.
- `initialize_event_queue()`: Initializes the event queue with all events.
- `process_events()`: Processes events according to Algorithm 1.
- `draw_scan_line(x)`: Draws the scan line at the given x-coordinate.
- `draw_intersection_point(point)`: Draws a red circle at the intersection point.

#### User Interface Components:
- **Canvas:** The area where segments are drawn and the algorithm is visualized.
- **Sidebar Controls:**
  - "Reset" button: Clears the canvas and resets data structures.
  - "Generate Lines" button: Generates random segments.
  - "Compute Intersections" button: Starts the algorithm.
  - "Visualization Delay" slider: Adjusts the speed of visualization.

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

### Adjusting Visualization Speed
- Use the "Visualization Delay" Slider to adjust the speed of visualization.

### Resetting the Canvas
- **Click "Reset":** Clears all segments and resets the application to its initial state.

---

## Visualization Details

### Scan Line
- **Representation:** A vertical red dashed line.
- **Movement:** Moves from left to right across the canvas.
- **Purpose:** Represents the sweep line in the algorithm, processing events in order.

### Segment Colors
- **Blue:** Segments that have not yet been processed.
- **Green:** Active horizontal segments currently in the active list `L`.
- **Black:** Horizontal segments that are no longer active after being removed from `L`.
- **Vertical Segments:** Change color to black after being processed.

### Intersections
- **Representation:** Small red circles drawn at the intersection points.

---

## Understanding the Code

### Event Queue
- **Structure:** A priority queue (heapq) storing events sorted by x-coordinate and event type.
- **Event Types:**
  - Start Event (0): Left endpoint of a horizontal segment.
  - Vertical Segment Event (1): A vertical segment.
  - End Event (2): Right endpoint of a horizontal segment.
- **Ordering:** Start events are processed before vertical segment events, which are processed before end events at the same x-coordinate.

### Processing Events
1. **Start Event:** Inserts the horizontal segment into the active list `L`.
2. **End Event:** Removes the horizontal segment from `L`.
3. **Vertical Segment Event:** Performs a range search in `L` to find all horizontal segments intersecting the vertical segment.

### Active Segments List
- **Implementation:** A list `L` sorted by y-coordinate using the bisect module.


## Why use a list instead of a tree?

### Time Complexity BST
- **Insertion:** O(log n)
- **Deletion:** O(log n)
- **Range Search:** O(log n + k), where k is the number of elements in the range.

### Time Complexity Sorted List with Bisect
- **Insertion:**
  - Finding insertion point: O(log n) using bisect.insert_left
  - Inserting element: O(n) to shift elements

- **Deletion:**
  - Finding the Deletion Point: O(log n) using bisect.bisect_left
  - Deleting Element: O(n) to shift elements

- **Range Search:**
  - Finding the start and end indices: O(log n) each
  - Collecting elements in the range: O(k), where k is the number of elements in the range

### Concluiosn
In this case the list is more efficient for the given operations, as the number of elements in the list is relatively small and the overhead of maintaining a balanced tree is not justified.


## Possible Extensions
1. **Implementing a Balanced BST:** Replace the list and bisect module with a balanced binary search tree for `L`.
2. **Handling More Complex Geometries:** Extend the algorithm to handle non-axis-aligned segments.
3. **Intersection Counting:** Keep track of the number of intersections found.
4. **Logging and Output:** Provide detailed logs or output files with intersection data.

---

## Conclusion
This application provides an interactive way to visualize how a sweep-line algorithm can efficiently find intersections among axis-aligned line segments. By observing the scan line and segment status changes, users can gain a deeper understanding of computational geometry algorithms and the importance of efficient data structures.
