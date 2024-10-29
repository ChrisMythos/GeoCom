import tkinter as tk
from tkinter import messagebox
import time

# Create the main application window
root = tk.Tk()
root.title("Convex Hull Visualizer")

# Set the window size
root.geometry("800x600")

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
    resolution=0.1,
    orient='horizontal',
    variable=delay_var
)
delay_slider.pack()

# Function to compute the convex hull using the selected algorithm


def compute_convex_hull():
    if len(points) < 3:
        messagebox.showerror(
            "Error", "At least 3 points are required to compute a convex hull.")
        return
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


# Function to calculate the cross product (ccw test) of three points p1, p2, p3
def ccw(p1, p2, p3):
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
    for i, p in enumerate(points_sorted):
        # Draw the scan line at the current x-coordinate
        draw_scan_line(p[0])
        # Add point to the lower hull
        while len(lower) >= 2 and ccw(lower[-2], lower[-1], p) <= 0:
            lower.pop()
            draw_partial_hull(lower + upper)
            canvas.update()
            time.sleep(0.2)
        lower.append(p)
        draw_partial_hull(lower + upper)
        canvas.update()
        time.sleep(delay_var.get())

    # Process the points for the upper part of the hull
    for i, p in enumerate(reversed(points_sorted)):
        # Draw the scan line at the current x-coordinate
        draw_scan_line(p[0])
        # Add point to the upper hull
        while len(upper) >= 2 and ccw(upper[-2], upper[-1], p) <= 0:
            upper.pop()
            draw_partial_hull(lower + upper)
            canvas.update()
            time.sleep(0.2)
        upper.append(p)
        draw_partial_hull(lower + upper)
        canvas.update()
        time.sleep(0.2)

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
    S = points_input.copy()
    n = len(S)

    # Find the leftmost point
    leftmost = min(S, key=lambda p: p[0])
    point_on_hull = leftmost
    hull = []

    canvas.delete("hull_line")
    canvas.delete("scan_line")

    i = 0
    while True:
        hull.append(point_on_hull)
        endpoint = S[0]

        # Visualize current point_on_hull
        canvas.delete("current_point")
        x, y = point_on_hull
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5,
                           outline='orange', width=2, tags="current_point")
        canvas.update()
        time.sleep(delay_var.get())

        for j in range(1, n):
            # If endpoint is the same as point_on_hull or S[j] is more counterclockwise
            if endpoint == point_on_hull or ccw(point_on_hull, endpoint, S[j]) < 0:
                endpoint = S[j]

                # Visualize potential endpoint
                canvas.delete("candidate_line")
                canvas.create_line(point_on_hull[0], point_on_hull[1], endpoint[0], endpoint[1], fill='gray', dash=(
                    4, 2), tags="candidate_line")
                canvas.update()
                time.sleep(delay_var.get())

        # Remove candidate line visualization
        canvas.delete("candidate_line")

        # Visualize the edge added to the hull
        canvas.create_line(point_on_hull[0], point_on_hull[1], endpoint[0],
                           endpoint[1], fill='blue', width=2, tags="hull_line")
        canvas.update()
        time.sleep(delay_var.get())

        point_on_hull = endpoint

        if endpoint == hull[0]:
            break
        i += 1

    # Draw the final convex hull
    draw_convex_hull(hull)
    canvas.delete("current_point")


# Start the Tkinter event loop
root.mainloop()
