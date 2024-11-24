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
scan_line_id = None # Canvas item ID for the scan line
current_x = 0       # Current x-coordinate of the scan line

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
    global scan_line_id, current_x
    import bisect
    L = []  # List of active horizontal segments, sorted by y-coordinate

    while event_queue:
        event = heapq.heappop(event_queue)
        current_x = event.x

        # Draw or update the scan line
        draw_scan_line(current_x)

        segment = event.segment

        if event.event_order == 0:
            # Left endpoint of horizontal segment
            # Insert segment into L, maintaining order by y-coordinate
            bisect.insort_left(L, (segment.start.y, segment))
            # Change the color to indicate active segment
            canvas.itemconfig(segment.canvas_id, fill='green')
        elif event.event_order == 2:
            # Right endpoint of horizontal segment
            # Remove segment from L
            idx = bisect.bisect_left(L, (segment.start.y, segment))
            if idx < len(L) and L[idx][1] == segment:
                L.pop(idx)
            # Change the color to indicate inactive segment
            canvas.itemconfig(segment.canvas_id, fill='black')
        elif event.event_order == 1:
            # Vertical segment
            # Determine all horizontal segments t in L whose y-coordinate t.y is in [y_l, y_u]
            y_l = min(segment.start.y, segment.end.y)
            y_u = max(segment.start.y, segment.end.y)
            # Find the starting index using bisect
            start_idx = bisect.bisect_left(L, (y_l, ))
            # Collect all segments within the y-range
            idx = start_idx
            while idx < len(L) and L[idx][0] <= y_u:
                h_segment = L[idx][1]
                # Report intersection
                draw_intersection_point(Point(segment.start.x, h_segment.start.y))
                idx += 1
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
    scan_line_id = canvas.create_line(x, 0, x, canvas.winfo_height(), fill='red', dash=(4, 2), width=2)

def draw_intersection_point(point):
    """Draw a red circle to represent an intersection point."""
    x, y = point.x, point.y
    canvas.create_oval(x - 3, y - 3, x + 3, y + 3, outline='red', width=2, tags="intersection")

# Buttons and Controls

def reset_canvas():
    """Clear the canvas and reset all data structures."""
    global segments, points, event_queue, scan_line_id
    canvas.delete("all")
    points.clear()
    segments.clear()
    event_queue.clear()
    scan_line_id = None  # Reset the scan line ID

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
