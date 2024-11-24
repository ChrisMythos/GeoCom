import tkinter as tk
import heapq
import random
from dataclasses import dataclass, field
from typing import Any

# Create the main application window
root = tk.Tk()
root.title("Axis-Aligned Line Intersections")

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
scan_line_id = None # Canvas item ID for the scan line
current_x = 0       # Current x-coordinate of the scan line
intersection_count = 0  # Counter for intersections found

@dataclass(order=True)
class Event:
    """Class representing an event in the sweep line algorithm."""
    x: float                              # X-coordinate of the event
    event_order: int                      # Event priority for ordering (start=0, vertical=1, end=2)
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
        canvas_id = canvas.create_line(x_coord, y1, x_coord, y2, fill='blue', width=2)
        segment = Segment(Point(x_coord, min(y1, y2)), Point(x_coord, max(y1, y2)), 'vertical', canvas_id)
    else:
        # Horizontal segment
        y_coord = start.y
        x1, x2 = start.x, end.x
        canvas_id = canvas.create_line(x1, y_coord, x2, y_coord, fill='blue', width=2)
        segment = Segment(Point(min(x1, x2), y_coord), Point(max(x1, x2), y_coord), 'horizontal', canvas_id)
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
    global scan_line_id, current_x, intersection_count, L

    L = AVLTree()

    def process_next_event():
        global scan_line_id, current_x, intersection_count

        if not event_queue:
            # Remove the scan line after processing is complete
            if scan_line_id is not None:
                canvas.delete(scan_line_id)
            # Display the total number of intersections found
            display_intersection_count()
            # Re-enable the canvas and buttons after computation
            canvas.bind("<Button-1>", add_point)
            compute_button.config(state='normal')
            reset_button.config(state='normal')
            delay_slider.config(state='normal')
            generate_button.config(state='normal')
            return

        event = heapq.heappop(event_queue)
        current_x = event.x

        # Draw or update the scan line
        draw_scan_line(current_x)

        segment = event.segment

        if event.event_order == 0:
            # Left endpoint of horizontal segment
            # Insert segment into L
            L.insert(segment.start.y, segment)
            # Change the color to indicate active segment
            canvas.itemconfig(segment.canvas_id, fill='green')
        elif event.event_order == 2:
            # Right endpoint of horizontal segment
            # Remove segment from L
            L.delete(segment.start.y, segment)
            # Change the color to indicate inactive segment
            canvas.itemconfig(segment.canvas_id, fill='black')
        elif event.event_order == 1:
            # Vertical segment
            y_l = min(segment.start.y, segment.end.y)
            y_u = max(segment.start.y, segment.end.y)
            # Find the starting node with smallest key ≥ y_l
            node = L.find_min_greater_equal(y_l)
            # Traverse successor links to collect all segments in the range
            while node and node.key <= y_u:
                h_segment = node.segment
                # Report intersection
                draw_intersection_point(Point(segment.start.x, h_segment.start.y))
                intersection_count += 1  # Increment intersection count
                node = node.successor
            # Change the color to indicate processed vertical segment
            canvas.itemconfig(segment.canvas_id, fill='black')
        else:
            raise ValueError(f"Unknown event order: {event.event_order}")

        # Update the canvas
        canvas.update()

        # Schedule the next event after a delay
        delay_ms = int(delay_var.get() * 1000)  # Convert seconds to milliseconds
        root.after(delay_ms, process_next_event)

    # Start processing events
    process_next_event()

def draw_scan_line(x):
    """Draw the vertical scan line at position x."""
    global scan_line_id
    # Remove the previous scan line if it exists
    if scan_line_id is not None:
        canvas.delete(scan_line_id)
    # Draw the new scan line
    scan_line_id = canvas.create_line(x, 0, x, canvas.winfo_height(), fill='red', dash=(4, 2), width=2)

def draw_intersection_point(point):
    """Draw a red circle to represent an intersection point."""
    x, y = point.x, point.y
    canvas.create_oval(x - 3, y - 3, x + 3, y + 3, outline='red', width=2, tags="intersection")

def display_intersection_count():
    """Display the total number of intersections found."""
    message = f"Total Intersections: {intersection_count}"
    canvas.create_text(10, 10, anchor='nw', text=message, font=('Arial', 16), fill='black', tags="count")

# AVL Tree Node Class with successor links
class AVLNode:
    def __init__(self, key, segment):
        self.key = key  # y-coordinate
        self.segment = segment  # Horizontal segment
        self.left = None
        self.right = None
        self.parent = None
        self.height = 1  # For AVL balancing
        self.successor = None  # Successor in in-order traversa

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key, segment):
        # Insert node and update successor links
        self.root = self._insert(self.root, key, segment, None)

    def _insert(self, node, key, segment, parent):
        if node is None:
            # Create new node
            new_node = AVLNode(key, segment)
            new_node.parent = parent
            # Update successor links
            self._update_successor_insert(new_node)
            return new_node
        elif key < node.key:
            node.left = self._insert(node.left, key, segment, node)
        else:
            node.right = self._insert(node.right, key, segment, node)
        # Update height and balance
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        # Rebalance and update parent
        new_node = self._rebalance(node)
        return new_node

    def _update_successor_insert(self, node):
        # Update successor pointers after insertion
        # Find successor
        successor = self._find_successor_for_insert(node)
        node.successor = successor
        # Update predecessor's successor if necessary
        predecessor = self._find_predecessor_for_insert(node)
        if predecessor:
            predecessor.successor = node

    def delete(self, key, segment):
        # Delete node and update successor links
        self.root = self._delete(self.root, key, segment)

    def _delete(self, node, key, segment):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key, segment)
        elif key > node.key:
            node.right = self._delete(node.right, key, segment)
        else:
            if node.segment != segment:
                # There may be multiple segments with the same y-coordinate
                # Continue searching in the right subtree
                node.right = self._delete(node.right, key, segment)
            else:
                # Node to be deleted found
                # Update successor links
                predecessor = self._find_predecessor_for_delete(node)
                successor = self._find_successor_for_delete(node)
                if predecessor:
                    predecessor.successor = successor
                # Delete node
                if node.left is None:
                    temp = node.right
                    if temp:
                        temp.parent = node.parent
                    node = None
                    return temp
                elif node.right is None:
                    temp = node.left
                    if temp:
                        temp.parent = node.parent
                    node = None
                    return temp
                else:
                    # Node with two children
                    temp = self._get_min_value_node(node.right)
                    node.key = temp.key
                    node.segment = temp.segment
                    node.right = self._delete(node.right, temp.key, temp.segment)
        # Update height and balance
        if node is None:
            return node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        # Rebalance and update parent
        new_node = self._rebalance(node)
        return new_node

    def find_min_greater_equal(self, y):
        # Find node with smallest key ≥ y
        node = self.root
        result = None
        while node:
            if y == node.key:
                result = node
                break
            elif y < node.key:
                result = node
                node = node.left
            else:
                node = node.right
        return result

    def _find_successor_for_insert(self, node):
        # Find successor after insertion
        current = node
        if current.right:
            return self._get_min_value_node(current.right)
        else:
            parent = current.parent
            while parent and current == parent.right:
                current = parent
                parent = parent.parent
            return parent

    def _find_predecessor_for_insert(self, node):
        # Find predecessor after insertion
        current = node
        if current.left:
            return self._get_max_value_node(current.left)
        else:
            parent = current.parent
            while parent and current == parent.left:
                current = parent
                parent = parent.parent
            return parent

    def _find_successor_for_delete(self, node):
        # Find successor before deletion
        if node.successor:
            return node.successor
        else:
            current = node
            parent = current.parent
            while parent and current == parent.right:
                current = parent
                parent = parent.parent
            return parent

    def _find_predecessor_for_delete(self, node):
        # Find predecessor before deletion
        current = node
        if current.left:
            return self._get_max_value_node(current.left)
        else:
            parent = current.parent
            while parent and current == parent.left:
                current = parent
                parent = parent.parent
            return parent

    def _get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def _get_max_value_node(self, node):
        current = node
        while current.right:
            current = current.right
        return current

    def _get_height(self, node):
        return node.height if node else 0

    def _get_balance(self, node):
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    def _rebalance(self, node):
        balance = self._get_balance(node)
        # Left heavy
        if balance > 1:
            if self._get_balance(node.left) < 0:
                # Left-Right case
                node.left = self._rotate_left(node.left)
            # Left-Left case
            return self._rotate_right(node)
        # Right heavy
        if balance < -1:
            if self._get_balance(node.right) > 0:
                # Right-Left case
                node.right = self._rotate_right(node.right)
            # Right-Right case
            return self._rotate_left(node)
        return node

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left
        # Perform rotation
        y.left = z
        z.right = T2
        # Update parents
        y.parent = z.parent
        z.parent = y
        if T2:
            T2.parent = z
        # Update heights
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        # Update successor pointers
        y.successor = z.successor
        z.successor = y.left  # z's successor is now T2 or None
        return y

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right
        # Perform rotation
        y.right = z
        z.left = T3
        # Update parents
        y.parent = z.parent
        z.parent = y
        if T3:
            T3.parent = z
        # Update heights
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        # Update successor pointers
        y.successor = z
        z.successor = T3  # z's successor is now T3 or None
        return y

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

compute_button = tk.Button(sidebar, text="Compute Intersections", command=start_computing)
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

generate_button = tk.Button(sidebar, text="Generate Lines", command=generate_lines)
generate_button.pack(pady=5)

# Bind the mouse click event to the canvas
canvas.bind("<Button-1>", add_point)

# Start the Tkinter event loop
root.mainloop()