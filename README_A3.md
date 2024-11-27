# Aufgabe 1: Interaktive Konstruktion eines 2D-Baums vorgehen

1.  Eingabe: Erfassen Sie eine Menge von Punkten in der Ebene. Dies kann interaktiv durch Mausklicks des Benutzers oder durch Einlesen aus einer Datei erfolgen.
2.  Erstellen Sie den 2D-Baum:

- Verwenden Sie den Algorithmus ConstructBalanced2DTree aus der Vorlesung, um einen balancierten 2D-Baum aus den Eingabepunkten zu erstellen.

  - Partitionierung: Der Algorithmus partitioniert die Punkte rekursiv an ihrem Median, abwechselnd entlang der x- und y-Achse.

  - Ausgeglichenheit: Die Partitionierung am Median garantiert die Ausgeglichenheit des Baumes und verhindert eine lineare Laufzeit.

3. Visualisieren Sie die Partitionierung:

- Zeigen Sie die Punkte und die durch den 2D-Baum definierten Trennlinien an.

- Trennlinien: Die Trennlinien verlaufen vertikal oder horizontal durch die Medianpunkte und teilen die Ebene in rechteckige Regionen.
- Interaktivität: Ermöglichen Sie dem Benutzer, die Punkte zu verschieben und die resultierende Änderung der Partitionierung zu beobachten.

# Aufgabe 2: Interaktive Bereichssuche

1. Eingabe: Erfassen Sie einen rechteckigen Suchbereich interaktiv, z.B. durch Ziehen mit der Maus.
2. Führen Sie die Bereichssuche im 2D-Baum durch: Verwenden Sie den Algorithmus RangeSearch aus den Quellen, um alle Punkte im Suchbereich zu finden.

- Rekursive Suche: Der Algorithmus durchläuft den Baum rekursiv und überprüft, ob sich Punkte oder Teilbäume innerhalb des Suchbereichs befinden.
- Abbruchbedingung: Die Suche wird abgebrochen, wenn ein Knoten außerhalb des Suchbereichs liegt oder ein Blatt erreicht wird.
  3 Visualisieren Sie das Ergebnis: Markieren Sie die Punkte, die innerhalb des Suchbereichs liegen.
- Hervorhebung: Die gefundenen Punkte können z.B. in einer anderen Farbe dargestellt werden.
- Interaktivität: Ermöglichen des Benutzers, den Suchbereich zu ändern und die resultierende Änderung der Suchergebnisse zu beobachten.
