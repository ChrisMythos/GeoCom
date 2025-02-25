"""
Bentley-Ottmann Sweep-Line Algorithm for Arbitrary Line Segment Intersections

This module implements a visualization of the Bentley-Ottmann sweep-line algorithm
for finding all intersections among arbitrary line segments in the 2D plane.
The algorithm efficiently finds all intersection points without checking every
possible pair of segments.
"""

import time
import tkinter as tk
import heapq
import random
from dataclasses import dataclass, field
from typing import Any, List, Optional, Set, Tuple, Union


@dataclass(order=True)
class Event:
    """
    Class representing an event in the sweep line algorithm.
    
    Events are ordered by x-coordinate and then by event type.
    """
    x: float                                  # X-coordinate of the event
    event_order: int                          # Event priority (start=0, intersection=1, end=2)
    point: Any = field(compare=False)         # Point where the event occurs
    event_type: str = field(compare=False)    # Type of the event ('start', 'end', 'intersection')
    segment: Any = field(compare=False, default=None)       # Associated segment (for start/end events)
    segment_up: Any = field(compare=False, default=None)    # Upper segment (for intersection events)
    segment_low: Any = field(compare=False, default=None)   # Lower segment (for intersection events)


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
    index: int                   # Unique index for the segment
    canvas_id: int = field(default=None, compare=False)  # Canvas ID for visualization

    def get_y_at_scanline(self, x: float) -> float:
        """
        Calculate the y-coordinate of the segment at the given x-coordinate.
        
        Args:
            x: The x-coordinate of the scan line
            
        Returns:
            The y-coordinate where the segment intersects the scan line
        """
        p1, p2 = self.start, self.end
        if p1.x == p2.x:
            # Vertical segment; return y-coordinate of the higher point (smaller y in canvas)
            return min(p1.y, p2.y)
        else:
            # Calculate y using the line equation
            m = (p2.y - p1.y) / (p2.x - p1.x)
            return m * (x - p1.x) + p1.y
        
    def slope(self) -> float:
        """
        Calculate the slope of the segment.
        
        Returns:
            The slope of the segment, or infinity for vertical segments
        """
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        if dx == 0:
            return float('inf')  # Vertical line
        else:
            return dy / dx


# AVL Tree Node Class
class AVLNode:
    """
    Node class for AVL Tree.
    
    Each node stores a segment and maintains the AVL tree properties.
    """
    def __init__(self, segment: Segment):
        self.segment = segment  # Line segment stored in this node
        self.height = 1         # Height of the node
        self.left = None        # Left child
        self.right = None       # Right child


# AVL Tree Class for SSS (Sweep-Line Status Structure)
class AVLTree:
    """
    AVL Tree implementation for the Sweep-Line Status Structure.
    
    This balanced binary search tree maintains the segments currently
    intersecting the sweep line, ordered by their y-coordinates.
    """
    def __init__(self):
        """Initialize an empty AVL tree."""
        self.root = None
        self.current_x = 0  # Current x-coordinate of the sweep line

    def set_current_x(self, x: float) -> None:
        """
        Set the current x-coordinate of the sweep line.
        
        Args:
            x: The x-coordinate of the sweep line
        """
        self.current_x = x

    def _height(self, node: Optional[AVLNode]) -> int:
        """
        Get height of a node.
        
        Args:
            node: The node to get the height of
            
        Returns:
            The height of the node, or 0 if the node is None
        """
        if not node:
            return 0
        return node.height

    def _update_height(self, node: AVLNode) -> None:
        """
        Update height of a node.
        
        Args:
            node: The node to update the height of
        """
        if node:
            node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node: Optional[AVLNode]) -> int:
        """
        Calculate the balance factor of a node.
        
        Args:
            node: The node to calculate the balance factor for
            
        Returns:
            The balance factor (left height - right height)
        """
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        """
        Perform a right rotation on the subtree rooted at y.
        
        Args:
            y: The root of the subtree to rotate
            
        Returns:
            The new root of the subtree after rotation
        """
        x = y.left
        T = x.right

        # Perform rotation
        x.right = y
        y.left = T

        # Update heights
        self._update_height(y)
        self._update_height(x)

        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        """
        Perform a left rotation on the subtree rooted at x.
        
        Args:
            x: The root of the subtree to rotate
            
        Returns:
            The new root of the subtree after rotation
        """
        y = x.right
        T = y.left

        # Perform rotation
        y.left = x
        x.right = T

        # Update heights
        self._update_height(x)
        self._update_height(y)

        return y

    def _balance(self, node: AVLNode) -> AVLNode:
        """
        Balance the subtree rooted at node.
        
        Args:
            node: The root of the subtree to balance
            
        Returns:
            The new root of the balanced subtree
        """
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

    def _compare(self, segment1: Segment, segment2: Segment) -> int:
        """
        Compare two segments based on their y-coordinate at the current scan-line.
        
        Args:
            segment1: The first segment
            segment2: The second segment
            
        Returns:
            -1 if segment1 is below segment2, 1 if segment1 is above segment2,
            or a comparison of their indices if they have the same y-coordinate
        """
        epsilon = 1e-9  # A small value to move slightly past the current x
        x = self.current_x + epsilon
        y1 = segment1.get_y_at_scanline(x)
        y2 = segment2.get_y_at_scanline(x)
        if abs(y1 - y2) < epsilon:
            # If y-coordinates are still equal, compare slopes to break the tie
            m1 = segment1.slope()
            m2 = segment2.slope()
            if abs(m1 - m2) < epsilon:
                return segment1.index - segment2.index
            elif m1 > m2:
                return 1
            else:
                return -1
        elif y1 < y2:
            return -1
        else:
            return 1

    def _insert(self, node: Optional[AVLNode], segment: Segment) -> AVLNode:
        """
        Insert a segment into the AVL tree.
        
        Args:
            node: The root of the subtree to insert into
            segment: The segment to insert
            
        Returns:
            The new root of the subtree after insertion
        """
        if not node:
            return AVLNode(segment)

        if self._compare(segment, node.segment) < 0:
            node.left = self._insert(node.left, segment)
        else:
            node.right = self._insert(node.right, segment)

        # Balance the tree
        return self._balance(node)

    def add_segment(self, segment: Segment) -> None:
        """
        Add a segment to the AVL tree.
        
        Args:
            segment: The segment to add
        """
        self.root = self._insert(self.root, segment)

    def _delete(self, node: Optional[AVLNode], segment: Segment) -> Optional[AVLNode]:
        """
        Delete a segment from the AVL tree.
        
        Args:
            node: The root of the subtree to delete from
            segment: The segment to delete
            
        Returns:
            The new root of the subtree after deletion
        """
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

    def remove_segment(self, segment: Segment) -> None:
        """
        Remove a segment from the AVL tree.
        
        Args:
            segment: The segment to remove
        """
        self.root = self._delete(self.root, segment)

    def _min_value_node(self, node: AVLNode) -> AVLNode:
        """
        Find the node with the minimum y-coordinate.
        
        Args:
            node: The root of the subtree to search
            
        Returns:
            The node with the minimum y-coordinate
        """
        current = node
        while current.left:
            current = current.left
        return current

    def _max_value_node(self, node: AVLNode) -> AVLNode:
        """
        Find the node with the maximum y-coordinate.
        
        Args:
            node: The root of the subtree to search
            
        Returns:
            The node with the maximum y-coordinate
        """
        current = node
        while current.right:
            current = current.right
        return current

    def _find_predecessor(self, node: Optional[AVLNode], segment: Segment, 
                          predecessor: Optional[Segment] = None) -> Optional[Segment]:
        """
        Find the predecessor of a segment in the AVL tree.
        
        Args:
            node: The current node in the search
            segment: The segment to find the predecessor of
            predecessor: The current best predecessor found
            
        Returns:
            The predecessor of the segment, or None if there is no predecessor
        """
        if not node:
            return predecessor
        
        cmp_result = self._compare(segment, node.segment)
        if cmp_result <= 0:
            return self._find_predecessor(node.left, segment, predecessor)
        else:
            return self._find_predecessor(node.right, segment, node.segment)

    def _find_successor(self, node: Optional[AVLNode], segment: Segment, 
                        successor: Optional[Segment] = None) -> Optional[Segment]:
        """
        Find the successor of a segment in the AVL tree.
        
        Args:
            node: The current node in the search
            segment: The segment to find the successor of
            successor: The current best successor found
            
        Returns:
            The successor of the segment, or None if there is no successor
        """
        if not node:
            return successor
        
        cmp_result = self._compare(segment, node.segment)
        if cmp_result >= 0:
            return self._find_successor(node.right, segment, successor)
        else:
            return self._find_successor(node.left, segment, node.segment)

    def predecessor(self, segment: Segment) -> Optional[Segment]:
        """
        Find the predecessor of a segment.
        
        Args:
            segment: The segment to find the predecessor of
            
        Returns:
            The predecessor of the segment, or None if there is no predecessor
        """
        return self._find_predecessor(self.root, segment)

    def successor(self, segment: Segment) -> Optional[Segment]:
        """
        Find the successor of a segment.
        
        Args:
            segment: The segment to find the successor of
            
        Returns:
            The successor of the segment, or None if there is no successor
        """
        return self._find_successor(self.root, segment)


class LineSegmentIntersectionVisualizer:
    """
    Class for visualizing the Bentley-Ottmann sweep-line algorithm for finding
    intersections among arbitrary line segments.
    """
    
    def __init__(self):
        """Initialize the visualizer with the main window and UI components."""
        # Create the main application window
        self.root = tk.Tk()
        self.root.title("Line Segment Intersections")
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
        self.segment_index = 0   # Unique index for each segment
        self.points = []         # Temporary list to store points when drawing segments
        self.event_queue = []    # Priority queue (min-heap) for events
        self.scan_line_id = None # Canvas item ID for the scan line
        self.current_x = 0       # Current x-coordinate of the scan line
        self.sss = AVLTree()     # Sweep-Line Status Structure (AVL Tree)
        self.processed_intersections = set()  # Set to track processed intersections
        self.intersection_count = 0  # Counter for intersections found
    
    def create_sidebar(self):
        """Create the sidebar with controls."""
        # Create a frame for the sidebar
        self.sidebar = tk.Frame(self.root, width=200, bg='lightgray', padx=10, pady=10)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        
        # Label for heading of the sidebar
        heading_text = tk.Label(
            self.sidebar, text="Line Segment Intersections", 
            font=("Arial", 20), bg='lightgray', fg='black')
        heading_text.pack(pady=5)
        
        # Delay Slider Label
        delay_label = tk.Label(
            self.sidebar, text="Visualization Delay (seconds):", 
            bg='lightgray', fg='black')
        delay_label.pack(pady=5)
        
        # Delay Slider
        self.delay_var = tk.DoubleVar(value=0.1)  # Default delay time
        self.delay_slider = tk.Scale(
            self.sidebar,
            from_=0.0,
            to=2.0,
            resolution=0.05,
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
        
        # Generate random segments button
        self.generate_button = tk.Button(
            self.sidebar, text="Generate Random Segments", command=self.generate_random_segments)
        self.generate_button.pack(pady=5)
    
    def add_point(self, event):
        """
        Handle mouse click event to add points and create segments.
        
        Args:
            event: The mouse click event
        """
        x, y = event.x, event.y
        # Draw a small circle to represent the point
        self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill='black', tags="point")
        self.points.append(Point(x, y))
        if len(self.points) == 2:
            # When two points are clicked, create a segment
            start, end = self.points
            segment = Segment(start, end, self.segment_index)
            self.segment_index += 1
            # Draw the line and store its canvas ID
            canvas_id = self.canvas.create_line(
                start.x, start.y, end.x, end.y, fill='black', tags="segment")
            segment.canvas_id = canvas_id
            self.segments.append(segment)
            self.points.clear()  # Reset points for the next segment
    
    def initialize_event_queue(self):
        """Initialize the event queue with start and end events for all segments."""
        self.event_queue.clear()
        for segment in self.segments:
            # Ensure left to right ordering of segment endpoints
            if segment.start.x > segment.end.x:
                segment.start, segment.end = segment.end, segment.start
            # Add start event with event_order = 0
            heapq.heappush(self.event_queue, Event(
                segment.start.x, 0, segment.start, event_type='start', segment=segment))
            # Add end event with event_order = 2
            heapq.heappush(self.event_queue, Event(
                segment.end.x, 2, segment.end, event_type='end', segment=segment))
    
    def process_events(self):
        """
        Process all events in the event queue.
        
        This is the main algorithm that finds all intersections among
        arbitrary line segments using a sweep-line approach.
        """
        # Reset intersection count
        self.intersection_count = 0
        self.update_intersection_label()
        
        # As long as there are events in the queue to process
        while self.event_queue:
            # Get the next event from the queue 
            event = heapq.heappop(self.event_queue)
            self.current_x = event.x
            
            # Update the current x-coordinate in the SSS
            self.sss.set_current_x(self.current_x)
            
            # Draw or update the scan line
            self.draw_scan_line(self.current_x)
            
            if event.event_type == 'start':
                self.handle_start_event(event)
            elif event.event_type == 'end':
                self.handle_end_event(event)
            elif event.event_type == 'intersection':
                self.handle_intersection_event(event)
            else:
                raise ValueError(f"Unknown event type: {event.event_type}")
            
            # Add a small delay for visualization
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
            x, 0, x, self.canvas.winfo_height(), fill='blue', dash=(4, 2), width=2)
    
    def handle_start_event(self, event: Event):
        """
        Handle start event: add segment to SSS and check for intersections.
        
        Args:
            event: The start event to handle
        """
        segment = event.segment
        
        # Add the segment to the SSS
        self.sss.add_segment(segment)
        
        # Change the color of the segment to green to indicate it's active 
        self.canvas.itemconfig(segment.canvas_id, fill='green')
        
        # Get predecessor and successor in SSS (segments above and below)
        pred_segment = self.sss.predecessor(segment)
        succ_segment = self.sss.successor(segment)
        
        # Check for intersections with neighboring segments
        if pred_segment:
            self.check_and_add_intersection(segment, pred_segment)
        if succ_segment:
            self.check_and_add_intersection(segment, succ_segment)
    
    def handle_end_event(self, event: Event):
        """
        Handle end event: remove segment from SSS and check for new intersections.
        
        Args:
            event: The end event to handle
        """
        segment = event.segment
        
        # Change the color of the segment back to black to indicate it's inactive
        self.canvas.itemconfig(segment.canvas_id, fill='black')
        
        # Get predecessor and successor in SSS before removing the segment
        pred_segment = self.sss.predecessor(segment)
        succ_segment = self.sss.successor(segment)
        
        # Remove the segment from SSS
        self.sss.remove_segment(segment)
        
        # If predecessor and successor exist, check for intersections between them
        if pred_segment and succ_segment:
            self.check_and_add_intersection(pred_segment, succ_segment)
    
    def handle_intersection_event(self, event: Event):
        """
        Handle intersection event: report intersection, swap segments, and check for new intersections.
        
        Args:
            event: The intersection event to handle
        """
        seg_up = event.segment_up
        seg_low = event.segment_low
        
        # Report intersection by drawing it
        self.draw_intersection_point(event.point)
        self.intersection_count += 1
        self.update_intersection_label()
        
        # Remove segments from AVL Tree
        self.sss.remove_segment(seg_up)
        self.sss.remove_segment(seg_low)
        
        # Swap the positions of the segments
        seg_up, seg_low = seg_low, seg_up
        
        # Re-insert segments into AVL Tree
        self.sss.add_segment(seg_up)
        self.sss.add_segment(seg_low)
        
        # Get new neighbors after swapping
        pred_segment = self.sss.predecessor(seg_low)
        succ_segment = self.sss.successor(seg_up)
        
        # Check if the segments have new intersections with neighbors 
        if pred_segment:
            self.check_and_add_intersection(seg_low, pred_segment)
        if succ_segment:
            self.check_and_add_intersection(seg_up, succ_segment)
    
    def check_and_add_intersection(self, s1: Segment, s2: Segment):
        """
        Check if two segments intersect and add an intersection event if they do.
        
        Args:
            s1: The first segment
            s2: The second segment
        """
        point = self.compute_intersection(s1, s2)
        if point and point.x >= self.current_x:
            # Create a unique key for the pair of segments
            segments_pair = tuple(sorted((s1.index, s2.index)))
            # Check if the intersection has already been processed to avoid duplicates
            if segments_pair not in self.processed_intersections:
                self.processed_intersections.add(segments_pair)
                # Create an intersection event and add it to the event queue
                event = Event(point.x, 1, point, event_type='intersection', segment_up=s1, segment_low=s2)
                heapq.heappush(self.event_queue, event)
    
    def compute_intersection(self, s1: Segment, s2: Segment) -> Optional[Point]:
        """
        Compute the intersection point between two segments, if it exists.
        
        Args:
            s1: The first segment
            s2: The second segment
            
        Returns:
            The intersection point, or None if the segments don't intersect
        """
        # Get the endpoints of the segments
        p1, p2 = s1.start, s1.end
        p3, p4 = s2.start, s2.end
        
        # Compute the determinant
        m = (p1.x - p2.x)*(p3.y - p4.y) - (p1.y - p2.y)*(p3.x - p4.x)
        epsilon = 1e-9  # Small value for floating-point comparison
        if abs(m) < epsilon:
            # Lines are parallel or coincident
            return None
        
        # Compute numerators 
        num_x = (p1.x*p2.y - p1.y*p2.x)*(p3.x - p4.x) - (p1.x - p2.x)*(p3.x*p4.y - p3.y*p4.x)
        num_y = (p1.x*p2.y - p1.y*p2.x)*(p3.y - p4.y) - (p1.y - p2.y)*(p3.x*p4.y - p3.y*p4.x)
        
        # Calculate intersection point
        x = num_x / m
        y = num_y / m
        
        # Check if the intersection point is within both segments
        if (min(p1.x, p2.x) - epsilon <= x <= max(p1.x, p2.x) + epsilon and
            min(p3.x, p4.x) - epsilon <= x <= max(p3.x, p4.x) + epsilon and
            min(p1.y, p2.y) - epsilon <= y <= max(p1.y, p2.y) + epsilon and
            min(p3.y, p4.y) - epsilon <= y <= max(p3.y, p4.y) + epsilon):
            return Point(x, y)
        else:
            return None
    
    def draw_intersection_point(self, point: Point):
        """
        Draw a red circle to represent an intersection point.
        
        Args:
            point: The intersection point
        """
        x, y = point.x, point.y
        self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill='red', tags="intersection")
    
    def update_intersection_label(self):
        """Update the intersection count label."""
        self.intersection_label.config(text=f"Intersections: {self.intersection_count}")
    
    def reset_canvas(self):
        """Clear the canvas and reset all data structures."""
        self.canvas.delete("all")
        self.points.clear()
        self.segments.clear()
        self.event_queue.clear()
        self.sss = AVLTree()  # Reset the AVL Tree
        self.segment_index = 0
        self.scan_line_id = None
        self.processed_intersections.clear()
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
        
        self.canvas.update_idletasks()  # Ensure the canvas has the correct size
        self.initialize_event_queue()
        self.process_events()
        
        # Re-enable the canvas and buttons after computation
        self.canvas.bind("<Button-1>", self.add_point)
        self.compute_button.config(state='normal')
        self.reset_button.config(state='normal')
        self.delay_slider.config(state='normal')
        self.generate_button.config(state='normal')
    
    def generate_random_segments(self):
        """Generate random line segments."""
        self.reset_canvas()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Ensure the canvas has a valid size
        if width <= 1 or height <= 1:
            width, height = 800, 600
        
        # Generate random segments
        for _ in range(10):
            x1 = random.uniform(50, width - 50)
            y1 = random.uniform(50, height - 50)
            x2 = random.uniform(50, width - 50)
            y2 = random.uniform(50, height - 50)
            
            start = Point(x1, y1)
            end = Point(x2, y2)
            
            segment = Segment(start, end, self.segment_index)
            self.segment_index += 1
            
            canvas_id = self.canvas.create_line(
                start.x, start.y, end.x, end.y, fill='black', tags="segment")
            segment.canvas_id = canvas_id
            
            self.segments.append(segment)
        
        self.canvas.update()
    
    def run(self):
        """Start the Tkinter event loop."""
        self.root.mainloop()


# Main entry point
if __name__ == "__main__":
    visualizer = LineSegmentIntersectionVisualizer()
    visualizer.run()
