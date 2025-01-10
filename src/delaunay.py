from time import sleep
import tkinter as tk
import random
from dataclasses import dataclass
from typing import List, Set
from convex_hull import graham_scan
import pdb
@dataclass(frozen=True)
class Point:
    x: float
    y: float

@dataclass
class Triangle:
    p1: Point
    p2: Point
    p3: Point

    def __post_init__(self):
        # Ensure vertices are ordered counterclockwise
        self.order_vertices_ccw()

    def order_vertices_ccw(self):
        # Calculate signed area to determine orientation
        area = (self.p2.x - self.p1.x) * (self.p3.y - self.p1.y) - (
            self.p2.y - self.p1.y
        ) * (self.p3.x - self.p1.x)
        if area < 0:
            # Swap vertices to ensure counterclockwise order
            self.p2, self.p3 = self.p3, self.p2

    def vertices(self) -> List[Point]:
        return [self.p1, self.p2, self.p3]

    def __hash__(self):
        # Sort vertices to ensure consistent hash value
        v = sorted(self.vertices(), key=lambda p: (p.x, p.y))
        return hash((v[0], v[1], v[2]))

    def __eq__(self, other):
        if not isinstance(other, Triangle):
            return False
        return set(self.vertices()) == set(other.vertices())


def circumcircle_contains(tri: Triangle, p: Point, epsilon=1e-8) -> bool:
    # Extract coordinates of the triangle vertices and the point
    p1, p2, p3 = tri.p1, tri.p2, tri.p3
    ax, ay = p1.x, p1.y
    bx, by = p2.x, p2.y
    cx, cy = p3.x, p3.y
    dx, dy = p.x, p.y

    # Compute the differences between the triangle vertices and the point
    A = ax - dx
    B = ay - dy
    C = (ax**2 - dx**2) + (ay**2 - dy**2)
    D = bx - dx
    E = by - dy
    F = (bx**2 - dx**2) + (by**2 - dy**2)
    G = cx - dx
    H = cy - dy
    I = (cx**2 - dx**2) + (cy**2 - dy**2)

    # Calculate the determinant of the matrix
    det = A * (E * I - F * H) - B * (D * I - F * G) + C * (D * H - E * G)

    # Return True if the determinant is positive (point is inside the circumcircle)
    return det > epsilon


def normalize_edge(p1, p2):
    return tuple(sorted((p1, p2), key=lambda p: (p.x, p.y)))

def is_valid_triangle(triangle):
    # Extract points from the triangle
    p1, p2, p3 = triangle.p1, triangle.p2, triangle.p3
    # Use a set to check if all points are unique
    return len({p1, p2, p3}) == 3

def point_in_triangle(pt: Point, tri: Triangle) -> bool:
    # Extract the point and the vertices of the triangle
    p = pt
    p1, p2, p3 = tri.p1, tri.p2, tri.p3

    # Calculate the denominator of the barycentric coordinates
    denom = (p2.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y)
    
    # If the denominator is zero, the points are collinear and the point is not inside the triangle
    if denom == 0:
        return False

    # Calculate the barycentric coordinates
    w1 = ((p2.y - p3.y) * (p.x - p3.x) + (p3.x - p2.x) * (p.y - p3.y)) / denom
    w2 = ((p3.y - p1.y) * (p.x - p3.x) + (p1.x - p3.x) * (p.y - p3.y)) / denom
    w3 = 1 - w1 - w2

    # Check if the point is inside the triangle by verifying if all barycentric coordinates are non-negative
    return (w1 >= 0) and (w2 >= 0) and (w3 >= 0)


def find_triangle_containing_point(triangles: Set[Triangle], pt: Point):
    for t in triangles:
        if point_in_triangle(pt, t):
            return t
    return None


def find_triangle_neighbors(triangles: Set[Triangle], tri: Triangle) -> List[Triangle]:
    # O(n) neighbor search
    nbrs = []
    v = tri.vertices()
    edges = {
        normalize_edge(v[0], v[1]),
        normalize_edge(v[1], v[2]),
        normalize_edge(v[2], v[0]),
    }

    for t in triangles:
        if t == tri:
            continue
        v2 = t.vertices()
        t_edges = [
            normalize_edge(v2[0], v2[1]),
            normalize_edge(v2[1], v2[2]),
            normalize_edge(v2[2], v2[0]),
        ]
        if any(e in edges for e in t_edges):
            nbrs.append(t)
    return nbrs


def find_cavity(
    triangles: Set[Triangle], new_point: Point, container_triangle: Triangle
) -> Set[Triangle]:
    # Use a stack/queue to find all connected bad triangles
    bad_triangles = set([container_triangle])
    stack = [container_triangle]

    while stack:
        current = stack.pop()
        neighbors = find_triangle_neighbors(triangles, current)
        for nbr in neighbors:
            if nbr not in bad_triangles:
                if circumcircle_contains(nbr, new_point):
                    # found a bad triangle
                    print("Bad triangle found:", nbr)
                    bad_triangles.add(nbr)
                    stack.append(nbr)
    
    return bad_triangles

# simpler implementation of find_cavity
def find_cavity_simple(triangles: Set[Triangle], new_point: Point) -> Set[Triangle]:
    """
    Simpler implementation of find_cavity.
    Iterates through all triangles and checks if they are 'bad' (their circumcircle contains the new_point).
    """
    bad_triangles = set()
    for tri in triangles:
        if circumcircle_contains(tri, new_point):
            bad_triangles.add(tri)
            print("Bad triangle found:", tri)
    # how many bad triangles found
    print("Bad triangles found:", len(bad_triangles))
    print("-------------------")
    return bad_triangles


def delaunay_insert_point(
    triangles: Set[Triangle], all_points: List[Point], new_point: Point
) -> Set[Triangle]:

    highlight_new_point(new_point)

    # Find the triangle containing the new point (works)
    container_triangle = find_triangle_containing_point(triangles, new_point)
    if container_triangle is None:
        # If no containing triangle is found, return unchanged
        print("No containing triangle found")
        return triangles

    # Highlight the container triangle in green (for visualization)
    highlight_container_triangle(container_triangle)

    # Find the cavity (connected bad triangles) that need to be removed 
    bad_triangles = find_cavity(triangles, new_point, container_triangle)

    highlight_bad_triangles(bad_triangles)

    print("Amount triangles:", len(triangles))
    print("Amount bad triangles:", len(bad_triangles))
    # Remove the bad triangles from the triangulation
    remaining_triangles = triangles - bad_triangles
    
    # remove invalid triangles (triangles with duplicate points)
    remaining_triangles = {t for t in remaining_triangles if is_valid_triangle(t)}

    print(
        "Amount after removing bad triangles:",
        len(remaining_triangles),
    )
    print("-------------------")
    # remaining_triangles 
    for t in remaining_triangles:
        print(t)
    print("-------------------")
    
    # clear all the highlighted triangles
    canvas.delete("triangle_containing_point")
    canvas.delete("triangle")
    canvas.delete("bad_triangle")
    root.update()

    # Redraw only the remaining triangles in blue (clear previous)
    draw_triangles(remaining_triangles)

    # Determine the polygon hole formed by removing bad_triangles
    edge_count = {}

    def add_edge(a, b):
        e = tuple(sorted((a, b), key=lambda p: (p.x, p.y)))
        edge_count[e] = edge_count.get(e, 0) + 1

    # Count edges of all removed triangles
    for tri in bad_triangles:
        v = tri.vertices()
        add_edge(v[0], v[1])
        add_edge(v[1], v[2])
        add_edge(v[2], v[0])

    # Boundary edges are those that appear exactly once
    boundary_edges = [e for e, c in edge_count.items() if c == 1]

    # show the boundary edges on canvas
    for e in boundary_edges:
        canvas.create_line(
            e[0].x, e[0].y, e[1].x, e[1].y, fill="red", tags="boundary_edge", width=4
        )
    root.update()
    sleep(sleep_time_slider.get())

    if not boundary_edges:
        # No hole to fill (degenerate case)
        print("No hole to fill")
        return remaining_triangles

    # Reconstruct the polygon loop from boundary edges
    polygon = [boundary_edges[0][0], boundary_edges[0][1]]
    used = {boundary_edges[0]}
    
    # Iterate until all boundary edges are used
    while len(used) < len(boundary_edges):
        last_point = polygon[-1]
        found_next = False
        
        # Find the next edge that connects to the last point in the polygon
        for e in boundary_edges:
            if e in used:
                continue
            if e[0] == last_point:
                polygon.append(e[1])
                used.add(e)
                found_next = True
                break
            elif e[1] == last_point:
                polygon.append(e[0])
                used.add(e)
                found_next = True
                break
        
        # If no connecting edge is found, break (degenerate case)
        if not found_next:
            print("Could not form a closed polygon")
            break

    # Triangulate the hole by connecting new_point to the polygon edges
    for i in range(len(polygon)):
        p_current = polygon[i]
        p_next = polygon[(i + 1) % len(polygon)]
        new_tri = Triangle(new_point, p_current, p_next)
        remaining_triangles.add(new_tri)

    # remove the boundary edges
    canvas.delete("boundary_edge")
    canvas.delete("new_point_circle")

    # Redraw the final updated triangulation in blue
    canvas.delete("triangle")
    for t in remaining_triangles:
        canvas.create_polygon(
            [t.p1.x, t.p1.y, t.p2.x, t.p2.y, t.p3.x, t.p3.y],
            outline="blue",
            fill="",
            tags="triangle",
        )
    root.update()
    sleep(sleep_time_slider.get())
    # remaining triangles are the new triangulation triangles after inserting the new point and filling the hole
    return remaining_triangles

def highlight_bad_triangles(bad_triangles):
        # Highlight bad triangles in green
    for t in bad_triangles:
        canvas.create_polygon(
            [t.p1.x, t.p1.y, t.p2.x, t.p2.y, t.p3.x, t.p3.y],
            outline="lightgreen",
            fill="",
            tags="bad_triangle",
            width=4,
        )
    root.update()
    sleep(sleep_time_slider.get())

def highlight_new_point(new_point):
    # mark the new point with a circle around it
    canvas.create_oval(
        new_point.x - 5,
        new_point.y - 5,
        new_point.x + 5,
        new_point.y + 5,
        outline="orange",
        tags="new_point_circle",
        width=3,
    )
    root.update()
    sleep(sleep_time_slider.get())

def highlight_container_triangle(container_triangle):
    canvas.create_polygon(
        [
            container_triangle.p1.x,
            container_triangle.p1.y,
            container_triangle.p2.x,
            container_triangle.p2.y,
            container_triangle.p3.x,
            container_triangle.p3.y,
        ],
        outline="green",
        fill="",
        tags="triangle_containing_point",
        width=4,
    )
    root.update()
    sleep(sleep_time_slider.get())


def draw_hull(hull_points):
    canvas.delete("hull")
    for i in range(len(hull_points)):
        p1 = hull_points[i]
        p2 = hull_points[(i + 1) % len(hull_points)]
        canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill="red", tags="hull")
    root.update()
    sleep(sleep_time_slider.get())


def draw_triangles(triangles):
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
    sleep(sleep_time_slider.get())


def perform_delaunay():
    global points, canvas
    # Step 0: Check if there are enough points to perform triangulation
    if len(points) < 3:
        return

    # Step 1: Compute the convex hull using Graham's scan
    points_tuple = [(p.x, p.y) for p in points]
    hull = graham_scan(points_tuple)
    hull_points = [Point(h[0], h[1]) for h in hull]

    hull_set = set(hull_points)
    interior_points = [p for p in points if p not in hull_set]

    # Step 2: Visualize the convex hull
    draw_hull(hull_points)

    # Step 3: Initialize the set of triangles with the convex hull
    triangles: Set[Triangle] = set()
    if len(interior_points) == 0:
        if len(hull_points) < 3:
            return
        for i in range(1, len(hull_points) - 1):
            t = Triangle(hull_points[0], hull_points[i], hull_points[i + 1])
            triangles.add(t)
        # Visualize the final triangulation (just the hull)
        draw_triangles(triangles)
    else:
        # Step 4: Initialize the triangulation with the first interior point and the convex hull
        p1 = interior_points[0]
        for i in range(len(hull_points)):
            t = Triangle(p1, hull_points[i], hull_points[(i + 1) % len(hull_points)])
            triangles.add(t)
        # Show the initial triangulation after adding the first interior point
        draw_triangles(triangles)

        # Step 5: Insert the remaining interior points one by one with visualization after each insertion
        for i in range(1, len(interior_points)):
            print("-------------------")
            print("Iteration:", i)
            p_i = interior_points[i]
            triangles = delaunay_insert_point(triangles, points, p_i)
            print("End of iteration:", i)
            print("-------------------")
            # Visualize after inserting each point
            draw_triangles(triangles)


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
    from_=5,
    to=50,
    orient=tk.HORIZONTAL,
    label="Anzahl der Punkte",
    length=150,
)
point_count_slider.set(20)
point_count_slider.pack(pady=5)

sleep_time_slider = tk.Scale(
    sidebar,
    from_=0,
    to=2,
    resolution=0.1,
    orient=tk.HORIZONTAL,
    label="Schlafzeit (in Sekunden)",
    length=150,
)
sleep_time_slider.set(0.5)
sleep_time_slider.pack(pady=5)


canvas = tk.Canvas(root, bg="white")
canvas.grid(row=0, column=1, sticky="nsew")

points: List[Point] = []
point_objs = []


def clear_canvas():
    canvas.delete("all")
    del points[:]
    del point_objs[:]


def add_point(x, y):
    # Create the point
    p = Point(x, y)
    points.append(p)

    # Draw the point on the canvas
    obj = canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black", tags="point")
    point_objs.append((obj, p))

    # Draw the coordinates below the point
    text_obj = canvas.create_text(x, y + 10, text=f"({x}, {y})", font=("Arial", 8), fill="gray", tags="coordinates")
    point_objs.append((text_obj, p))

def on_canvas_click(event):
    add_point(event.x, event.y)

def generate_random_points():
    clear_canvas()
    n = point_count_slider.get()
    # Make sure canvas dimensions are available
    root.update_idletasks()
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    # generate from a normal distribution
    for _ in range(n):
        x = random.randint(5, width - 5)
        y = random.randint(5, height - 5)
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
