import tkinter as tk
import random
from dataclasses import dataclass


@dataclass
class Point:
    """Repräsentiert einen Punkt mit x- und y-Koordinaten."""
    x: int
    y: int


@dataclass
class Node:
    """Knotenklasse für den 2D-Baum."""

    def __init__(self, point=None, left=None, right=None, axis=0):
        self.point = point    # Punkt an diesem Knoten
        self.left = left      # Linker Teilbaum
        self.right = right    # Rechter Teilbaum
        self.axis = axis      # Aktuelle Achse: 0 für x, 1 für y


root = tk.Tk()
root.title("Interactive construction of a 2D-Tree")

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
    sidebar, text="Tree construction", font=("Arial", 18), bg='lightgray', fg='black')
heading_text.pack(pady=5)

# Create a canvas for drawing points
canvas = tk.Canvas(root, bg='white')
canvas.grid(row=0, column=1, sticky="nsew")

# List to hold all initial Points
points = []
points_sorted_x = []
points_sorted_y = []
# Hauptfenster erstellen
root = tk.Tk()
root.title("Interaktive Konstruktion eines 2D-Baums")

# Fenstergröße festlegen
root.geometry("1000x800")

# Grid-Layout konfigurieren (2 Spalten, 1 Zeile)
root.grid_columnconfigure(0, weight=0)  # Seitenleiste
root.grid_columnconfigure(1, weight=1)  # Canvas
root.grid_rowconfigure(0, weight=1)     # Zeile dehnt sich vertikal aus

# Seitenleiste erstellen
sidebar = tk.Frame(root, width=200, bg='lightgray', padx=10, pady=10)
sidebar.grid(row=0, column=0, sticky="ns")

# Überschrift in der Seitenleiste
heading_text = tk.Label(
    sidebar, text="2D-Baum Konstruktion", font=("Arial", 18), bg='lightgray', fg='black')
heading_text.pack(pady=5)

# Canvas zum Zeichnen erstellen
canvas = tk.Canvas(root, bg='white')
canvas.grid(row=0, column=1, sticky="nsew")

# Globale Variablen
points = []            # Liste aller Punkte
point_objs = []        # Liste der Canvas-Objekte der Punkte
root_node = None       # Wurzel des 2D-Baums
lines = []             # Liste der gezeichneten Partitionierungslinien
selected_point = None  # Zum Verschieben ausgewählter Punkt
search_rect = None     # Suchrechteck
found_points = []      # Gefundene Punkte im Suchbereich
search_rectangle = None  # Gezeichnetes Suchrechteck


def preprocessing(points):
    """ Sortiert die Punkte nach x- und y-Koordinate.
    Args:
        points: Liste von Punkten
    Returns:
        points_sorted_x: Liste von Punkten sortiert nach x-Koordinate
        points_sorted_y: Liste von Punkten sortiert nach y-Koordinate
    """
    # Sort points by x
    points_sorted_x = sorted(points, key=lambda point: point.x)
    # Sort points by y
    points_sorted_y = sorted(points, key=lambda point: point.y)
    return points_sorted_x, points_sorted_y


# Function to generate 100 random points on the canvas
def generate_points():
    # Clear the canvas
    canvas.delete("all")

    for _ in range(100):
        x = random.randint(0, canvas.winfo_width())
        y = random.randint(0, canvas.winfo_height())
        points.append(Point(x, y))
        # Draw the point on the canvas
        canvas.create_oval(x-3, y-3, x+3, y+3, fill='black')
    return points


# Function to create a point at the clicked location
def create_point(event):
    x, y = event.x, event.y
    canvas.create_oval(x-3, y-3, x+3, y+3, fill='black')


# Function to create the kd tree
def ConstructBalanced2DTree(index_left, index_right, knot, direction):

    pass


# Bind the left mouse button click event to the create_point function
canvas.bind("<Button-1>", create_point)

generate_button = tk.Button(
    sidebar, text="Generate random points", command=generate_points)
generate_button.pack(pady=5)

root.mainloop()
