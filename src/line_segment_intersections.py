import tkinter as tk
from tkinter import messagebox
import time
import numpy as np
import heapq
import sortedcontainers as sc

# Data classes for the event queue, points, and line segments (maybe move to a separate file)
from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class Event:
    x: float
    point: Any = field(compare=False)
    segments: Any = field(compare=False)
    # 'left', 'right', or 'intersection'
    event_type: str = field(compare=False)


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Segment:
    left: Point
    right: Point
    index: int  # To identify the segment
# ------------------------------------------------------------


# Create the main application window
root = tk.Tk()
root.title("Line Segment Intersections ")

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


# Function to reset the canvas and clear line segments
def reset_canvas():
    canvas.delete("all")
    points.clear()


# Reset button
reset_button = tk.Button(sidebar, text="Reset", command=reset_canvas)
reset_button.pack(pady=5)

# Create the canvas for drawing line segments
canvas = tk.Canvas(root, bg='white')
canvas.grid(row=0, column=1, sticky="nsew")


# store all line segments
line_segments = []
segment_index = 0  # To assign a unique index to each segment


# store all points
points = []


def add_point(event):
    global segment_index
    x, y = event.x, event.y
    radius = 4
    canvas.create_oval(x - radius, y - radius, x + radius,
                       y + radius, fill='black', tags="point")
    points.append(Point(x, y))
    if len(points) == 2:
        p1, p2 = points
        # Ensure left to right ordering
        if p1.x <= p2.x:
            left, right = p1, p2
        else:
            left, right = p2, p1
        segment = Segment(left, right, segment_index)
        segment_index += 1
        line_segments.append(segment)
        # Draw the line
        canvas.create_line(left.x, left.y, right.x,
                           right.y, fill='blue', tags="line_segment")
        points.clear()


# bind the mouse click event to the canvas
canvas.bind("<Button-1>", add_point)


event_queue = []


# initialize the event queue with left and right endpoints events (start and end events for all line segments)
def initialize_event_queue():
    for segment in line_segments:
        # Left endpoint event (start event)
        heapq.heappush(event_queue, Event(
            segment.left.x, segment.left, [segment], 'left'))
        # Right endpoint event (end event)
        heapq.heappush(event_queue, Event(
            segment.right.x, segment.right, [segment], 'right'))


# Start the Tkinter event loop
root.mainloop()
