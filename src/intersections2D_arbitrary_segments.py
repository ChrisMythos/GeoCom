import tkinter as tk
import time
import heapq
from dataclasses import dataclass, field
from typing import Any

# Create the main application window
root = tk.Tk()
root.title("Line Segment Intersections")

# Set the window size
root.geometry("1000x800")

# Configure the grid layout (2 columns, 1 row)
root.grid_columnconfigure(0, weight=0)  # Sidebar column does not expand
root.grid_columnconfigure(1, weight=1)  # Canvas column expands
root.grid_rowconfigure(0, weight=1)     # Row expands vertically

# Create a frame for the sidebar
sidebar = tk.Frame(root, width=200, bg='lightgray', padx=10, pady=10)
sidebar.grid(row=0, column=0, sticky="ns")

# Label for heading of the sidebar
heading_text = tk.Label(
    sidebar, text="Line Segment Intersections", font=("Arial", 20), bg='lightgray', fg='black')
heading_text.pack(pady=5)

# Delay Slider Label
delay_label = tk.Label(
    sidebar, text="Visualization Delay (seconds):", bg='lightgray', fg='black')
delay_label.pack(pady=5)

# Delay Slider
delay_var = tk.DoubleVar(value=0.1)  # Default delay time
delay_slider = tk.Scale(
    sidebar,
    from_=0.0,
    to=2.0,
    resolution=0.05,
    orient='horizontal',
    variable=delay_var
)
delay_slider.pack()

# Reset button
def reset_canvas():
    """Clear the canvas and reset all data structures."""
    global segment_index, scan_line_id, points, segments, event_queue, sss, processed_intersections
    canvas.delete("all")
    points.clear()
    segments.clear()
    event_queue.clear()
    sss = AVLTree()  # Reset the AVL Tree
    segment_index = 0
    scan_line_id = None
    processed_intersections.clear()

reset_button = tk.Button(sidebar, text="Reset", command=reset_canvas)
reset_button.pack(pady=5)


# Compute Intersections button
def start_computing():
    """Initialize the event queue and start processing events."""
    # Disable the canvas and buttons during computation
    canvas.unbind("<Button-1>")
    compute_button.config(state='disabled')
    reset_button.config(state='disabled')
    delay_slider.config(state='disabled')

    canvas.update_idletasks()  # Ensure the canvas has the correct size
    initialize_event_queue()
    process_events()

    # Re-enable the canvas and buttons after computation
    canvas.bind("<Button-1>", add_point)
    compute_button.config(state='normal')
    reset_button.config(state='normal')
    delay_slider.config(state='normal')

compute_button = tk.Button(sidebar, text="Compute Intersections", command=start_computing)
compute_button.pack(pady=5)

# Create the canvas for drawing line segments
canvas = tk.Canvas(root, bg='white')
canvas.grid(row=0, column=1, sticky="nsew")

# Store the segments and points
segments = []      # List to store all segments
segment_index = 0  # Unique index for each segment
points = []        # Temporary list to store points when drawing segments

# Event queue and Sweep Line Status Structure (SSS)
event_queue = []   # Priority queue (min-heap) for events
current_x = 0      # Global variable to keep track of the scan line position

# Initialize the AVL Tree for the SSS
sss = None  # Will be initialized in reset_canvas

# Canvas item ID for the scan line
scan_line_id = None

# Keep track of processed intersections to avoid duplicates
processed_intersections = set()

@dataclass
class Point:
    """Class representing a point with x and y coordinates."""
    x: float
    y: float

@dataclass
class Segment:
    """Class representing a line segment with a start and end point."""
    start: Point
    end: Point
    index: int                   # Unique index for the segment
    canvas_id: int = field(default=None, compare=False)  # Canvas ID for visualization

    def get_y_at_scanline(self, x):
        """Calculate the y-coordinate of the segment at the given x-coordinate."""
        p1, p2 = self.start, self.end
        if p1.x == p2.x:
            # Vertical segment; return y-coordinate of the higher point (smaller y in canvas)
            return min(p1.y, p2.y)
        else:
            # Calculate y using the line equation
            m = (p2.y - p1.y) / (p2.x - p1.x)
            return m * (x - p1.x) + p1.y
        
    def slope(self):
        """Calculate the slope of the segment."""
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        if dx == 0:
            return float('inf')  # Vertical line
        else:
            return dy / dx

@dataclass(order=True)
class Event:
    """Class representing an event in the sweep line algorithm."""
    x: float                              # X-coordinate of the event
    event_order: int                      # Event priority for ordering (start=0, intersection=1, end=2)
    point: Point = field(compare=False)   # Point where the event occurs
    event_type: str = field(compare=False)# Type of the event ('start', 'end', 'intersection')
    segment: Any = field(compare=False, default=None)       # Associated segment (for start/end events)
    segment_up: Any = field(compare=False, default=None)    # Upper segment (for intersection events)
    segment_low: Any = field(compare=False, default=None)   # Lower segment (for intersection events)

def add_point(event):
    """Handle mouse click event to add points and create segments."""
    global segment_index
    x, y = event.x, event.y
    # Draw a small circle to represent the point
    canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill='black', tags="point")
    points.append(Point(x, y))
    if len(points) == 2:
        # When two points are clicked, create a segment
        start, end = points
        segment = Segment(start, end, segment_index)
        segment_index += 1
        # Draw the line and store its canvas ID
        canvas_id = canvas.create_line(start.x, start.y, end.x, end.y, fill='black', tags="segment")
        segment.canvas_id = canvas_id
        segments.append(segment)
        points.clear()  # Reset points for the next segment

def initialize_event_queue():
    """Initialize the event queue with start and end events for all segments."""
    event_queue.clear()
    for segment in segments:
        # Ensure left to right ordering of segment endpoints
        if segment.start.x > segment.end.x:
            segment.start, segment.end = segment.end, segment.start
        # Add start event with event_order = 0
        heapq.heappush(event_queue, Event(segment.start.x, 0, segment.start, event_type='start', segment=segment))
        # Add end event with event_order = 2
        heapq.heappush(event_queue, Event(segment.end.x, 2, segment.end, event_type='end', segment=segment))

def process_events():
    """Process all events in the event queue."""
    global current_x, scan_line_id
    intersections = []  # List to store intersection points
    # As long as there are events in the queue to process
    while event_queue:
        # Get the next event from the queue 
        event = heapq.heappop(event_queue)
        current_x = event.x

        # Draw or update the scan line
        draw_scan_line(current_x)

        if event.event_type == 'start':
            handle_start_event(event, intersections)
        elif event.event_type == 'end':
            handle_end_event(event, intersections)
        elif event.event_type == 'intersection':
            handle_intersection_event(event, intersections)
        else:
            raise ValueError(f"Unknown event type: {event.event_type}")

        # Add a small delay for visualization
        canvas.update()
        time.sleep(delay_var.get())

    # Remove the scan line after processing is complete
    if scan_line_id is not None:
        canvas.delete(scan_line_id)

def draw_scan_line(x):
    """Draw the vertical scan line at position x."""
    global scan_line_id
    # Remove the previous scan line if it exists
    if scan_line_id is not None:
        canvas.delete(scan_line_id)
    # Draw the new scan line
    scan_line_id = canvas.create_line(x, 0, x, canvas.winfo_height(), fill='blue', dash=(4, 2), width=2)

def handle_start_event(event, intersections):
    """Handle start event: add segment to SSS and check for intersections."""
    segment = event.segment

    # Add the segment to the SSS
    sss.add_segment(segment)

    # Change the color of the segment to green to indicate it's active 
    canvas.itemconfig(segment.canvas_id, fill='green')

    # Get predecessor and successor in SSS (segments above and below in the ca)
    pred_segment = sss.predecessor(segment)
    succ_segment = sss.successor(segment)

    # Check for intersections with neighboring segments
    if pred_segment:
        check_and_add_intersection(segment, pred_segment)
    if succ_segment:
        check_and_add_intersection(segment, succ_segment)

def handle_end_event(event, intersections):
    """Handle end event: remove segment from SSS and check for new intersections."""
    segment = event.segment

    # Change the color of the segment back to black to indicate it's inactive
    canvas.itemconfig(segment.canvas_id, fill='black')

    # Get predecessor and successor in SSS before removing the segment
    pred_segment = sss.predecessor(segment)
    succ_segment = sss.successor(segment)

    # Remove the segment from SSS
    sss.remove_segment(segment)

    # If predecessor and successor exist, check for intersections between them
    if pred_segment and succ_segment:
        check_and_add_intersection(pred_segment, succ_segment)

def handle_intersection_event(event, intersections):
    """Handle intersection event: report intersection, swap segments, and check for new intersections."""
    seg_up = event.segment_up
    seg_low = event.segment_low

    # Report intersection by drawing it
    intersections.append(event.point)
    draw_intersection_point(event.point)

    # Remove segments from AVL Tree
    sss.remove_segment(seg_up)
    sss.remove_segment(seg_low)

    # Swap the positions of the segments
    seg_up, seg_low = seg_low, seg_up

    # Re-insert segments into AVL Tree
    sss.add_segment(seg_up)
    sss.add_segment(seg_low)

    # Get new neighbors after swapping
    pred_segment = sss.predecessor(seg_low)
    succ_segment = sss.successor(seg_up)

    # Check id the activated segment has new intersections with neighbors 
    if pred_segment:
        check_and_add_intersection(seg_low, pred_segment)
    if succ_segment:
        check_and_add_intersection(seg_up, succ_segment)

def check_and_add_intersection(s1, s2):
    """Check if two segments intersect and add an intersection event if they do."""
    point = compute_intersection(s1, s2)
    if point and point.x >= current_x:
        # Create a unique key for the pair of segments
        segments_pair = tuple(sorted((s1.index, s2.index)))
        # Check if the intersection has already been processed to avoid duplicates
        if segments_pair not in processed_intersections:
            processed_intersections.add(segments_pair)
            # Create an intersection event and add it to the event queue
            event = Event(point.x, 1, point, event_type='intersection', segment_up=s1, segment_low=s2)
            heapq.heappush(event_queue, event)

def compute_intersection(s1, s2):
    """Compute the intersection point between two segments, if it exists."""
    # Get them start and endpoints of the segments
    p1, p2 = s1.start, s1.end
    p3, p4 = s2.start, s2.end

    # compute slopes of the segments
    m = (p1.x - p2.x)*(p3.y - p4.y) - (p1.y - p2.y)*(p3.x - p4.x)
    epsilon = 1e-9  # Small value for floating-point comparison, this is done to avoid precision errors
    if abs(m) < epsilon:
        # Lines are parallel or coincident
        return None

    # Compute numerators 
    num_x = (p1.x*p2.y - p1.y*p2.x)*(p3.x - p4.x) - (p1.x - p2.x)*(p3.x*p4.y - p3.y*p4.x)
    num_y = (p1.x*p2.y - p1.y*p2.x)*(p3.y - p4.y) - (p1.y - p2.y)*(p3.x*p4.y - p3.y*p4.x)

    # Calculate intersection point
    x = num_x / m
    y = num_y / m

    # Check if the intersection point is within both segments (with a small epsilon to avoid precision errors)
    if (min(p1.x, p2.x) - epsilon <= x <= max(p1.x, p2.x) + epsilon and
        min(p3.x, p4.x) - epsilon <= x <= max(p3.x, p4.x) + epsilon and
        min(p1.y, p2.y) - epsilon <= y <= max(p1.y, p2.y) + epsilon and
        min(p3.y, p4.y) - epsilon <= y <= max(p3.y, p4.y) + epsilon):
        return Point(x, y)
    else:
        return None

def draw_intersection_point(point):
    """Draw a red circle to represent an intersection point."""
    x, y = point.x, point.y
    canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill='red', tags="intersection")
    # No need to update or sleep here

# AVL Tree Node Class
class AVLNode:
    """Node class for AVL Tree."""
    def __init__(self, segment):
        self.segment = segment  # Line segment stored in this node
        self.height = 1         # Height of the node
        self.left = None        # Left child
        self.right = None       # Right child

# AVL Tree Class for SSS
class AVLTree:
    """AVL Tree implementation for the Scan-Line Status Structure."""
    def __init__(self):
        self.root = None

    def _height(self, node):
        """Get height of a node."""
        if not node:
            return 0
        return node.height

    def _update_height(self, node):
        """Update height of a node."""
        if node:
            node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        """Balance factor of a node."""
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y):
        """Right rotation."""
        x = y.left
        T = x.right

        # Perform rotation
        x.right = y
        y.left = T

        # Update heights
        self._update_height(y)
        self._update_height(x)

        return x

    def _rotate_left(self, x):
        """Left rotation."""
        y = x.right
        T = y.left

        # Perform rotation
        y.left = x
        x.right = T

        # Update heights
        self._update_height(x)
        self._update_height(y)

        return y

    def _balance(self, node):
        """Balancing the tree."""
        self._update_height(node)
        balance = self._balance_factor(node)

        # Left-heavy
        if balance > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right-heavy
        if balance < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _compare(self, segment1, segment2):
        """Compare two segments based on their y-coordinate slightly after the scan-line."""
        global current_x
        epsilon = 1e-9  # A small value to move slightly past the current x
        x = current_x + epsilon
        y1 = segment1.get_y_at_scanline(x)
        y2 = segment2.get_y_at_scanline(x)
        if abs(y1 - y2) < epsilon:
            # If y-coordinates are still equal, compare slopes to break the tie
            m1 = segment1.slope()
            m2 = segment2.slope()
            if m1 == m2:
                return segment1.index - segment2.index
            elif m1 > m2:
                return 1
            else:
                return -1
        elif y1 < y2:
            return -1
        else:
            return 1

    def _insert(self, node, segment):
        """Insert a segment into the AVL tree."""
        if not node:
            return AVLNode(segment)

        if self._compare(segment, node.segment) < 0:
            node.left = self._insert(node.left, segment)
        else:
            node.right = self._insert(node.right, segment)

        # Balance the tree
        return self._balance(node)

    def add_segment(self, segment):
        """Public method to add a segment."""
        self.root = self._insert(self.root, segment)

    def _delete(self, node, segment):
        """Delete a segment from the AVL tree."""
        if not node:
            return None

        if self._compare(segment, node.segment) < 0:
            node.left = self._delete(node.left, segment)
        elif self._compare(segment, node.segment) > 0:
            node.right = self._delete(node.right, segment)
        else:
            # Node to delete found
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Replace with the smallest value in the right subtree
            temp = self._min_value_node(node.right)
            node.segment = temp.segment
            node.right = self._delete(node.right, temp.segment)

        # Balance the tree
        return self._balance(node)

    def remove_segment(self, segment):
        """Public method to remove a segment."""
        self.root = self._delete(self.root, segment)

    def _min_value_node(self, node):
        """Find the segment with the smallest y-coordinate."""
        current = node
        while current.left:
            current = current.left
        return current

    def _max_value_node(self, node):
        """Find the segment with the largest y-coordinate."""
        current = node
        while current.right:
            current = current.right
        return current

    def predecessor(self, segment):
        """Find the predecessor of a segment."""
        predecessor = None
        node = self.root
        while node:
            cmp_result = self._compare(segment, node.segment)
            if cmp_result <= 0:
                node = node.left
            else:
                predecessor = node.segment
                node = node.right
        return predecessor

    def successor(self, segment):
        """Find the successor of a segment."""
        successor = None
        node = self.root
        while node:
            cmp_result = self._compare(segment, node.segment)
            if cmp_result >= 0:
                node = node.right
            else:
                successor = node.segment
                node = node.left
        return successor

# Initialize the AVL Tree for the SSS
sss = AVLTree()

# Bind the mouse click event to the canvas
canvas.bind("<Button-1>", add_point)

# Start the Tkinter event loop
root.mainloop()
