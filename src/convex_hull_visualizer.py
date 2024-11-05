import tkinter as tk
from tkinter import messagebox
import time
import numpy as np

# Create the main application window
root = tk.Tk()
root.title("Convex Hull Visualizer")

# Set the window size
root.geometry("1000x800")

# Configure the grid layout (2 columns, 1 row)
root.grid_columnconfigure(0, weight=0)  # Sidebar column does not expand
root.grid_columnconfigure(1, weight=1)  # Canvas column expands
root.grid_rowconfigure(0, weight=1)     # Row expands vertically

# Create a frame for the sidebar
sidebar = tk.Frame(root, width=200, bg='lightgray', padx=10, pady=10)
sidebar.grid(row=0, column=0, sticky="ns")

# Label for algorithm selection
algorithm_label = tk.Label(sidebar, text="Select Algorithm:")
algorithm_label.pack(pady=5)

# Variable to store the selected algorithm
selected_algorithm = tk.StringVar(value="Graham Scan")

# List of available algorithms
algorithms = ["Graham Scan", "Jarvis' March"]

# Create radio buttons for algorithm selection
for algo in algorithms:
    rb = tk.Radiobutton(
        sidebar,
        text=algo,
        variable=selected_algorithm,
        value=algo
    )
    rb.pack(anchor='w')

# Delay Slider Label
delay_label = tk.Label(sidebar, text="Visualization Delay (seconds):")
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


# Function to call the selected algorithm to compute the convex hull
def compute_convex_hull():
    # Check if there are enough points to compute the convex hull
    if len(points) < 3:
        messagebox.showerror(
            "Error", "At least 3 points are required to compute a convex hull.")
        return
    # Get the selected algorithm from the radio buttons
    algo = selected_algorithm.get()
    if algo == "Graham Scan":
        graham_scan(points)
    elif algo == "Jarvis' March":
        jarvis_march(points)


# Compute button (now with the command bound)
compute_button = tk.Button(
    sidebar, text="Compute Convex Hull", command=compute_convex_hull)
compute_button.pack(pady=20)


# Function to reset the canvas and clear points
def reset_canvas():
    canvas.delete("all")
    points.clear()


# Reset button
reset_button = tk.Button(sidebar, text="Reset", command=reset_canvas)
reset_button.pack(pady=5)

# Create the canvas for drawing points
canvas = tk.Canvas(root, bg='white')
canvas.grid(row=0, column=1, sticky="nsew")

# List to store the point coordinates
points = []


# Function to handle mouse clicks on the canvas
def add_point(event):
    x, y = event.x, event.y
    radius = 3
    canvas.create_oval(x - radius, y - radius, x + radius,
                       y + radius, fill='black', tags="point")
    points.append((x, y))


# Bind the left mouse button click event to the canvas
canvas.bind("<Button-1>", add_point)


# Function to calculate the cross product (ccw test) of three points p1, p2, p3 using NumPy
def ccwNP(p1, p2, p3):
    return np.cross(np.array(p2) - np.array(p1), np.array(p3) - np.array(p1))


# Function to calculate the cross product (ccw test) of three points p1, p2, p3 only last coordiates the rest are 0 revisit before exam
def determine_point_orientation(p1, p2, p3):
    """
    Determines if three points make a counter-clockwise turn.

    Args:
        p1 (tuple): The first point as a tuple (x, y).
        p2 (tuple): The second point as a tuple (x, y).
        p3 (tuple): The third point as a tuple (x, y).

    Returns:
        int: A positive value if the points make a counter-clockwise turn,
             a negative value if they make a clockwise turn,
             and zero if the points are collinear.
    """
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])


# Graham Scan implementation
def graham_scan(points_input):
    # Copy and sort the points by x-coordinate, and by y-coordinate in case of a tie
    points_sorted = sorted(points_input, key=lambda p: (p[0], p[1]))

    # Initialize the upper and lower parts of the hull
    lower = []
    upper = []

    canvas.delete("hull_line")
    canvas.delete("scan_line")

    # Process the points for the lower part of the hull
    for p in points_sorted:
        # Draw the scan line at the current x-coordinate
        draw_scan_line(p[0])
        # Add point to the lower hull
        while len(lower) >= 2 and determine_point_orientation(lower[-2], lower[-1], p) <= 0:
            # If the last two points and the current point do not make a counter-clockwise turn,
            # remove the last point from the lower hull
            lower.pop()
            # Draw the current state of the partial hull
            draw_partial_hull(lower + upper)
            # Update the canvas to reflect changes
            canvas.update()
            # Pause for a short duration to visualize the process
            time.sleep(delay_var.get())
        # Add the current point to the lower hull
        lower.append(p)
        # Draw the current state of the partial hull
        draw_partial_hull(lower + upper)
        # Update the canvas to reflect changes
        canvas.update()
        # Pause for a short duration to visualize the process
        time.sleep(delay_var.get())

    # Process the points for the upper part of the hull in reverse order
    for p in reversed(points_sorted):
        # Draw the scan line at the current x-coordinate
        draw_scan_line(p[0])
        # Add point to the upper hull
        while len(upper) >= 2 and determine_point_orientation(upper[-2], upper[-1], p) <= 0:
            # If the last two points and the current point do not make a counter-clockwise turn,
            # remove the last point from the upper hull
            upper.pop()
            # Draw the current state of the partial hull
            draw_partial_hull(lower + upper)
            # Update the canvas to reflect changes
            canvas.update()
            # Pause for a short duration to visualize the process
            time.sleep(delay_var.get())
        # Add the current point to the upper hull
        upper.append(p)
        # Draw the current state of the partial hull
        draw_partial_hull(lower + upper)
        # Update the canvas to reflect changes
        canvas.update()
        # Pause for a short duration to visualize the process
        time.sleep(delay_var.get())

    # Concatenate lower and upper to get the full hull
    full_hull = lower[:-1] + upper[:-1]

    # Draw the final convex hull
    draw_convex_hull(full_hull)
    canvas.delete("scan_line")


# Function to draw the convex hull
def draw_convex_hull(hull_points):
    canvas.delete("hull_line")
    for i in range(len(hull_points)):
        x1, y1 = hull_points[i]
        x2, y2 = hull_points[(i + 1) % len(hull_points)]
        canvas.create_line(x1, y1, x2, y2, fill='red',
                           width=2, tags="hull_line")
    canvas.update()


# Function to draw partial hull during the algorithm execution
def draw_partial_hull(hull_points):
    canvas.delete("hull_line")
    for i in range(len(hull_points) - 1):
        x1, y1 = hull_points[i]
        x2, y2 = hull_points[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill='blue',
                           width=2, tags="hull_line")


# Function to draw the scan line
def draw_scan_line(x_pos):
    canvas.delete("scan_line")
    canvas.create_line(x_pos, 0, x_pos, canvas.winfo_height(),
                       fill='green', dash=(4, 2), tags="scan_line")
    canvas.update()


# Jarvis' March algorithm implementation
def jarvis_march(points_input):
    # Copy the list to avoid modifying the original
    all_points = points_input.copy()
    n = len(all_points)

    # Find the leftmost point and set
    leftmost = min(all_points, key=lambda p: p[0])
    point_on_hull = leftmost
    hull = []

    # Clear previous hull and scan line visualizations
    canvas.delete("hull_line")
    canvas.delete("scan_line")
    # Initialize the loop counter
    iterations = 0
    while True:
        # Add the current point on the hull to the hull list
        hull.append(point_on_hull)
        # Start with the first point as the endpoint_canidate
        endpoint_canidate = all_points[0]

        # Visualize the current point on the hull
        canvas.delete("current_point")
        x, y = point_on_hull
        # Draw a circle around the current point in orange
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5,
                           outline='orange', width=2, tags="current_point")
        canvas.update()
        time.sleep(delay_var.get())

        # Iterate through all points to find the most counterclockwise point
        for j in range(1, n):
            # If endpoint_canidate is the same as point_on_hull or all_points[j] is more counterclockwise than the current endpoint_canidate
            if endpoint_canidate == point_on_hull or determine_point_orientation(point_on_hull, endpoint_canidate, all_points[j]) < 0:
                # Update the endpoint_canidate to the new candidate
                endpoint_canidate = all_points[j]

                # Visualize the potential endpoint_canidate
                canvas.delete("candidate_line")
                canvas.create_line(point_on_hull[0], point_on_hull[1], endpoint_canidate[0], endpoint_canidate[1], fill='gray', dash=(
                    4, 2), tags="candidate_line")
                canvas.update()
                time.sleep(delay_var.get())

        # Remove the candidate line visualization
        canvas.delete("candidate_line")

        # Visualize the edge added to the hull
        canvas.create_line(point_on_hull[0], point_on_hull[1], endpoint_canidate[0],
                           endpoint_canidate[1], fill='blue', width=2, tags="hull_line")
        canvas.update()
        time.sleep(delay_var.get())

        # Move to the next point on the hull
        point_on_hull = endpoint_canidate

        # If we have returned to the starting point, the hull is complete
        if endpoint_canidate == hull[0]:
            break
        # Increment the loop counter
        iterations += 1
        # ---- end of while loop----

    # Draw the final convex hull
    draw_convex_hull(hull)
    canvas.delete("current_point")


# Start the Tkinter event loop
root.mainloop()
