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
delay_var = tk.DoubleVar(value=0.2)  # Default delay time
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
    global segment_index
    canvas.delete("all")
    points.clear()
    segments.clear()
    event_queue.clear()
    sss.clear()
    segment_index = 0


reset_button = tk.Button(sidebar, text="Reset", command=reset_canvas)
reset_button.pack(pady=5)

# Compute Intersections button


def start_computing():
    initialize_event_queue()
    process_events()


compute_button = tk.Button(
    sidebar, text="Compute Intersections", command=start_computing)
compute_button.pack(pady=5)

# Create the canvas for drawing line segments
canvas = tk.Canvas(root, bg='white')
canvas.grid(row=0, column=1, sticky="nsew")

# Store the segments and points
segments = []
segment_index = 0
points = []

# Event queue and SSS
event_queue = []
current_x = 0  # Global variable to keep track of the scan line position
sss = []


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Segment:
    start: Point
    end: Point
    index: int


@dataclass(order=True)
class Event:
    x: float
    event_type: str
    point: Point
    segment: Any = field(compare=False, default=None)
    segment_up: Any = field(compare=False, default=None)
    segment_low: Any = field(compare=False, default=None)


def add_point(event):
    global segment_index
    x, y = event.x, event.y
    canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill='black', tags="point")
    points.append(Point(x, y))
    if len(points) == 2:
        start, end = points
        segment = Segment(start, end, segment_index)
        segment_index += 1
        segments.append(segment)
        # Draw the line
        canvas.create_line(start.x, start.y, end.x, end.y,
                           fill='black', tags="segment")
        points.clear()


def initialize_event_queue():
    event_queue.clear()
    for segment in segments:
        # Ensure left to right ordering
        if segment.start.x > segment.end.x:
            segment.start, segment.end = segment.end, segment.start
        # Add start event
        heapq.heappush(event_queue, Event(segment.start.x,
                       'start', segment.start, segment=segment))
        # Add end event
        heapq.heappush(event_queue, Event(
            segment.end.x, 'end', segment.end, segment=segment))


def process_events():
    global current_x
    intersections = []
    while event_queue:
        event = heapq.heappop(event_queue)
        current_x = event.x

        # Re-sort SSS based on current_x
        sss.sort(key=lambda s: get_segment_y_at_x(s, current_x))

        if event.event_type == 'start':
            handle_start_event(event, intersections)
        elif event.event_type == 'end':
            handle_end_event(event, intersections)
        elif event.event_type == 'intersection':
            handle_intersection_event(event, intersections)
        else:
            raise ValueError(f"Unknown event type: {event.event_type}")
    return intersections


def handle_start_event(event, intersections):
    segment = event.segment
    sss.append(segment)
    sss.sort(key=lambda s: get_segment_y_at_x(s, current_x))
    idx = sss.index(segment)

    pred_segment = sss[idx - 1] if idx > 0 else None
    succ_segment = sss[idx + 1] if idx + 1 < len(sss) else None

    if pred_segment:
        check_and_add_intersection(segment, pred_segment)
    if succ_segment:
        check_and_add_intersection(segment, succ_segment)


def handle_end_event(event, intersections):
    segment = event.segment
    idx = sss.index(segment)

    pred_segment = sss[idx - 1] if idx > 0 else None
    succ_segment = sss[idx + 1] if idx + 1 < len(sss) else None

    sss.remove(segment)

    if pred_segment and succ_segment:
        check_and_add_intersection(pred_segment, succ_segment)


def handle_intersection_event(event, intersections):
    seg_up = event.segment_up
    seg_low = event.segment_low

    # Report intersection
    intersections.append(event.point)
    draw_intersection_point(event.point)

    # Swap segments in SSS
    idx_up = sss.index(seg_up)
    idx_low = sss.index(seg_low)

    sss[idx_up], sss[idx_low] = sss[idx_low], sss[idx_up]

    # Re-sort SSS after swapping
    sss.sort(key=lambda s: get_segment_y_at_x(s, current_x))

    # Update indices after sorting
    idx_up = sss.index(seg_up)
    idx_low = sss.index(seg_low)

    idx_up, idx_low = min(idx_up, idx_low), max(idx_up, idx_low)

    pred_segment = sss[idx_up - 1] if idx_up > 0 else None
    succ_segment = sss[idx_low + 1] if idx_low + 1 < len(sss) else None

    if pred_segment:
        check_and_add_intersection(seg_up, pred_segment)
    if succ_segment:
        check_and_add_intersection(seg_low, succ_segment)


def check_and_add_intersection(s1, s2):
    point = compute_intersection(s1, s2)
    if point and point.x >= current_x:
        event = Event(point.x, 'intersection', point,
                      segment_up=s1, segment_low=s2)
        # Avoid adding duplicate events
        if event not in event_queue:
            heapq.heappush(event_queue, event)


def compute_intersection(s1, s2):
    p1, p2 = s1.start, s1.end
    p3, p4 = s2.start, s2.end

    denom = (p1.x - p2.x)*(p3.y - p4.y) - (p1.y - p2.y)*(p3.x - p4.x)
    if denom == 0:
        return None

    num_x = (p1.x*p2.y - p1.y*p2.x)*(p3.x - p4.x) - \
        (p1.x - p2.x)*(p3.x*p4.y - p3.y*p4.x)
    num_y = (p1.x*p2.y - p1.y*p2.x)*(p3.y - p4.y) - \
        (p1.y - p2.y)*(p3.x*p4.y - p3.y*p4.x)

    x = num_x / denom
    y = num_y / denom

    if (min(p1.x, p2.x) - 1e-6 <= x <= max(p1.x, p2.x) + 1e-6 and
        min(p3.x, p4.x) - 1e-6 <= x <= max(p3.x, p4.x) + 1e-6 and
        min(p1.y, p2.y) - 1e-6 <= y <= max(p1.y, p2.y) + 1e-6 and
            min(p3.y, p4.y) - 1e-6 <= y <= max(p3.y, p4.y) + 1e-6):
        return Point(x, y)
    else:
        return None


def get_segment_y_at_x(segment, x):
    p1, p2 = segment.start, segment.end
    if p1.x == p2.x:
        return p1.y
    else:
        m = (p2.y - p1.y) / (p2.x - p1.x)
        return m * (x - p1.x) + p1.y


def draw_intersection_point(point):
    x, y = point.x, point.y
    canvas.create_oval(x - 4, y - 4, x + 4, y + 4,
                       fill='red', tags="intersection")
    canvas.update()
    time.sleep(delay_var.get())


# Bind the mouse click event to the canvas
canvas.bind("<Button-1>", add_point)

# Start the Tkinter event loop
root.mainloop()
