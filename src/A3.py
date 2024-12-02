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
        self.axis = axis      # Aktuelle Achse: 0 für x, 1 für y


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

# Slider für die Anzahl der Punkte
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

# Steuerungsmodus-Auswahl hinzufügen
control_mode_var = tk.StringVar(value='normal')

control_mode_label = tk.Label(sidebar, text="Steuerungsmodus:", bg='lightgray')
control_mode_label.pack(pady=(10, 0))

control_mode_frame = tk.Frame(sidebar, bg='lightgray')
control_mode_frame.pack(pady=5)

normal_control_radio = tk.Radiobutton(
    control_mode_frame, text="Normale Maussteuerung", variable=control_mode_var, value='normal', bg='lightgray')
normal_control_radio.pack(anchor='w')

touchpad_control_radio = tk.Radiobutton(
    control_mode_frame, text="Vereinfachte Touchpad-Steuerung", variable=control_mode_var, value='touchpad', bg='lightgray')
touchpad_control_radio.pack(anchor='w')

# Modusauswahl für Touchpad-Steuerung
mode_var = tk.StringVar(value='add')

mode_label = tk.Label(sidebar, text="Modus auswählen:", bg='lightgray')
mode_frame = tk.Frame(sidebar, bg='lightgray')

# Canvas zum Zeichnen erstellen
canvas = tk.Canvas(root, bg='white')
canvas.grid(row=0, column=1, sticky="nsew")

# Globale Variablen
points = []            # Liste aller Punkte
point_objs = []        # Liste der Canvas-Objekte der Punkte
root_node = None       # Wurzel des 2D-Baums
lines = []             # Liste der gezeichneten Partitionierungslinien
selected_point = None  # Zum Verschieben ausgewählter Punkt
search_rect_coords = []    # Koordinaten für den Suchbereich
found_points = []      # Gefundene Punkte im Suchbereich
search_rectangle = None  # Gezeichnetes Suchrechteck


def preprocessing(points):
    """Sortiert die Punkte nach x- und y-Koordinaten."""
    points_sorted_x = sorted(points, key=lambda point: (point.x, point.y))
    points_sorted_y = sorted(points, key=lambda point: (point.y, point.x))
    return points_sorted_x, points_sorted_y


def generate_points():
    """Erzeugt zufällige Punkte und zeichnet sie auf dem Canvas."""
    global points, point_objs
    clear_canvas()
    points.clear()
    point_objs.clear()
    num_points = point_count_slider.get()
    for _ in range(num_points):
        x = random.randint(10, canvas.winfo_width() - 10)
        y = random.randint(10, canvas.winfo_height() - 10)
        point = Point(x, y)
        points.append(point)
        obj = canvas.create_oval(
            x-3, y-3, x+3, y+3, fill='black', tags='point')
        point_objs.append((obj, point))
    build_tree_and_draw()


def clear_canvas():
    """Löscht alle Elemente vom Canvas."""
    canvas.delete("all")
    lines.clear()


def canvas_click(event):
    """Verarbeitet Klicks auf dem Canvas basierend auf dem ausgewählten Modus."""
    if control_mode_var.get() == 'touchpad':
        touchpad_canvas_click(event)
    else:
        normal_canvas_click(event)


def touchpad_canvas_click(event):
    """Klickverarbeitung im Touchpad-Modus."""
    mode = mode_var.get()
    x, y = event.x, event.y

    if mode == 'add':
        add_point(x, y)
    elif mode == 'move':
        move_point_click(x, y)
    elif mode == 'range':
        range_selection_click(x, y)


def normal_canvas_click(event):
    """Klickverarbeitung im normalen Modus."""
    x, y = event.x, event.y
    add_point(x, y)


def add_point(x, y):
    """Fügt einen Punkt hinzu."""
    point = Point(x, y)
    points.append(point)
    obj = canvas.create_oval(x-3, y-3, x+3, y+3, fill='black', tags='point')
    point_objs.append((obj, point))
    build_tree_and_draw()


def move_point_click(x, y):
    """Verarbeitet Klicks im Verschiebemodus."""
    global selected_point

    if selected_point is None:
        # Überprüfen, ob ein Punkt angeklickt wurde
        for obj, point in point_objs:
            coords = canvas.coords(obj)
            if coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]:
                selected_point = (obj, point)
                # Punkt hervorheben
                canvas.itemconfig(obj, outline='green', width=2)
                break
    else:
        # Punkt an neue Position bewegen
        obj, point = selected_point
        canvas.coords(obj, x-3, y-3, x+3, y+3)
        point.x = x
        point.y = y
        # Hervorhebung entfernen
        canvas.itemconfig(obj, outline='', width=1)
        selected_point = None
        build_tree_and_draw()


def range_selection_click(x, y):
    """Verarbeitet Klicks im Bereichssuchmodus."""
    global search_rect_coords, search_rectangle

    if len(search_rect_coords) == 0:
        # Erster Klick - erste Ecke speichern
        search_rect_coords = [x, y]
        # Vorheriges Suchrechteck entfernen
        if search_rectangle:
            canvas.delete(search_rectangle)
            search_rectangle = None
    else:
        # Zweiter Klick - zweite Ecke speichern und Suche durchführen
        search_rect_coords.extend([x, y])
        x0, y0, x1, y1 = search_rect_coords
        # Suchrechteck zeichnen
        search_rectangle = canvas.create_rectangle(
            x0, y0, x1, y1, outline='green', dash=(2, 2))
        perform_range_search(min(x0, x1), min(
            y0, y1), max(x0, x1), max(y0, y1))
        # Koordinaten zurücksetzen
        search_rect_coords = []


def build_tree_and_draw():
    """Erstellt den 2D-Baum und zeichnet die Partitionierung."""
    global root_node
    if not points:
        return
    points_sorted_x, points_sorted_y = preprocessing(points)
    root_node = construct_balanced_2d_tree(
        points_sorted_x, points_sorted_y, depth=0)
    clear_partition_lines()
    draw_partition(root_node, 0, 0, 0, canvas.winfo_width(),
                   canvas.winfo_height())


def construct_balanced_2d_tree(points_sorted_x, points_sorted_y, depth):
    """Konstruiert rekursiv einen balancierten 2D-Baum mit zusätzlichen Überprüfungen."""
    if not points_sorted_x or not points_sorted_y:
        return None

    if len(points_sorted_x) == 1:
        return Node(point=points_sorted_x[0], axis=depth % 2)

    axis = depth % 2  # 0 für x, 1 für y

    if axis == 0:  # x-Achse
        median = len(points_sorted_x) // 2
        median_point = points_sorted_x[median]
        left_points_x = points_sorted_x[:median]
        right_points_x = points_sorted_x[median+1:]

        # Filtern der Punkte für die y-sortierte Liste
        left_points_y = [
            point for point in points_sorted_y if point.x < median_point.x]
        right_points_y = [
            point for point in points_sorted_y if point.x > median_point.x]

    # axis == 1 (y-Achse)
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

    # Abbruchbedingung: Keine Punkte mehr übrig
    if not left_points_x and not right_points_x:
        return Node(point=median_point, axis=axis)

    # Erstellen des Knotens mit dem Medianpunkt und der aktuellen Achse
    node = Node(
        point=median_point,
        axis=axis
    )
    # Rekursiver Aufruf für linke und rechte Teilbäume mit den gefilterten Punktmengen
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
                canvas.itemconfig(obj, fill='magenta')


def range_search(node, x_min, y_min, x_max, y_max):
    """Rekursiver Bereichssuchalgorithmus."""
    if node is None:
        return

    x = node.point.x
    y = node.point.y

    # Wenn der Punkt im Suchbereich liegt, hinzufügen
    if x_min <= x <= x_max and y_min <= y <= y_max:
        found_points.append(node.point)

    axis = node.axis

    if axis == 0:  # Überprüfen ob Punkt im Suchbereich liegt (x-Achse)
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


def on_point_press(event):
    """Startet das Verschieben eines Punktes im normalen Modus."""
    global selected_point
    x, y = event.x, event.y
    for obj, point in point_objs:
        coords = canvas.coords(obj)
        if coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]:
            selected_point = (obj, point)
            break


def on_point_move(event):
    """Verschiebt den ausgewählten Punkt im normalen Modus."""
    global selected_point
    if selected_point is not None:
        obj, point = selected_point
        x, y = event.x, event.y
        canvas.coords(obj, x-3, y-3, x+3, y+3)
        point.x = x
        point.y = y
        build_tree_and_draw()


def on_point_release(event):
    """Beendet das Verschieben eines Punktes im normalen Modus."""
    global selected_point
    selected_point = None


def start_range_selection(event):
    """Startet die Auswahl eines Suchbereichs im normalen Modus."""
    global search_rect_coords, search_rectangle
    search_rect_coords = [event.x, event.y]
    if search_rectangle:
        canvas.delete(search_rectangle)
        search_rectangle = None


def update_range_selection(event):
    """Aktualisiert die Darstellung des Suchbereichs während der Auswahl im normalen Modus."""
    global search_rect_coords, search_rectangle
    x0, y0 = search_rect_coords
    x1, y1 = event.x, event.y
    if search_rectangle:
        canvas.delete(search_rectangle)
    search_rectangle = canvas.create_rectangle(
        x0, y0, x1, y1, outline='green', dash=(2, 2))
    perform_range_search(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))


def end_range_selection(event):
    """Beendet die Auswahl des Suchbereichs im normalen Modus."""
    global search_rect_coords
    search_rect_coords = []


def update_control_mode(*args):
    """Aktualisiert die Ereignisbindungen basierend auf dem Steuerungsmodus."""
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    canvas.unbind("<Button-3>")
    canvas.unbind("<B3-Motion>")
    canvas.unbind("<ButtonRelease-3>")

    if control_mode_var.get() == 'touchpad':
        # Touchpad-Steuerung
        mode_label.pack(pady=(10, 0))
        mode_frame.pack(pady=5)
        canvas.bind("<Button-1>", canvas_click)
    else:
        # Normale Maussteuerung
        mode_label.pack_forget()
        mode_frame.pack_forget()
        canvas.bind("<Button-1>", on_point_press)
        canvas.bind("<B1-Motion>", on_point_move)
        canvas.bind("<ButtonRelease-1>", on_point_release)
        canvas.bind("<Button-3>", start_range_selection)
        canvas.bind("<B3-Motion>", update_range_selection)
        canvas.bind("<ButtonRelease-3>", end_range_selection)


# Steuerungsmodus-Auswahl aktualisieren
control_mode_var.trace_add('write', update_control_mode)
update_control_mode()

# Modusauswahl für Touchpad-Steuerung hinzufügen
add_radio = tk.Radiobutton(
    mode_frame, text="Punkte hinzufügen", variable=mode_var, value='add', bg='lightgray')
add_radio.pack(anchor='w')

# Verschiebemodus hinzufügen
move_radio = tk.Radiobutton(
    mode_frame, text="Punkte verschieben", variable=mode_var, value='move', bg='lightgray')
move_radio.pack(anchor='w')

# Bereichssuche-Modus hinzufügen
range_radio = tk.Radiobutton(
    mode_frame, text="Bereichssuche", variable=mode_var, value='range', bg='lightgray')
range_radio.pack(anchor='w')

# Buttons in der Seitenleiste
generate_button = tk.Button(
    sidebar, text="Zufällige Punkte erzeugen", command=generate_points)
generate_button.pack(pady=5)

# Punkte löschen Button (alle Punkte)
clear_button = tk.Button(
    sidebar, text="Punkte löschen", command=lambda: [points.clear(), point_objs.clear(), clear_canvas()])
clear_button.pack(pady=5)

# Hauptschleife starten
root.mainloop()
