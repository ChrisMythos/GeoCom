import tkinter as tk
from tkinter import messagebox
import time
import numpy as np

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

# store the line segments
line_segments = []

# store all points
points = []


# Function to handle mouse clicks on the canvas add a point and draw a line after two points are added
def add_point(event):
    x, y = event.x, event.y
    radius = 4
    canvas.create_oval(x - radius, y - radius, x + radius,
                       y + radius, fill='black', tags="point")
    points.append((x, y))
    if len(points) == 2:
        canvas.create_line(points[0][0], points[0][1], points[1][0],
                           points[1][1], fill='black', tags="line_segment")
        line_segments.append((points[0], points[1]))
        points.clear()


# bind the mouse click event to the canvas
canvas.bind("<Button-1>", add_point)


# Start the Tkinter event loop
root.mainloop()
