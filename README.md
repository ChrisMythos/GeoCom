# GeoCom

Excercises for Lecture Computational Geometry with Prof. Georg Umlauf

## How the Algorithm and Visualization Work for Graham's Scan:

1. Sort Points: Points are sorted from left to right.

2. Construct Lower Hull:

   - Start with an empty lower list.
   - Iterate over the sorted points.
   - For each point p:
     - Remove the last point from lower if adding p would make a non-left turn (clockwise).
     - Add p to lower.
   - Visualization:
     Draw the scan line at p[0].
     Update the partial hull.

3. Construct Upper Hull:

   - Repeat the process for the upper hull, but iterate over the points in reverse order.

4. Combine Hulls:

   - Concatenate lower and upper (excluding the last point of each to avoid duplication) to get the full convex hull.

5. Final Visualization:

   - Draw the complete convex hull in red.
   - Remove the scan line.
