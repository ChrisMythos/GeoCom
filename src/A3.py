import tkinter as tk
import random
from dataclasses import dataclass


@dataclass
class Point:
    """Repräsentiert einen Punkt mit x- und y-Koordinaten."""
    x: int
    y: int


class Node:
    """Knotenklasse für den 2D-Baum."""

    def __init__(self, point=None, left=None, right=None, axis=0):
        self.point = point    # Punkt an diesem Knoten
        self.left = left      # Linker Teilbaum
        self.right = right    # Rechter Teilbaum
        # Aktuelle Achse: 0 für x, 1 für y (direction aus Vorlesung)
        self.axis = axis


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
    """Sortiert die Punkte nach x- und y-Koordinaten."""
    points_sorted_x = sorted(points, key=lambda point: point.x)
    points_sorted_y = sorted(points, key=lambda point: point.y)
    return points_sorted_x, points_sorted_y


def generate_points():
    """Erzeugt zufällige Punkte und zeichnet sie auf dem Canvas."""
    global points, point_objs
    clear_canvas()
    points.clear()
    point_objs.clear()
    num_points = point_count_slider.get()
    for _ in range(num_points):
        x = random.randint(50, canvas.winfo_width() - 50)
        y = random.randint(50, canvas.winfo_height() - 50)
        point = Point(x, y)
        points.append(point)
        obj = canvas.create_oval(x-3, y-3, x+3, y+3, fill='black')
        point_objs.append((obj, point))
    build_tree_and_draw()


def clear_canvas():
    """Löscht alle Elemente vom Canvas."""
    canvas.delete("all")
    lines.clear()


def create_point(event):
    """Erstellt einen Punkt an der geklickten Position."""
    x, y = event.x, event.y
    point = Point(x, y)
    points.append(point)
    obj = canvas.create_oval(x-3, y-3, x+3, y+3, fill='black')
    point_objs.append((obj, point))
    build_tree_and_draw()


def build_tree_and_draw():
    """Erstellt den 2D-Baum und zeichnet die Partitionierung."""
    global root_node
    # wenn keine Punkte vorhanden sind, wird der Baum nicht erstellt
    if not points:
        return
    # Punkte sortieren (preprocessing)
    points_sorted_x, points_sorted_y = preprocessing(points)
    # Baum erstellen
    root_node = construct_balanced_2d_tree(
        points_sorted_x, points_sorted_y, depth=0)

    clear_partition_lines()
    draw_partition(root_node, 0, 0, 0, canvas.winfo_width(),
                   canvas.winfo_height())


def construct_balanced_2d_tree(points_sorted_x, points_sorted_y, depth):
    """Konstruiert rekursiv einen balancierten 2D-Baum."""
    # Abbruchbedingung: Leere Liste
    if not points_sorted_x or not points_sorted_y:
        return None

    # Achse für die Partitionierung (x oder y im Wechsel)
    axis = depth % 2  # 0 für x, 1 für y

    # Medianpunkt und Aufteilung der Punkte in x Richtung
    if axis == 0:
        median = len(points_sorted_x) // 2
        median_point = points_sorted_x[median]

        # Erstellen der linken und rechten Teilpunkte
        left_points_x = points_sorted_x[:median]
        right_points_x = points_sorted_x[median+1:]

        # Filtern der Punkte für die y-sortierte Liste
        left_points_y = [
            point for point in points_sorted_y if point.x < median_point.x]
        right_points_y = [
            point for point in points_sorted_y if point.x > median_point.x]

    # Medianpunkt und Aufteilung der Punkte in y Richtung
    else:
        median = len(points_sorted_y) // 2
        median_point = points_sorted_y[median]
        left_points_y = points_sorted_y[:median]
        right_points_y = points_sorted_y[median+1:]

        # Filtern der Punkte für die x-sortierte Liste
        left_points_x = [
            point for point in points_sorted_x if point.y < median_point.y]
        right_points_x = [
            point for point in points_sorted_x if point.y > median_point.y]

    # Neuer Knoten mit dem Medianpunkt
    node = Node(
        point=median_point,
        axis=axis
    )
    # Rekursiver Aufruf für linke und rechte Teilbäume
    node.left = construct_balanced_2d_tree(
        left_points_x, left_points_y, depth + 1)
    node.right = construct_balanced_2d_tree(
        right_points_x, right_points_y, depth + 1)

    return node


def draw_partition(node, depth, x_min, y_min, x_max, y_max):
    """Zeichnet die Partitionierungslinien des 2D-Baums."""
    if node is None:
        return

    x = node.point.x
    y = node.point.y

    if node.axis == 0:
        # Vertikale Linie
        line = canvas.create_line(x, y_min, x, y_max, fill='red')
        lines.append(line)
        draw_partition(node.left, depth+1, x_min, y_min, x, y_max)
        draw_partition(node.right, depth+1, x, y_min, x_max, y_max)
    else:
        # Horizontale Linie
        line = canvas.create_line(x_min, y, x_max, y, fill='blue')
        lines.append(line)
        draw_partition(node.left, depth+1, x_min, y_min, x_max, y)
        draw_partition(node.right, depth+1, x_min, y, x_max, y_max)


def clear_partition_lines():
    """Löscht alle Partitionierungslinien vom Canvas."""
    for line in lines:
        canvas.delete(line)
    lines.clear()


def on_point_click(event):
    """Wird aufgerufen, wenn auf einen Punkt geklickt wird (zum Verschieben)."""
    global selected_point
    x, y = event.x, event.y
    for obj, point in point_objs:
        coords = canvas.coords(obj)
        if coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]:
            selected_point = (obj, point)
            break


def on_point_move(event):
    """Verschiebt den ausgewählten Punkt."""
    global selected_point
    if selected_point is not None:
        obj, point = selected_point
        x, y = event.x, event.y
        canvas.coords(obj, x-3, y-3, x+3, y+3)
        point.x = x
        point.y = y
        build_tree_and_draw()


def on_point_release(event):
    """Setzt den ausgewählten Punkt zurück."""
    global selected_point
    selected_point = None


def start_range_selection(event):
    """Startet die Auswahl eines Suchbereichs."""
    global search_rect, search_rectangle
    search_rect = (event.x, event.y)
    if search_rectangle:
        canvas.delete(search_rectangle)
        search_rectangle = None


def update_range_selection(event):
    """Aktualisiert die Darstellung des Suchbereichs während der Auswahl."""
    global search_rect, search_rectangle
    if search_rect:
        x0, y0 = search_rect
        x1, y1 = event.x, event.y
        if search_rectangle:
            canvas.delete(search_rectangle)
        search_rectangle = canvas.create_rectangle(
            x0, y0, x1, y1, outline='green', dash=(2, 2))
        perform_range_search(min(x0, x1), min(
            y0, y1), max(x0, x1), max(y0, y1))


def end_range_selection(event):
    """Beendet die Auswahl des Suchbereichs."""
    global search_rect
    search_rect = None


def perform_range_search(x_min, y_min, x_max, y_max):
    """Führt die Bereichssuche im 2D-Baum durch."""
    global found_points
    # Vorherige Markierungen entfernen
    for obj, point in point_objs:
        canvas.itemconfig(obj, fill='black')
    found_points.clear()
    # Suche starten
    range_search(root_node, x_min, y_min, x_max, y_max)
    # Gefundene Punkte markieren
    for point in found_points:
        for obj, p in point_objs:
            if p == point:
                canvas.itemconfig(obj, fill='orange')


def range_search(node, x_min, y_min, x_max, y_max):
    """Rekursiver Bereichssuchalgorithmus."""
    if node is None:
        return

    x = node.point.x
    y = node.point.y

    if x_min <= x <= x_max and y_min <= y <= y_max:
        found_points.append(node.point)

    axis = node.axis

    if axis == 0:
        # x-Achse
        if x_min <= x:
            range_search(node.left, x_min, y_min, x_max, y_max)
        if x <= x_max:
            range_search(node.right, x_min, y_min, x_max, y_max)
    else:
        # y-Achse
        if y_min <= y:
            range_search(node.left, x_min, y_min, x_max, y_max)
        if y <= y_max:
            range_search(node.right, x_min, y_min, x_max, y_max)


# Ereignisse binden
canvas.bind("<Button-1>", create_point)  # Punkt hinzufügen
# Punkt anklicken zum Verschieben
canvas.tag_bind("point", "<Button-1>", on_point_click)
canvas.bind("<B1-Motion>", on_point_move)  # Punkt verschieben
canvas.bind("<ButtonRelease-1>", on_point_release)  # Verschieben beenden

# Rechte Maustaste zum Starten der Bereichsauswahl
canvas.bind("<Button-3>", start_range_selection)
# Bereichsauswahl aktualisieren
canvas.bind("<B3-Motion>", update_range_selection)
# Bereichsauswahl beenden
canvas.bind("<ButtonRelease-3>", end_range_selection)


# Buttons in der Seitenleiste
generate_button = tk.Button(
    sidebar, text="Zufällige Punkte erzeugen", command=generate_points)
generate_button.pack(pady=5)

clear_button = tk.Button(
    sidebar, text="Punkte löschen", command=lambda: [points.clear(), point_objs.clear(), clear_canvas()])
clear_button.pack(pady=5)

# Schieberegler für die Anzahl der Punkte
point_count_slider = tk.Scale(
    sidebar,
    from_=10,
    to=1000,
    orient=tk.HORIZONTAL,
    label='Anzahl der Punkte',
    length=150
)
point_count_slider.set(20)  # Standardwert setzen
point_count_slider.pack(pady=5)


# Hauptschleife starten
root.mainloop()
