from time import sleep
import tkinter as tk
import random
from dataclasses import dataclass
from typing import List, Set
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

    def vertices(self) -> List[Point]:
        return [self.p1, self.p2, self.p3]

    def __post_init__(self):
        pass

    def __hash__(self):
        v = sorted(self.vertices(), key=lambda p: (p.x, p.y))
        return hash((v[0], v[1], v[2]))

    def __eq__(self, other):
        if not isinstance(other, Triangle):
            return False
        return set(self.vertices()) == set(other.vertices())


def circumcircle_contains(tri: Triangle, p: Point) -> bool:
    p1, p2, p3 = tri.p1, tri.p2, tri.p3
    ax, ay = p1.x, p1.y
    bx, by = p2.x, p2.y
    cx, cy = p3.x, p3.y
    dx, dy = p.x, p.y

    A = ax - dx
    B = ay - dy
    C = (ax**2 - dx**2) + (ay**2 - dy**2)
    D = bx - dx
    E = by - dy
    F = (bx**2 - dx**2) + (by**2 - dy**2)
    G = cx - dx
    H = cy - dy
    I = (cx**2 - dx**2) + (cy**2 - dy**2)

    det = A * (E * I - F * H) - B * (D * I - F * G) + C * (D * H - E * G)
    return det > 0


def point_in_triangle(pt: Point, tri: Triangle) -> bool:
    p = pt
    p1, p2, p3 = tri.p1, tri.p2, tri.p3
    denom = (p2.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y)
    if denom == 0:
        return False
    w1 = ((p2.y - p3.y) * (p.x - p3.x) + (p3.x - p2.x) * (p.y - p3.y)) / denom
    w2 = ((p3.y - p1.y) * (p.x - p3.x) + (p1.x - p3.x) * (p.y - p3.y)) / denom
    w3 = 1 - w1 - w2
    return (w1 >= 0) and (w2 >= 0) and (w3 >= 0)


def find_triangle_containing_point(triangles: Set[Triangle], pt: Point):
    for t in triangles:
        if point_in_triangle(pt, t):
            return t
    return None


def delaunay_insert_point(
    triangles: Set[Triangle], all_points: List[Point], new_point: Point
) -> Set[Triangle]:
    container_triangle = find_triangle_containing_point(triangles, new_point)
    if container_triangle is None:
        return triangles
    # draw the container triangle in red
    canvas.create_polygon(
        [
            container_triangle.p1.x,
            container_triangle.p1.y,
            container_triangle.p2.x,
            container_triangle.p2.y,
            container_triangle.p3.x,
            container_triangle.p3.y,
        ],
        outline="red",
        fill="",
        tags="triangle",
    )
    root.update()
    sleep(0.5)
    # find all triangles that violate the Delaunay condition unsing ajeacent triangles of the container triangle
    # and the new point
    bad_triangles: Set[Triangle] = set()
    for t in triangles:
        if t == container_triangle:
            continue
        if circumcircle_contains(t, new_point):
            bad_triangles.add(t)
    # draw the bad triangles in green
    for t in bad_triangles:
        canvas.create_polygon(
            [t.p1.x, t.p1.y, t.p2.x, t.p2.y, t.p3.x, t.p3.y],
            outline="green",
            fill="",
            tags="triangle",
        )
    root.update()
    sleep(0.5)

    # remove the bad triangles who violate the Delaunay condition
    remianing_triangles = triangles - bad_triangles

    # redraw the remaining triangles
    canvas.delete("triangle")
    for t in remianing_triangles:
        canvas.create_polygon(
            [t.p1.x, t.p1.y, t.p2.x, t.p2.y, t.p3.x, t.p3.y],
            outline="blue",
            fill="",
            tags="triangle",
        )
    root.update()

    sleep(0.5)
    # add new triagles formed by the new point and the walls of whole cut by the removal of bad triangles
    for t in bad_triangles:
        remianing_triangles.add(Triangle(t.p1, t.p2, new_point))
        remianing_triangles.add(Triangle(t.p2, t.p3, new_point))
        remianing_triangles.add(Triangle(t.p3, t.p1, new_point))

    # draw the new triangles in blue
    for t in remianing_triangles:
        canvas.create_polygon(
            [t.p1.x, t.p1.y, t.p2.x, t.p2.y, t.p3.x, t.p3.y],
            outline="blue",
            fill="",
            tags="triangle",
        )
    root.update()
    sleep(0.5)

    return remianing_triangles


def draw_hull(hull_points):
    canvas.delete("hull")
    for i in range(len(hull_points)):
        p1 = hull_points[i]
        p2 = hull_points[(i + 1) % len(hull_points)]
        canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill="red", tags="hull")
    root.update()
    sleep(0.5)


def draw_triangulation(triangles):
    canvas.delete("triangle")
    for tri in triangles:
        canvas.create_polygon(
            [tri.p1.x, tri.p1.y, tri.p2.x, tri.p2.y, tri.p3.x, tri.p3.y],
            outline="blue",
            fill="",
            tags="triangle",
        )
    root.update()
    # A short pause to visualize step by step updates.
    sleep(0.5)


def perform_delaunay():
    if len(points) < 3:
        return

    points_tuple = [(p.x, p.y) for p in points]
    hull = graham_scan(points_tuple)
    hull_points = [Point(h[0], h[1]) for h in hull]

    hull_set = set(hull_points)
    interior_points = [p for p in points if p not in hull_set]

    # Step 1: visualize the hull
    draw_hull(hull_points)

    # Shuffle interior points
    random.shuffle(interior_points)

    triangles: Set[Triangle] = set()
    if len(interior_points) == 0:
        if len(hull_points) < 3:
            return
        for i in range(1, len(hull_points) - 1):
            t = Triangle(hull_points[0], hull_points[i], hull_points[i + 1])
            triangles.add(t)
        # Visualize the final triangulation (just the hull)
        draw_triangulation(triangles)
    else:
        p1 = interior_points[0]
        for i in range(len(hull_points)):
            t = Triangle(p1, hull_points[i], hull_points[(i + 1) % len(hull_points)])
            triangles.add(t)
        # Show the initial triangulation after adding the first interior point
        draw_triangulation(triangles)

        # Insert the remaining interior points one by one with visualization after each insertion
        for i in range(1, len(interior_points)):
            p_i = interior_points[i]
            triangles = delaunay_insert_point(triangles, points, p_i)
            # Visualize after inserting each point
            draw_triangulation(triangles)


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


def clear_canvas():
    canvas.delete("all")
    del points[:]
    del point_objs[:]


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
