# Delaunay Triangulation 2


The goal of this project is to implement the **Divide and Conquer** algorithm using **Delaunay Triangulation**. The purpose of this project is to implement Delaunay Triangulation using the divide-and-conquer algorithm. The initial set of points is divided into two smaller sections, and triangles are created in each section. Then, the triangulation algorithm is applied to each section separately, and continuous and complete triangulation for the entire set of points is achieved. This method is efficient due to the reduction in problem size at each stage, optimizing performance and increasing the speed of calculations for large sets of points.


# Input and Output

We can assume the input is given as an array of points in the form of 2D coordinates. For example, the input could be:

**Input:**  
`[(5, 4), (3, 2), (2, 1)]`

---

# Output

The output will consist of the edges (or sides) between these points. In this case, since there are only three points, the output will contain just one triangle formed by the three points.

**Output:**  
`[((5, 4), (2, 1)), ((5, 4), (3, 2)), ((3, 2), (2, 1))]`

This output indicates that the three points are connected with three edges, forming one triangle.
