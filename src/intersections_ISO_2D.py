import tkinter as tk
import time
import heapq
import random
from dataclasses import dataclass, field
from typing import Any

# Create the main application window
root = tk.Tk()
root.title("Axis-Aligned Line Segment Intersections")

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
    sidebar, text="Axis-Aligned Line Intersections", font=("Arial", 18), bg='lightgray', fg='black')
heading_text.pack(pady=5)

# Delay Slider Label
delay_label = tk.Label(
    sidebar, text="Visualization Delay (seconds):", bg='lightgray', fg='black')
delay_label.pack(pady=5)

# Delay Slider
delay_var = tk.DoubleVar(value=0.05)  # Default delay time
delay_slider = tk.Scale(
    sidebar,
    from_=0.0,
    to=1.0,
    resolution=0.01,
    orient='horizontal',
    variable=delay_var
)
delay_slider.pack()

# Reset button
def reset_canvas():
    """Clear the canvas and reset all data structures."""
    global segment_index, scan_line_id, points, segments, event_queue, sss
    canvas.delete("all")
    points.clear()
    segments.clear()
    event_queue.clear()
    sss = AVLTree()  # Reset the AVL Tree
    segment_index = 0
    scan_line_id = None

reset_button = tk.Button(sidebar, text="Reset", command=reset_canvas)
reset_button.pack(pady=5)

# Generate Lines button
def generate_lines():
    """Generate 100 random horizontal and vertical segments."""
    global segment_index
    reset_canvas()
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    for _ in range(100):
        x1 = random.uniform(50, width - 50)
        y1 = random.uniform(50, height - 50)
        if random.choice([True, False]):
            # Horizontal segment
            x2 = random.uniform(50, width - 50)
            y2 = y1
        else:
            # Vertical segment
            x2 = x1
            y2 = random.uniform(50, height - 50)
        start = Point(x1, y1)
        end = Point(x2, y2)
        add_segment(start, end)
    canvas.update()

generate_button = tk.Button(sidebar, text="Generate Lines", command=generate_lines)
generate_button.pack(pady=5)

# Compute Intersections button
def start_computing():
    """Initialize the event queue and start processing events."""
    # Disable the canvas and buttons during computation
    canvas.unbind("<Button-1>")
    compute_button.config(state='disabled')
    reset_button.config(state='disabled')
    delay_slider.config(state='disabled')
    generate_button.config(state='disabled')

    canvas.update_idletasks()  # Ensure the canvas has the correct size
    initialize_event_queue()
    process_events()

    # Re-enable the canvas and buttons after computation
    canvas.bind("<Button-1>", add_point)
    compute_button.config(state='normal')
    reset_button.config(state='normal')
    delay_slider.config(state='normal')
    generate_button.config(state='normal')

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
    canvas_id: int               # Canvas ID for visualization
    orientation: str             # 'horizontal' or 'vertical'

@dataclass(order=True)
class Event:
    """Class representing an event in the sweep line algorithm."""
    x: float                              # X-coordinate of the event
    event_order: int                      # Event priority for ordering (start=0, vertical=1, end=2)
    segment: Any = field(compare=False)   # Associated segment

def add_point(event):
    """Handle mouse click event to add points and create segments."""
    x, y = event.x, event.y
    # Draw a small circle to represent the point
    canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='black', tags="point")
    points.append(Point(x, y))
    if len(points) == 2:
        # When two points are clicked, create a segment
        start, end = points
        add_segment(start, end)
        points.clear()  # Reset points for the next segment
        # remove the point from the canvas
        canvas.delete("point")
        canvas.update()

def add_segment(start, end):
    """Add a segment to the canvas and segments list."""
    global segment_index
    if abs(start.x - end.x) < abs(start.y - end.y):
        # Vertical segment
        x_coord = start.x
        y1, y2 = start.y, end.y
        canvas_id = canvas.create_line(x_coord, y1, x_coord, y2, fill='blue', width=2)
        segment = Segment(Point(x_coord, min(y1, y2)), Point(x_coord, max(y1, y2)), segment_index, canvas_id, 'vertical')
    else:
        # Horizontal segment
        y_coord = start.y
        x1, x2 = start.x, end.x
        canvas_id = canvas.create_line(x1, y_coord, x2, y_coord, fill='blue', width=2)
        segment = Segment(Point(min(x1, x2), y_coord), Point(max(x1, x2), y_coord), segment_index, canvas_id, 'horizontal')
    segments.append(segment)
    segment_index += 1

def initialize_event_queue():
    """Initialize the event queue with start and end events for all segments."""
    event_queue.clear()
    for segment in segments:
        if segment.orientation == 'horizontal':
            # Add start and end events for horizontal segments
            heapq.heappush(event_queue, Event(segment.start.x, 0, segment))
            heapq.heappush(event_queue, Event(segment.end.x, 2, segment))
        else:
            # Add vertical segment event
            heapq.heappush(event_queue, Event(segment.start.x, 1, segment))

def process_events():
    """Process all events in the event queue."""
    global current_x, scan_line_id
    while event_queue:
        event = heapq.heappop(event_queue)
        current_x = event.x

        # Draw or update the scan line
        draw_scan_line(current_x)

        if event.event_order == 0:
            handle_start_event(event)
        elif event.event_order == 2:
            handle_end_event(event)
        elif event.event_order == 1:
            handle_vertical_segment(event)
        else:
            raise ValueError(f"Unknown event order: {event.event_order}")

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
    scan_line_id = canvas.create_line(x, 0, x, canvas.winfo_height(), fill='red', dash=(4, 2), width=2)

def handle_start_event(event):
    """Handle start event: add horizontal segment to SSS."""
    segment = event.segment
    # Add the segment to the AVL Tree
    sss.add_segment(segment)
    # Change the color of the segment to indicate it's active (green)
    canvas.itemconfig(segment.canvas_id, fill='green')

def handle_end_event(event):
    """Handle end event: remove horizontal segment from SSS."""
    segment = event.segment
    # Remove the segment from SSS
    sss.remove_segment(segment)
    # Change the color of the segment to indicate it's dead (black)
    canvas.itemconfig(segment.canvas_id, fill='black')

def handle_vertical_segment(event):
    """Handle vertical segment: check for intersections with active horizontal segments."""
    segment = event.segment
    # Change the color of the vertical segment to indicate it's being active (green)
    canvas.itemconfig(segment.canvas_id, fill='green')
    # Get all horizontal segments in SSS that intersect with the vertical segment's y-range
    overlapping_segments = sss.get_overlapping_segments(segment.start.y, segment.end.y)
    for h_segment in overlapping_segments:
        draw_intersection_point(Point(segment.start.x, h_segment.start.y))
    # After processing, change the color of the vertical segment to indicate it's dead (black)
    canvas.itemconfig(segment.canvas_id, fill='black')

def draw_intersection_point(point):
    """Draw a red circle to represent an intersection point."""
    x, y = point.x, point.y
    # create a red circle with no infill and red border
    canvas.create_oval(x - 3, y - 3, x + 3, y + 3, outline='red', tags="intersection")
    # No need to update or sleep here

# AVL Tree Node Class
class AVLNode:
    """Node class for AVL Tree."""
    def __init__(self, segment):
        self.segment = segment  # Horizontal line segment stored in this node
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
        return node.height if node else 0

    def _update_height(self, node):
        """Update height of a node."""
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        """Balance factor of a node."""
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y):
        """Right rotation."""
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        self._update_height(y)
        self._update_height(x)

        return x

    def _rotate_left(self, x):
        """Left rotation."""
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

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

    def _insert(self, node, segment):
        """Insert a segment into the AVL tree."""
        if not node:
            return AVLNode(segment)
        if segment.start.y < node.segment.start.y:
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

        if segment.start.y < node.segment.start.y:
            node.left = self._delete(node.left, segment)
        elif segment.start.y > node.segment.start.y:
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

    def get_overlapping_segments(self, y_start, y_end):
        """Get all segments that overlap with the given y-range."""
        result = []
        self._collect_overlaps(self.root, y_start, y_end, result)
        return result

    def _collect_overlaps(self, node, y_start, y_end, result):
        """
        Recursively collect overlapping segments within a given y-coordinate range.

        Args:
            node (Node): The current node in the segment tree.
            y_start (float): The starting y-coordinate of the range.
            y_end (float): The ending y-coordinate of the range.
            result (list): A list to store the overlapping segments.

        Returns:
            None: This function modifies the result list in place.

        """
        #  If the current node is None, return immediately (base case for recursion)
        if not node:
            return
        seg_y = node.segment.start.y
        # If the segment's y-coordinate is within the specified range [y_start, y_end], add the segment to the result list
        if seg_y >= y_start and seg_y <= y_end:
            result.append(node.segment)
        # If there is a left child and the segment's y-coordinate is greater than or equal to y_start, recursively check the left subtree
        if node.left and seg_y >= y_start:
            self._collect_overlaps(node.left, y_start, y_end, result)
        # If there is a right child and the segment's y-coordinate is less than or equal to y_end, recursively check the right subtree
        if node.right and seg_y <= y_end:
            self._collect_overlaps(node.right, y_start, y_end, result)

# Initialize the AVL Tree for the SSS
sss = AVLTree()

# Bind the mouse click event to the canvas
canvas.bind("<Button-1>", add_point)

# Start the Tkinter event loop
root.mainloop()
