#!/usr/bin/env python3
"""
Delaunay Triangulation with Tkinter Visualization

Improvements:
- Clear separation between triangulation logic and GUI logic.
- Consistent use of type hints.
- Better variable naming and modular functions.
- Use of helper function delay_update() to handle GUI updates with delays.
- Some minor algorithmic optimizations.
"""

import random
from time import sleep
import tkinter as tk
from dataclasses import dataclass
from typing import List, Set, Tuple, Optional

# Assuming graham_scan is implemented in convex_hull.py
from src.convex_hull import graham_scan


# ===========================
# Data Structures and Helpers
# ===========================

@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass
class Triangle:
    p1: Point
    p2: Point
    p3: Point

    def __post_init__(self) -> None:
        self.order_vertices_ccw()

    def order_vertices_ccw(self) -> None:
        # Ensure vertices are in counterclockwise order using signed area
        area = (self.p2.x - self.p1.x) * (self.p3.y - self.p1.y) - \
               (self.p2.y - self.p1.y) * (self.p3.x - self.p1.x)
        if area < 0:
            self.p2, self.p3 = self.p3, self.p2

    def vertices(self) -> List[Point]:
        return [self.p1, self.p2, self.p3]

    def __hash__(self) -> int:
        # Use sorted vertices to ensure consistent hash independent of order
        sorted_vertices = sorted(self.vertices(), key=lambda pt: (pt.x, pt.y))
        return hash(tuple(sorted_vertices))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Triangle):
            return False
        return set(self.vertices()) == set(other.vertices())


def normalize_edge(p1: Point, p2: Point) -> Tuple[Point, Point]:
    return tuple(sorted((p1, p2), key=lambda pt: (pt.x, pt.y)))


def is_valid_triangle(tri: Triangle) -> bool:
    # A triangle is valid if all vertices are unique.
    return len({tri.p1, tri.p2, tri.p3}) == 3


def circumcircle_contains(tri: Triangle, pt: Point, epsilon: float = 1e-8) -> bool:
    # Check whether the point lies inside the circumcircle of the triangle.
    ax, ay = tri.p1.x, tri.p1.y
    bx, by = tri.p2.x, tri.p2.y
    cx, cy = tri.p3.x, tri.p3.y
    dx, dy = pt.x, pt.y

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
    return det > epsilon


def point_in_triangle(pt: Point, tri: Triangle) -> bool:
    # Barycentric coordinate test for point inside triangle.
    p1, p2, p3 = tri.p1, tri.p2, tri.p3
    denom = (p2.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y)
    if denom == 0:
        return False  # Degenerate triangle
    w1 = ((p2.y - p3.y) * (pt.x - p3.x) + (p3.x - p2.x) * (pt.y - p3.y)) / denom
    w2 = ((p3.y - p1.y) * (pt.x - p3.x) + (p1.x - p3.x) * (pt.y - p3.y)) / denom
    w3 = 1 - w1 - w2
    return w1 >= 0 and w2 >= 0 and w3 >= 0


def find_triangle_containing_point(triangles: Set[Triangle], pt: Point) -> Optional[Triangle]:
    for tri in triangles:
        if point_in_triangle(pt, tri):
            return tri
    return None


def find_triangle_neighbors(triangles: Set[Triangle], target: Triangle) -> List[Triangle]:
    target_edges = {
        normalize_edge(*edge) for edge in [(target.p1, target.p2), (target.p2, target.p3), (target.p3, target.p1)]
    }
    neighbors = []
    for tri in triangles:
        if tri == target:
            continue
        tri_edges = [
            normalize_edge(tri.p1, tri.p2),
            normalize_edge(tri.p2, tri.p3),
            normalize_edge(tri.p3, tri.p1),
        ]
        if any(edge in target_edges for edge in tri_edges):
            neighbors.append(tri)
    return neighbors


def find_cavity(triangles: Set[Triangle], new_pt: Point, container: Triangle) -> Set[Triangle]:
    bad_triangles = {container}
    stack = [container]
    while stack:
        current = stack.pop()
        for neighbor in find_triangle_neighbors(triangles, current):
            if neighbor not in bad_triangles and circumcircle_contains(neighbor, new_pt):
                # Uncomment for debugging:
                # print("Bad triangle found:", neighbor)
                bad_triangles.add(neighbor)
                stack.append(neighbor)
    return bad_triangles


# ===========================
# Delaunay Insertion & Triangulation
# ===========================

def delaunay_insert_point(
    triangles: Set[Triangle],
    new_pt: Point,
    canvas: tk.Canvas,
    delay: float
) -> Set[Triangle]:
    highlight_new_point(canvas, new_pt, delay)

    container = find_triangle_containing_point(triangles, new_pt)
    if container is None:
        print("No containing triangle found for point:", new_pt)
        return triangles

    highlight_container_triangle(canvas, container, delay)
    bad_triangles = find_cavity(triangles, new_pt, container)
    highlight_bad_triangles(canvas, bad_triangles, delay)

    remaining_triangles = {tri for tri in triangles if tri not in bad_triangles and is_valid_triangle(tri)}
    # Remove bad triangles from the canvas before drawing new ones.
    canvas.delete("triangle_containing_point", "triangle", "bad_triangle")
    draw_triangles(canvas, remaining_triangles, delay)

    # Determine boundary edges from bad triangles.
    edge_count: dict[Tuple[Point, Point], int] = {}
    def add_edge(a: Point, b: Point) -> None:
        edge = normalize_edge(a, b)
        edge_count[edge] = edge_count.get(edge, 0) + 1

    for tri in bad_triangles:
        v = tri.vertices()
        add_edge(v[0], v[1])
        add_edge(v[1], v[2])
        add_edge(v[2], v[0])
    boundary_edges = [edge for edge, count in edge_count.items() if count == 1]

    # Draw boundary edges for visualization.
    for edge in boundary_edges:
        canvas.create_line(edge[0].x, edge[0].y, edge[1].x, edge[1].y,
                           fill="red", tags="boundary_edge", width=4)
    delay_update(canvas, delay)

    if not boundary_edges:
        print("No boundary edges found; degenerate case.")
        return remaining_triangles

    # Reconstruct a polygon loop from boundary edges.
    polygon = [boundary_edges[0][0], boundary_edges[0][1]]
    used_edges = {boundary_edges[0]}
    while len(used_edges) < len(boundary_edges):
        last_point = polygon[-1]
        found_next = False
        for edge in boundary_edges:
            if edge in used_edges:
                continue
            if edge[0] == last_point:
                polygon.append(edge[1])
                used_edges.add(edge)
                found_next = True
                break
            elif edge[1] == last_point:
                polygon.append(edge[0])
                used_edges.add(edge)
                found_next = True
                break
        if not found_next:
            print("Could not form a closed polygon from boundary edges.")
            break

    # Fill the hole by connecting the new point to each edge of the polygon.
    for i in range(len(polygon)):
        next_index = (i + 1) % len(polygon)
        new_triangle = Triangle(new_pt, polygon[i], polygon[next_index])
        remaining_triangles.add(new_triangle)

    canvas.delete("boundary_edge", "new_point_circle")
    draw_triangles(canvas, remaining_triangles, delay)
    return remaining_triangles


def perform_delaunay(points: List[Point], canvas: tk.Canvas, delay: float) -> None:
    if len(points) < 3:
        return

    # Compute convex hull (expects list of (x,y) tuples).
    points_tuple = [(pt.x, pt.y) for pt in points]
    hull_tuples = graham_scan(points_tuple)
    hull_points = [Point(x, y) for x, y in hull_tuples]
    hull_set = set(hull_points)
    interior_points = [pt for pt in points if pt not in hull_set]
    random.shuffle(interior_points)
    draw_hull(canvas, hull_points, delay)

    triangles: Set[Triangle] = set()
    if not interior_points:
        if len(hull_points) < 3:
            return
        # Special case: triangulate convex hull.
        for i in range(1, len(hull_points) - 1):
            triangles.add(Triangle(hull_points[0], hull_points[i], hull_points[i + 1]))
        draw_triangles(canvas, triangles, delay)
    else:
        # Initialize triangulation using the first interior point.
        first_pt = interior_points[0]
        for i in range(len(hull_points)):
            triangles.add(Triangle(first_pt, hull_points[i], hull_points[(i + 1) % len(hull_points)]))
        draw_triangles(canvas, triangles, delay)

        # Check and flip edges if necessary to enforce Delaunay condition.
        for tri in list(triangles):
            for neighbor in find_triangle_neighbors(triangles, tri):
                shared = set(tri.vertices()) & set(neighbor.vertices())
                if len(shared) == 2:
                    tri_opposite = (set(tri.vertices()) - shared).pop()
                    neighbor_opposite = (set(neighbor.vertices()) - shared).pop()
                    shared_list = list(shared)
                    test_triangle = Triangle(shared_list[0], shared_list[1], neighbor_opposite)
                    if circumcircle_contains(test_triangle, tri_opposite):
                        # Flip edge.
                        # Uncomment for debugging:
                        # print("Flipping edge for Delaunay condition:", shared)
                        triangles.remove(tri)
                        triangles.remove(neighbor)
                        triangles.add(Triangle(tri_opposite, shared_list[0], neighbor_opposite))
                        triangles.add(Triangle(tri_opposite, neighbor_opposite, shared_list[1]))
                        break
            else:
                continue
            break

        draw_triangles(canvas, triangles, delay)
        # Insert remaining interior points.
        for idx, pt in enumerate(interior_points[1:], start=1):
            # Uncomment for debugging:
            # print(f"Inserting interior point {idx}: {pt}")
            triangles = delaunay_insert_point(triangles, pt, canvas, delay)
            draw_triangles(canvas, triangles, delay)


# ===========================
# GUI Helper Functions
# ===========================

def delay_update(canvas: tk.Canvas, delay: float) -> None:
    """Helper to delay and update the canvas without freezing the UI."""
    canvas.update()
    sleep(delay)


def highlight_new_point(canvas: tk.Canvas, pt: Point, delay: float) -> None:
    canvas.create_oval(pt.x - 5, pt.y - 5, pt.x + 5, pt.y + 5,
                       outline="orange", tags="new_point_circle", width=3)
    delay_update(canvas, delay)


def highlight_container_triangle(canvas: tk.Canvas, tri: Triangle, delay: float) -> None:
    canvas.create_polygon(
        [tri.p1.x, tri.p1.y, tri.p2.x, tri.p2.y, tri.p3.x, tri.p3.y],
        outline="green", fill="", tags="triangle_containing_point", width=4)
    delay_update(canvas, delay)


def highlight_bad_triangles(canvas: tk.Canvas, triangles: Set[Triangle], delay: float) -> None:
    for tri in triangles:
        canvas.create_polygon(
            [tri.p1.x, tri.p1.y, tri.p2.x, tri.p2.y, tri.p3.x, tri.p3.y],
            outline="lightgreen", fill="", tags="bad_triangle", width=4)
    delay_update(canvas, delay)


def draw_hull(canvas: tk.Canvas, hull_points: List[Point], delay: float) -> None:
    canvas.delete("hull")
    num = len(hull_points)
    for i in range(num):
        p1 = hull_points[i]
        p2 = hull_points[(i + 1) % num]
        canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill="red", tags="hull")
    delay_update(canvas, delay)


def draw_triangles(canvas: tk.Canvas, triangles: Set[Triangle], delay: float) -> None:
    canvas.delete("triangle")
    for tri in triangles:
        canvas.create_polygon(
            [tri.p1.x, tri.p1.y, tri.p2.x, tri.p2.y, tri.p3.x, tri.p3.y],
            outline="blue", fill="", tags="triangle")
    delay_update(canvas, delay)


# ===========================
# GUI Setup and Event Handlers
# ===========================

def main() -> None:
    root = tk.Tk()
    root.title("Delaunay Triangulation (Improved Version)")
    root.geometry("1000x800")
    root.grid_columnconfigure(0, weight=0)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    sidebar = tk.Frame(root, width=200, bg="lightgray", padx=10, pady=10)
    sidebar.grid(row=0, column=0, sticky="ns")

    heading = tk.Label(sidebar, text="Delaunay Triangulation", font=("Arial", 18),
                       bg="lightgray", fg="black")
    heading.pack(pady=5)

    point_count_slider = tk.Scale(sidebar, from_=5, to=50, orient=tk.HORIZONTAL,
                                  label="Number of Points", length=150)
    point_count_slider.set(20)
    point_count_slider.pack(pady=5)

    sleep_time_slider = tk.Scale(sidebar, from_=0, to=2, resolution=0.1,
                                 orient=tk.HORIZONTAL, label="Delay (sec)", length=150)
    sleep_time_slider.set(0.5)
    sleep_time_slider.pack(pady=5)

    canvas = tk.Canvas(root, bg="white")
    canvas.grid(row=0, column=1, sticky="nsew")

    points: List[Point] = []
    point_objs = []

    def clear_canvas() -> None:
        canvas.delete("all")
        points.clear()
        point_objs.clear()

    def add_point(x: int, y: int) -> None:
        pt = Point(x, y)
        points.append(pt)
        # Draw the point.
        oval = canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black", tags="point")
        point_objs.append((oval, pt))
        # Draw the coordinates below the point.
        text = canvas.create_text(x, y + 10, text=f"({x}, {y})",
                                  font=("Arial", 8), fill="gray", tags="coordinates")
        point_objs.append((text, pt))

    def on_canvas_click(event) -> None:
        add_point(event.x, event.y)

    def generate_random_points() -> None:
        clear_canvas()
        n = point_count_slider.get()
        root.update_idletasks()
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        for _ in range(n):
            x = random.randint(5, width - 5)
            y = random.randint(5, height - 5)
            add_point(x, y)

    def start_triangulation() -> None:
        delay = sleep_time_slider.get()
        perform_delaunay(points, canvas, delay)

    generate_points_button = tk.Button(sidebar, text="Generate Points", command=generate_random_points)
    generate_points_button.pack(pady=10)

    delaunay_button = tk.Button(sidebar, text="Start Delaunay Triangulation", command=start_triangulation)
    delaunay_button.pack(pady=10)

    clear_button = tk.Button(sidebar, text="Clear", command=clear_canvas)
    clear_button.pack(pady=10)

    canvas.bind("<Button-1>", on_canvas_click)

    root.mainloop()


if __name__ == "__main__":
    main()
