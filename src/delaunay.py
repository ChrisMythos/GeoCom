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
        # Wir stellen sicher, dass alle Operationen, die von sortierten
        # Scheitelpunkten abhängen, sich auf eine stabile Reihenfolge verlassen können.
        # Wenn in __post_init__ in einer Dataclass ohne `frozen=True` mutiert,
        # ist es erlaubt. Aber wir speichern sie nicht anders; stattdessen behandeln wir das Sortieren in __hash__.
        pass

    def __hash__(self):
        # Sortieren der Vertices, um eine stabile Reihenfolge zu gewährleisten
        v = sorted(self.vertices(), key=lambda p: (p.x, p.y))
        return hash((v[0], v[1], v[2]))

    def __eq__(self, other):
        if not isinstance(other, Triangle):
            return False
        return set(self.vertices()) == set(other.vertices())


def circumcircle_contains(tri: Triangle, p: Point) -> bool:
    p1, p2, p3 = tri.p1, tri.p2, tri.p3  # vertices des Dreiecks
    ax, ay = p1.x, p1.y  # vertex A
    bx, by = p2.x, p2.y  # vertex B
    cx, cy = p3.x, p3.y  # vertex C
    dx, dy = p.x, p.y    # punkt D (der zu testende Punkt)

    # Berechnung der Determinante
    A = ax - dx
    B = ay - dy
    C = (ax**2 - dx**2) + (ay**2 - dy**2)
    D = bx - dx
    E = by - dy
    F = (bx**2 - dx**2) + (by**2 - dy**2)
    G = cx - dx
    H = cy - dy
    I = (cx**2 - dx**2) + (cy**2 - dy**2)

    # wenn die Determinante positiv ist, liegt der Punkt innerhalb des Umkreises des Dreiecks
    det = A*(E*I - F*H) - B*(D*I - F*G) + C*(D*H - E*G)
    return det > 0


def point_in_triangle(pt: Point, tri: Triangle) -> bool:
    p = pt
    p1, p2, p3 = tri.p1, tri.p2, tri.p3
    denom = ((p2.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y))
    if denom == 0:
        return False
    w1 = ((p2.y - p3.y)*(p.x - p3.x) + (p3.x - p2.x)*(p.y - p3.y))/denom
    w2 = ((p3.y - p1.y)*(p.x - p3.x) + (p1.x - p3.x)*(p.y - p3.y))/denom
    w3 = 1 - w1 - w2
    return (w1 >= 0) and (w2 >= 0) and (w3 >= 0)


def find_triangle_containing_point(triangles: Set[Triangle], pt: Point):
    # Checken aller Dreiecke, ob der Punkt darin enthalten ist (O(n))
    for t in triangles:
        if point_in_triangle(pt, t):
            return t
    return None


def delaunay_insert_point(triangles: Set[Triangle], all_points: List[Point], new_point: Point) -> Set[Triangle]:
    """
    Inserts a new point into an existing Delaunay triangulation.
    This function finds the triangle containing the new point, removes it, and creates three new triangles
    by connecting the new point to the vertices of the containing triangle.

    Args:
        triangles (Set[Triangle]): A set of triangles representing the current Delaunay triangulation.
        all_points (List[Point]): A list of all points in the triangulation.
        new_point (Point): The new point to be inserted into the triangulation.

    Returns:
        Set[Triangle]: The updated set of triangles after inserting the new point.
    """
    container_triangle = find_triangle_containing_point(triangles, new_point)
    if container_triangle is None:
        return triangles

    triangles.remove(container_triangle)
    p1, p2, p3 = container_triangle.p1, container_triangle.p2, container_triangle.p3
    new_tris = [
        Triangle(new_point, p1, p2),
        Triangle(new_point, p2, p3),
        Triangle(new_point, p3, p1)
    ]
    for nt in new_tris:
        triangles.add(nt)
    # For now, no Delaunay correction loop to keep things simple.
    return triangles


###############################################
# GUI
###############################################
root = tk.Tk()
root.title("Delaunay Triangulation with Dataclasses")

root.geometry("1000x800")
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

sidebar = tk.Frame(root, width=200, bg='lightgray', padx=10, pady=10)
sidebar.grid(row=0, column=0, sticky="ns")

heading_text = tk.Label(sidebar, text="Delaunay Triangulation", font=(
    "Arial", 18), bg='lightgray', fg='black')
heading_text.pack(pady=5)

point_count_slider = tk.Scale(
    sidebar, from_=10, to=200, orient=tk.HORIZONTAL, label='Anzahl der Punkte', length=150)
point_count_slider.set(30)
point_count_slider.pack(pady=5)

canvas = tk.Canvas(root, bg='white')
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
    obj = canvas.create_oval(x-3, y-3, x+3, y+3, fill='black', tags='point')
    point_objs.append((obj, p))


def on_canvas_click(event):
    add_point(event.x, event.y)


def generate_random_points():
    clear_canvas()
    n = point_count_slider.get()
    for _ in range(n):
        x = random.randint(50, 950)
        y = random.randint(50, 750)
        add_point(x, y)


def perform_delaunay():
    if len(points) < 3:
        return

    # Compute hull using the imported function
    points_tuple = [(p.x, p.y) for p in points]
    hull = graham_scan(points_tuple)
    hull_points = [Point(h[0], h[1]) for h in hull]

    hull_set = set(hull_points)
    interior_points = [p for p in points if p not in hull_set]

    random.shuffle(interior_points)

    triangles: Set[Triangle] = set()
    if len(interior_points) == 0:
        # If no interior points, just triangulate hull naively if possible
        if len(hull_points) < 3:
            return
        for i in range(1, len(hull_points)-1):
            t = Triangle(hull_points[0], hull_points[i], hull_points[i+1])
            triangles.add(t)
    else:
        p1 = interior_points[0]
        for i in range(len(hull_points)):
            t = Triangle(p1, hull_points[i],
                         hull_points[(i+1) % len(hull_points)])
            triangles.add(t)

        for i in range(1, len(interior_points)):
            p_i = interior_points[i]
            triangles = delaunay_insert_point(triangles, points, p_i)

    # Draw result
    canvas.delete("triangle")
    for tri in triangles:
        canvas.create_polygon([tri.p1.x, tri.p1.y, tri.p2.x, tri.p2.y, tri.p3.x, tri.p3.y],
                              outline='blue', fill='', tags="triangle")


generate_points_button = tk.Button(
    sidebar, text="Punkte generieren", command=generate_random_points)
generate_points_button.pack(pady=10)

delaunay_button = tk.Button(
    sidebar, text="Delaunay Triangulation starten", command=perform_delaunay)
delaunay_button.pack(pady=10)

clear_button = tk.Button(sidebar, text="Löschen", command=clear_canvas)
clear_button.pack(pady=10)

canvas.bind("<Button-1>", on_canvas_click)

root.mainloop()
