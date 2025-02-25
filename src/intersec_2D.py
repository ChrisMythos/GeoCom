"""
Sweep-Line Algorithm for Axis-Aligned Line Segment Intersections

This module implements a sweep-line algorithm for finding all intersections
among axis-aligned (horizontal and vertical) line segments. The implementation
uses a sorted list with binary search for efficient range queries.

The visualization allows users to:
1. Draw segments manually by clicking on the canvas
2. Generate random segments
3. Visualize the sweep-line algorithm in action
4. Adjust the visualization speed
"""

import time
import tkinter as tk
import heapq
import random
import bisect
from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional


@dataclass(order=True)
class Event:
    """
    Class representing an event in the sweep-line algorithm.
    
    Events are ordered by x-coordinate and then by event type.
    """
    x: float                              # X-coordinate of the event
    event_order: int                      # Event priority (start=0, vertical=1, end=2)
    segment: Any = field(compare=False)   # Associated segment


@dataclass
class Point:
    """
    Class representing a point with x and y coordinates.
    """
    x: float
    y: float


@dataclass
class Segment:
    """
    Class representing a line segment with a start and end point.
    """
    start: Point
    end: Point
    orientation: str             # 'horizontal' or 'vertical'
    canvas_id: int               # Canvas ID for visualization


class SweepLineVisualizer:
    """
    Class for visualizing the sweep-line algorithm for finding intersections
    among axis-aligned line segments.
    """
    
    def __init__(self):
        """Initialize the visualizer with the main window and UI components."""
        # Create the main application window
        self.root = tk.Tk()
        self.root.title("Axis-Aligned Line Segment Intersections")
        self.root.geometry("1000x800")
        
        # Configure the grid layout
        self.root.grid_columnconfigure(0, weight=0)  # Sidebar column does not expand
        self.root.grid_columnconfigure(1, weight=1)  # Canvas column expands
        self.root.grid_rowconfigure(0, weight=1)     # Row expands vertically
        
        # Create sidebar
        self.create_sidebar()
        
        # Create canvas
        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.grid(row=0, column=1, sticky="nsew")
        self.canvas.bind("<Button-1>", self.add_point)
        
        # Initialize data structures
        self.segments = []       # List to store all segments
        self.points = []         # Temporary list to store points when drawing segments
        self.event_queue = []    # Priority queue (min-heap) for events
        self.scan_line_id = None # Canvas item ID for the scan line
        self.current_x = 0       # Current x-coordinate of the scan line
        self.intersection_count = 0  # Counter for intersections found
    
    def create_sidebar(self):
        """Create the sidebar with controls."""
        # Create a frame for the sidebar
        self.sidebar = tk.Frame(self.root, width=200, bg='lightgray', padx=10, pady=10)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        
        # Label for heading of the sidebar
        heading_text = tk.Label(
            self.sidebar, text="Axis-Aligned Line Intersections", 
            font=("Arial", 18), bg='lightgray', fg='black')
        heading_text.pack(pady=5)
        
        # Delay Slider Label
        delay_label = tk.Label(
            self.sidebar, text="Visualization Delay (seconds):", 
            bg='lightgray', fg='black')
        delay_label.pack(pady=5)
        
        # Delay Slider
        self.delay_var = tk.DoubleVar(value=0.05)  # Default delay time
        self.delay_slider = tk.Scale(
            self.sidebar,
            from_=0.0,
            to=1.0,
            resolution=0.01,
            orient='horizontal',
            variable=self.delay_var
        )
        self.delay_slider.pack()
        
        # Intersection count label
        self.intersection_label = tk.Label(
            self.sidebar, text="Intersections: 0", 
            bg='lightgray', fg='black', font=("Arial", 12))
        self.intersection_label.pack(pady=10)
        
        # Reset button
        self.reset_button = tk.Button(
            self.sidebar, text="Reset", command=self.reset_canvas)
        self.reset_button.pack(pady=5)
        
        # Compute button
        self.compute_button = tk.Button(
            self.sidebar, text="Compute Intersections", command=self.start_computing)
        self.compute_button.pack(pady=5)
        
        # Generate lines button
        self.generate_button = tk.Button(
            self.sidebar, text="Generate Lines", command=self.generate_lines)
        self.generate_button.pack(pady=5)
    
    def add_point(self, event):
        """
        Handle mouse click event to add points and create segments.
        
        Args:
            event: The mouse click event
        """
        x, y = event.x, event.y
        # Draw a small circle to represent the point
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='black', tags="point")
        self.points.append(Point(x, y))
        if len(self.points) == 2:
            # When two points are clicked, create a segment
            start, end = self.points
            self.add_segment(start, end)
            self.points.clear()  # Reset points for the next segment
    
    def add_segment(self, start: Point, end: Point):
        """
        Add a segment to the canvas and segments list.
        
        Args:
            start: The start point of the segment
            end: The end point of the segment
        """
        if abs(start.x - end.x) < abs(start.y - end.y):
            # Vertical segment
            x_coord = start.x
            y1, y2 = start.y, end.y
            canvas_id = self.canvas.create_line(
                x_coord, y1, x_coord, y2, fill='blue', width=2)
            segment = Segment(
                Point(x_coord, min(y1, y2)), 
                Point(x_coord, max(y1, y2)), 
                'vertical', canvas_id)
        else:
            # Horizontal segment
            y_coord = start.y
            x1, x2 = start.x, end.x
            canvas_id = self.canvas.create_line(
                x1, y_coord, x2, y_coord, fill='blue', width=2)
            segment = Segment(
                Point(min(x1, x2), y_coord), 
                Point(max(x1, x2), y_coord), 
                'horizontal', canvas_id)
        self.segments.append(segment)
    
    def initialize_event_queue(self):
        """Initialize the event queue with all events sorted by x-coordinate."""
        self.event_queue.clear()
        for segment in self.segments:
            if segment.orientation == 'horizontal':
                # Add start and end events for horizontal segments
                heapq.heappush(self.event_queue, Event(segment.start.x, 0, segment))
                heapq.heappush(self.event_queue, Event(segment.end.x, 2, segment))
            else:
                # Add vertical segment event
                heapq.heappush(self.event_queue, Event(segment.start.x, 1, segment))
    
    def process_events(self):
        """
        Process all events in the event queue.
        
        This is the main algorithm that finds all intersections among
        axis-aligned line segments using a sweep-line approach.
        """
        # Reset intersection count
        self.intersection_count = 0
        self.update_intersection_label()
        
        # List of active horizontal segments, sorted by y-coordinate
        L = []  
        
        while self.event_queue:
            event = heapq.heappop(self.event_queue)
            self.current_x = event.x
            
            # Draw or update the scan line
            self.draw_scan_line(self.current_x)
            
            segment = event.segment
            
            if event.event_order == 0:
                # Left endpoint of horizontal segment
                # Insert segment into L, maintaining order by y-coordinate
                bisect.insort_left(L, (segment.start.y, segment))
                # Change the color to indicate active segment
                self.canvas.itemconfig(segment.canvas_id, fill='green')
            elif event.event_order == 2:
                # Right endpoint of horizontal segment
                # Remove segment from L
                idx = bisect.bisect_left(L, (segment.start.y, segment))
                if idx < len(L) and L[idx][1] == segment:
                    L.pop(idx)
                # Change the color to indicate inactive segment
                self.canvas.itemconfig(segment.canvas_id, fill='black')
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
                    self.draw_intersection_point(Point(segment.start.x, h_segment.start.y))
                    self.intersection_count += 1
                    self.update_intersection_label()
                    idx += 1
                # Change the color to indicate processed vertical segment
                self.canvas.itemconfig(segment.canvas_id, fill='black')
            else:
                raise ValueError(f"Unknown event order: {event.event_order}")
            
            # Update the canvas and add delay
            self.canvas.update()
            time.sleep(self.delay_var.get())
        
        # Remove the scan line after processing is complete
        if self.scan_line_id is not None:
            self.canvas.delete(self.scan_line_id)
    
    def draw_scan_line(self, x: float):
        """
        Draw the vertical scan line at position x.
        
        Args:
            x: The x-coordinate of the scan line
        """
        # Remove the previous scan line if it exists
        if self.scan_line_id is not None:
            self.canvas.delete(self.scan_line_id)
        # Draw the new scan line
        self.scan_line_id = self.canvas.create_line(
            x, 0, x, self.canvas.winfo_height(), 
            fill='red', dash=(4, 2), width=2)
    
    def draw_intersection_point(self, point: Point):
        """
        Draw a red circle to represent an intersection point.
        
        Args:
            point: The intersection point
        """
        x, y = point.x, point.y
        self.canvas.create_oval(
            x - 3, y - 3, x + 3, y + 3, 
            outline='red', width=2, tags="intersection")
    
    def update_intersection_label(self):
        """Update the intersection count label."""
        self.intersection_label.config(text=f"Intersections: {self.intersection_count}")
    
    def reset_canvas(self):
        """Clear the canvas and reset all data structures."""
        self.canvas.delete("all")
        self.points.clear()
        self.segments.clear()
        self.event_queue.clear()
        self.scan_line_id = None  # Reset the scan line ID
        self.intersection_count = 0
        self.update_intersection_label()
    
    def start_computing(self):
        """Initialize the event queue and start processing events."""
        # Disable the canvas and buttons during computation
        self.canvas.unbind("<Button-1>")
        self.compute_button.config(state='disabled')
        self.reset_button.config(state='disabled')
        self.delay_slider.config(state='disabled')
        self.generate_button.config(state='disabled')
        
        self.initialize_event_queue()
        self.process_events()
        
        # Re-enable the canvas and buttons after computation
        self.canvas.bind("<Button-1>", self.add_point)
        self.compute_button.config(state='normal')
        self.reset_button.config(state='normal')
        self.delay_slider.config(state='normal')
        self.generate_button.config(state='normal')
    
    def generate_lines(self):
        """Generate random horizontal and vertical segments."""
        self.reset_canvas()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
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
            self.add_segment(start, end)
        self.canvas.update()
    
    def run(self):
        """Start the Tkinter event loop."""
        self.root.mainloop()


# Main entry point
if __name__ == "__main__":
    visualizer = SweepLineVisualizer()
    visualizer.run()
