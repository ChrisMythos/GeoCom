from time import sleep
import tkinter as tk
import random
from dataclasses import dataclass
from typing import List
from convex_hull import graham_scan


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass
class Triangle:
    p1: Point
    p2: Point
    p3: Point


def draw_hull(hull_points):
    canvas.delete("hull")
    for i in range(len(hull_points)):
        p1 = hull_points[i]
        p2 = hull_points[(i + 1) % len(hull_points)]
        canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill="red", tags="hull")
    root.update()


def draw_connections(hull_points, new_point):
    """Connects all points on the hull to a new point."""
    for p in hull_points:
        canvas.create_line(
            p.x, p.y, new_point.x, new_point.y, fill="red", tags="connections"
        )
    root.update()


def perform_delaunay():
    global triangles  # Store triangles globally

    # Step 1: Generate convex hull if not already done
    if not canvas.find_withtag("hull"):
        hull_points = graham_scan(points)
        draw_hull(hull_points)
        sleep(0.1)

    # Step 2: Get the hull points from the points list
    hull_points = [p for p in points if p in hull_points]

    # Step 3: Add the first random point from remaining points
    points_set = set(points)
    hull_set = set(hull_points)
    points_set.difference_update(hull_set)
    remaining_points = list(points_set)

    if not remaining_points:
        print("No remaining points to add!")
        return

    new_point = random.choice(remaining_points)

    # Step 4: Connect the new point to all points on the hull
    draw_connections(hull_points, new_point)

    # Step 5: Store the triangles created by the new point and the hull
    for i in range(len(hull_points)):
        p1 = hull_points[i]
        p2 = hull_points[(i + 1) % len(hull_points)]
        triangle = Triangle(p1, p2, new_point)
        triangles.append(triangle)

    # remove the new point from the remaining points
    remaining_points.remove(new_point)

    # draw new point
    new_point = random.choice(remaining_points)

    # mark the new point with a circle around it
    canvas.create_oval(
        new_point.x - 5,
        new_point.y - 5,
        new_point.x + 5,
        new_point.y + 5,
        outline="red",
        tags="new_point",
    )
    # Step 6: Find the triangle the new point is in
    found_triangle = None
    for triangle in triangles:
        if point_in_triangle(new_point, triangle):
            found_triangle = triangle
            break

    if found_triangle:
        highlight_triangle(found_triangle)


def point_in_triangle(point_p: Point, triangle: Triangle) -> bool:
    """Check if point P is inside triangle ABC."""

    def calculate_barycentric_coordinates(p, a, b, c):
        denominator = (b.y - c.y) * (a.x - c.x) + (c.x - b.x) * (a.y - c.y)

        alpha = ((b.y - c.y) * (p.x - c.x) + (c.x - b.x) * (p.y - c.y)) / denominator

        beta = ((c.y - a.y) * (p.x - c.x) + (a.x - c.x) * (p.y - c.y)) / denominator

        gamma = 1 - alpha - beta

        return alpha, beta, gamma

    alpha, beta, gamma = calculate_barycentric_coordinates(
        point_p, triangle.p1, triangle.p2, triangle.p3
    )

    return alpha >= 0 and beta >= 0 and gamma >= 0


def highlight_triangle(triangle: Triangle):
    """Highlight the triangle on the canvas."""
    canvas.delete("highlighted_triangle")
    canvas.create_line(
        triangle.p1.x,
        triangle.p1.y,
        triangle.p2.x,
        triangle.p2.y,
        fill="blue",
        width=2,
        tags="highlighted_triangle",
    )
    canvas.create_line(
        triangle.p2.x,
        triangle.p2.y,
        triangle.p3.x,
        triangle.p3.y,
        fill="blue",
        width=2,
        tags="highlighted_triangle",
    )
    canvas.create_line(
        triangle.p3.x,
        triangle.p3.y,
        triangle.p1.x,
        triangle.p1.y,
        fill="blue",
        width=2,
        tags="highlighted_triangle",
    )
    root.update()


###############################################
# GUI
###############################################
root = tk.Tk()
root.title("Delaunay Triangulation with Dataclasses - Step by Step")

root.geometry("1000x800")
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

sidebar = tk.Frame(root, width=200, bg="lightgray", padx=10, pady=10)
sidebar.grid(row=0, column=0, sticky="ns")

heading_text = tk.Label(
    sidebar,
    text="Delaunay Triangulation",
    font=("Arial", 18),
    bg="lightgray",
    fg="black",
)
heading_text.pack(pady=5)

point_count_slider = tk.Scale(
    sidebar,
    from_=10,
    to=200,
    orient=tk.HORIZONTAL,
    label="Anzahl der Punkte",
    length=150,
)
point_count_slider.set(20)
point_count_slider.pack(pady=5)

canvas = tk.Canvas(root, bg="white")
canvas.grid(row=0, column=1, sticky="nsew")

points: List[Point] = []
point_objs = []
triangles: List[Triangle] = []  # List to store triangles


def clear_canvas():
    canvas.delete("all")
    del points[:]
    del point_objs[:]
    del triangles[:]


def add_point(x, y):
    p = Point(x, y)
    points.append(p)
    obj = canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black", tags="point")
    point_objs.append((obj, p))


def on_canvas_click(event):
    add_point(event.x, event.y)


def generate_random_points():
    clear_canvas()
    n = point_count_slider.get()
    # Make sure canvas dimensions are available
    root.update_idletasks()
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    for _ in range(n):
        x = random.randint(10, width - 10)
        y = random.randint(10, height - 10)
        add_point(x, y)


generate_points_button = tk.Button(
    sidebar, text="Punkte generieren", command=generate_random_points
)
generate_points_button.pack(pady=10)

delaunay_button = tk.Button(
    sidebar, text="Delaunay Triangulation starten", command=perform_delaunay
)
delaunay_button.pack(pady=10)

clear_button = tk.Button(sidebar, text="Löschen", command=clear_canvas)
clear_button.pack(pady=10)

canvas.bind("<Button-1>", on_canvas_click)

root.mainloop()
