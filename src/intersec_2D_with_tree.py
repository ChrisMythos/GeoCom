import time
import tkinter as tk
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

# Global variables
segments = []       # List to store all segments
points = []         # Temporary list to store points when drawing segments
event_queue = []    # Priority queue (min-heap) for events
scan_line_id = None  # Canvas item ID for the scan line
current_x = 0       # Current x-coordinate of the scan line
intersection_count = 0  # Counter for intersections found


@dataclass(order=True)
class Event:
    """Class representing an event in the sweep line algorithm."""
    x: float                              # X-coordinate of the event
    # Event priority for ordering (start=0, vertical=1, end=2)
    event_order: int
    segment: Any = field(compare=False)   # Associated segment


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
    orientation: str             # 'horizontal' or 'vertical'
    canvas_id: int               # Canvas ID for visualization


# Create the canvas for drawing line segments
canvas = tk.Canvas(root, bg='white')
canvas.grid(row=0, column=1, sticky="nsew")


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


def add_segment(start, end):
    """Add a segment to the canvas and segments list."""
    if abs(start.x - end.x) < abs(start.y - end.y):
        # Vertical segment
        x_coord = start.x
        y1, y2 = start.y, end.y
        canvas_id = canvas.create_line(
            x_coord, y1, x_coord, y2, fill='blue', width=2)
        segment = Segment(Point(x_coord, min(y1, y2)), Point(
            x_coord, max(y1, y2)), 'vertical', canvas_id)
    else:
        # Horizontal segment
        y_coord = start.y
        x1, x2 = start.x, end.x
        canvas_id = canvas.create_line(
            x1, y_coord, x2, y_coord, fill='blue', width=2)
        segment = Segment(Point(min(x1, x2), y_coord), Point(
            max(x1, x2), y_coord), 'horizontal', canvas_id)
    segments.append(segment)


def initialize_event_queue():
    """Initialize the event queue with all events sorted by x-coordinate."""
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
    global scan_line_id, current_x, intersection_count

    L = AVLTree()

    while event_queue:
        event = heapq.heappop(event_queue)
        current_x = event.x

        # Draw or update the scan line
        draw_scan_line(current_x)

        segment = event.segment

        if event.event_order == 0:
            # Left endpoint of horizontal segment
            # Insert segment into L
            L.insert_value(segment.start.y, segment)
            # Change the color to indicate active segment
            canvas.itemconfig(segment.canvas_id, fill='green')
        elif event.event_order == 2:
            # Right endpoint of horizontal segment
            # Remove segment from L
            L.delete_value(segment.start.y, segment)
            # Change the color to indicate inactive segment
            canvas.itemconfig(segment.canvas_id, fill='black')
        elif event.event_order == 1:
            # Vertical segment
            # Determine all horizontal segments t in L whose y-coordinate t.y is in [y_l, y_u]
            y_l = min(segment.start.y, segment.end.y)
            y_u = max(segment.start.y, segment.end.y)
            # Perform range search in L
            results = L.search_range(y_l, y_u)
            for h_segment in results:
                # Report intersection
                draw_intersection_point(
                    Point(segment.start.x, h_segment.start.y))
                intersection_count += 1  # Increment intersection count
            # Change the color to indicate processed vertical segment
            canvas.itemconfig(segment.canvas_id, fill='black')
        else:
            raise ValueError(f"Unknown event order: {event.event_order}")

        # Update the canvas and add delay
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
    scan_line_id = canvas.create_line(
        x, 0, x, canvas.winfo_height(), fill='red', dash=(4, 2), width=2)


def draw_intersection_point(point):
    """Draw a red circle to represent an intersection point."""
    x, y = point.x, point.y
    canvas.create_oval(x - 3, y - 3, x + 3, y + 3,
                       outline='red', width=2, tags="intersection")

# AVL Tree implementation


class Node:
    def __init__(self, key, segment=None):
        self.key = key               # y-coordinate of the segment
        self.segment = segment       # Pointer to the line segment object
        self.left = None             # Left child
        self.right = None            # Right child
        self.height = 1              # Height of the subtree
        self.successor = None        # In-order successor


class AVLTree:
    def __init__(self):
        self.root = None

    # Utility function to get the height of the tree
    def height(self, node):
        return node.height if node else 0

    # Utility function to calculate balance factor of node
    def get_balance(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    # Right rotate subtree rooted with y
    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))

        # Successor pointers remain valid after rotation
        return x

    # Left rotate subtree rooted with x
    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        # Successor pointers remain valid after rotation
        return y

    # Insert a node and update successor pointers
    def insert(self, node, key, segment=None, predecessor=None, successor=None):
        # Perform standard BST insert
        if not node:
            new_node = Node(key, segment)
            new_node.successor = successor
            if predecessor:
                predecessor.successor = new_node
            return new_node

        if key < node.key:
            # Current node is potential successor
            node.left = self.insert(node.left, key, segment, predecessor, node)
        elif key > node.key:
            # Current node is potential predecessor
            node.right = self.insert(node.right, key, segment, node, successor)
        else:
            # Handle duplicate keys by comparing segment IDs
            if id(segment) < id(node.segment):
                node.left = self.insert(
                    node.left, key, segment, predecessor, node)
            else:
                node.right = self.insert(
                    node.right, key, segment, node, successor)

        # Update height of this ancestor node
        node.height = 1 + max(self.height(node.left), self.height(node.right))

        # Get the balance factor to check whether this node became unbalanced
        balance = self.get_balance(node)

        # Balance the tree
        # Left Left Case
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

        # Right Right Case
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    # Delete a node and update successor pointers
    def delete(self, node, key, predecessor=None, successor=None):
        # Perform standard BST delete
        if not node:
            return node

        if key < node.key:
            # Current node is potential successor
            node.left = self.delete(node.left, key, predecessor, node)
        elif key > node.key:
            # Current node is potential predecessor
            node.right = self.delete(node.right, key, node, successor)
        else:
            # Node with one child or no child
            if not node.left or not node.right:
                temp = node.left if node.left else node.right

                if temp:
                    temp.successor = node.successor
                if predecessor:
                    predecessor.successor = node.successor
                else:
                    # If deleting the root node with no predecessor
                    if temp:
                        temp.successor = node.successor

                node = temp  # Replace node with its child (could be None)
            else:
                # Node with two children:
                # Get the inorder successor (smallest in the right subtree)
                temp = self.min_value_node(node.right)

                # Copy the inorder successor's data to this node
                node.key = temp.key
                node.segment = temp.segment

                # Delete the inorder successor
                node.right = self.delete(node.right, temp.key, node, successor)

        if not node:
            return node

        # Update height
        node.height = 1 + max(self.height(node.left), self.height(node.right))

        # Balance the tree
        balance = self.get_balance(node)

        # Left Left Case
        if balance > 1 and self.get_balance(node.left) >= 0:
            node = self.right_rotate(node)
        # Left Right Case
        elif balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            node = self.right_rotate(node)
        # Right Right Case
        elif balance < -1 and self.get_balance(node.right) <= 0:
            node = self.left_rotate(node)
        # Right Left Case
        elif balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            node = self.left_rotate(node)

        # Dirty fix: Ensure that the successor of the highest node is None
        if node.successor == node:
            node.successor = None

        return node

    # Find the node with minimum key >= value
    def find_min_ge(self, node, value):
        """Find the node with the minimum key >= given value."""
        if not node:
            return None
        if node.key == value:
            return node
        elif node.key < value:
            return self.find_min_ge(node.right, value)
        else:
            # node.key > value
            left_result = self.find_min_ge(node.left, value)
            return left_result if left_result else node

    def search_range(self, low, high):
        """Search for all segments in the given y-range using successor pointers."""
        result = []
        node = self.find_min_ge(self.root, low)
        while node and node.key <= high:
            result.append(node.segment)
            node = node.successor
        return result

    # Public methods to insert and delete values

    def insert_value(self, key, segment=None):
        self.root = self.insert(self.root, key, segment)

    def delete_value(self, key, segment):
        self.root = self.delete(self.root, key, segment)

    # Helper methods
    def min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    # For debugging: In-order traversal (optional)
    def inorder(self, node):
        if not node:
            return []
        return self.inorder(node.left) + [(node.key, node.segment)] + self.inorder(node.right)

# Buttons and Controls


def reset_canvas():
    """Clear the canvas and reset all data structures."""
    global segments, points, event_queue, scan_line_id, intersection_count
    canvas.delete("all")
    points.clear()
    segments.clear()
    event_queue.clear()
    scan_line_id = None  # Reset the scan line ID
    intersection_count = 0  # Reset intersection count


reset_button = tk.Button(sidebar, text="Reset", command=reset_canvas)
reset_button.pack(pady=5)


def start_computing():
    """Initialize the event queue and start processing events."""
    # Disable the canvas and buttons during computation
    canvas.unbind("<Button-1>")
    compute_button.config(state='disabled')
    reset_button.config(state='disabled')
    delay_slider.config(state='disabled')
    generate_button.config(state='disabled')

    initialize_event_queue()
    process_events()

    # Re-enable the canvas and buttons after computation
    canvas.bind("<Button-1>", add_point)
    compute_button.config(state='normal')
    reset_button.config(state='normal')
    delay_slider.config(state='normal')
    generate_button.config(state='normal')


compute_button = tk.Button(
    sidebar, text="Compute Intersections", command=start_computing)
compute_button.pack(pady=5)


def generate_lines():
    """Generate random horizontal and vertical segments."""
    reset_canvas()
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    for _ in range(50):
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


generate_button = tk.Button(
    sidebar, text="Generate Lines", command=generate_lines)
generate_button.pack(pady=5)

# Bind the mouse click event to the canvas
canvas.bind("<Button-1>", add_point)

# Start the Tkinter event loop
root.mainloop()
