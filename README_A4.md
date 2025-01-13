# `circumcircle_contains` Function Explanation

This document explains how the `circumcircle_contains` function works. In short, it uses a classic determinant-based test from computational geometry to check whether a point \(p\) lies **inside** the circumcircle of a given triangle \((p_1, p_2, p_3)\).

---

## 1. Geometric Background

For a triangle with vertices \(A, B, C\), its **circumcircle** is the unique circle passing through all three vertices. Given an additional point \(P\) in the plane, you can determine if \(P\) is inside, on, or outside the circumcircle by evaluating the **sign** of a particular determinant of size (3 x 3):


M = $\begin{vmatrix}
(A_x - P_x) & (A_y - P_y) & (A_x^2 + A_y^2 - (P_x^2 + P_y^2))\\
(B_x - P_x) & (B_y - P_y) & (B_x^2 + B_y^2 - (P_x^2 + P_y^2)) \\
(C_x - P_x) & (C_y - P_y) & (C_x^2 + C_y^2 - (P_x^2 + P_y^2))
\end{vmatrix}$.

- If the determinant is **positive**, \(P\) is inside the circumcircle (assuming a consistent triangle orientation).
- If it is **zero**, \(P\) lies exactly on the circumcircle.
- If it is **negative**, \(P\) is outside the circumcircle.

> **Note on orientation:** If the triangle \((A, B, C)\) is oriented clockwise, this sign might be reversed. Usually, one ensures a **counterclockwise** orientation or simply checks the absolute value if the orientation isn’t consistent.

## 2 Python Implementation

```python
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
    det = A * (E * I - F * H) \
        - B * (D * I - F * G) \
        + C * (D * H - E * G)

    # Return True if the determinant is positive (point is inside the circumcircle)
    return det > epsilon
```

Each vertex coordinate 
𝐴𝑥, 𝐴𝑦 is replaced by 𝐴𝑥−𝑃𝑥 and 𝐴𝑦−𝑃𝑦. This is why you see:
```python
A = ax - dx
B = ay - dy
```
similarly for  𝐵  and  𝐶.

### 2.2 Quadratic Terms

The expression \((A_x^2 + A_y^2) - (P_x^2 + P_y^2)\) is expanded as:

```python
C = (ax**2 - dx**2) + (ay**2 - dy**2)
```

det = A * (E * I - F * H) \
      - B * (D * I - F * G) \
      + C * (D * H - E * G)