import numpy as np

class Edge:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        self.next_edge = None
        self.prev_edge = None
        self.symmetric = None
        self.metadata = None  # Marks deleted edges

    def __str__(self):
        desc = f"{self.origin} -> {self.destination}"
        if self.metadata is None:
            return desc
        else:
            return f"{desc} (deleted)"

class DelaunayTriangulation:
    def __init__(self):
        self.edge_list = []  # Stores 

    def delaunay_recursion(self, points):
        if len(points) < 2:
            raise ValueError("At least two points are required AZIZAM.")
        
        self.edge_list = []
        points = np.asarray(points, dtype=np.float64)
        points.view(dtype=[('f0', points.dtype), ('f1', points.dtype)]).sort(order=['f0', 'f1'], axis=0)

        # duplicate points
        unique_points = np.unique(points, axis=0)
        if len(unique_points) != len(points):
            points = unique_points

        self._recursive_triangulation(points)
        
        # Remove edges marked as deleted
        self.edge_list = [edge for edge in self.edge_list if edge.metadata is None]
        return self.edge_list

    def _recursive_triangulation(self, points):
        if len(points) == 2:
            edge = self._create_edge(points[0], points[1])
            return edge, edge.symmetric

        if len(points) == 3:
            a, b, c = points
            edge1 = self._create_edge(a, b)
            edge2 = self._create_edge(b, c)
            self._link_edges(edge1.symmetric, edge2)

            if self._is_right_of(c, edge1):
                self._create_connection(edge2, edge1)
                return edge1, edge2.symmetric
            elif self._is_left_of(c, edge1):
                edge3 = self._create_connection(edge2, edge1)
                return edge3.symmetric, edge3
            else:
                return edge1, edge2.symmetric

        mid = len(points) // 2
        left_out, left_in = self._recursive_triangulation(points[:mid])
        right_in, right_out = self._recursive_triangulation(points[mid:])

        while True:
            if self._is_right_of(right_in.origin, left_in):
                left_in = left_in.symmetric.next_edge
            elif self._is_left_of(left_in.origin, right_in):
                right_in = right_in.symmetric.prev_edge
            else:
                break

        base = self._create_connection(left_in.symmetric, right_in)

        if np.array_equal(left_in.origin, left_out.origin):
            left_out = base
        if np.array_equal(right_in.origin, right_out.origin):
            right_out = base.symmetric

        while True:
            right_candidate = base.symmetric.next_edge
            left_candidate = base.prev_edge
            validate_right = self._is_right_of(right_candidate.destination, base)
            validate_left = self._is_right_of(left_candidate.destination, base)

            if not validate_right and not validate_left:
                break

            if validate_right:
                while self._is_right_of(right_candidate.next_edge.destination, base) and \
                        self._circle_check(base.destination, base.origin, right_candidate.destination, right_candidate.next_edge.destination):
                    temp = right_candidate.next_edge
                    self._remove_edge(right_candidate)
                    right_candidate = temp

            if validate_left:
                while self._is_right_of(left_candidate.prev_edge.destination, base) and \
                        self._circle_check(base.destination, base.origin, left_candidate.destination, left_candidate.prev_edge.destination):
                    temp = left_candidate.prev_edge
                    self._remove_edge(left_candidate)
                    left_candidate = temp

            if not validate_right or \
                    (validate_left and self._circle_check(right_candidate.destination, right_candidate.origin, left_candidate.origin, left_candidate.destination)):
                base = self._create_connection(left_candidate, base.symmetric)
            else:
                base = self._create_connection(base.symmetric, right_candidate.symmetric)

        return left_out, right_out

    def _create_edge(self, origin, destination):
        edge1 = Edge(origin, destination)
        edge2 = Edge(destination, origin)
        edge1.symmetric, edge2.symmetric = edge2, edge1
        edge1.next_edge, edge1.prev_edge = edge1, edge1
        edge2.next_edge, edge2.prev_edge = edge2, edge2
        self.edge_list.append(edge1)
        return edge1

    def _link_edges(self, edge_a, edge_b):
        edge_a.next_edge.prev_edge = edge_b
        edge_b.next_edge.prev_edge = edge_a
        edge_a.next_edge, edge_b.next_edge = edge_b.next_edge, edge_a.next_edge

    def _create_connection(self, edge_a, edge_b):
        new_edge = self._create_edge(edge_a.destination, edge_b.origin)
        self._link_edges(new_edge, edge_a.symmetric.prev_edge)
        self._link_edges(new_edge.symmetric, edge_b)
        return new_edge

    def _remove_edge(self, edge):
        self._link_edges(edge, edge.prev_edge)
        self._link_edges(edge.symmetric, edge.symmetric.prev_edge)
        edge.metadata = edge.symmetric.metadata = True

    def _is_right_of(self, point, edge):
        return self._calculate_determinant(edge.origin, edge.destination, point) > 0

    def _is_left_of(self, point, edge):
        return self._calculate_determinant(edge.origin, edge.destination, point) < 0

    def _calculate_determinant(self, a, b, p):
        return (a[0] - p[0]) * (b[1] - p[1]) - (a[1] - p[1]) * (b[0] - p[0])

    def _circle_check(self, a, b, c, d):
        dx_a, dy_a = a[0] - d[0], a[1] - d[1]
        dx_b, dy_b = b[0] - d[0], b[1] - d[1]
        dx_c, dy_c = c[0] - d[0], c[1] - d[1]
        sq_a, sq_b, sq_c = dx_a**2 + dy_a**2, dx_b**2 + dy_b**2, dx_c**2 + dy_c**2
        determinant = (dx_a * dy_b * sq_c + dy_a * sq_b * dx_c + sq_a * dx_b * dy_c -
                       (sq_a * dy_b * dx_c + dx_a * sq_b * dy_c + dy_a * dx_b * sq_c))
        return determinant < 0

def main():
    print("Enter points as [(x1, y1), (x2, y2), ...]:")
    try:
        user_input = input()
        points = eval(user_input)
        if not isinstance(points, list) or not all(isinstance(p, (tuple, list)) and len(p) == 2 for p in points):
            raise ValueError("Input must be a list of tuples or lists, each containing exactly two numerical values.")

        triangulation = DelaunayTriangulation()
        edges = triangulation.delaunay_recursion(points)

        if not edges:
            print("No edges for you today!")
        else:
            print("Delaunay triangulation edges:")
            for edge in edges:
                print(edge)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
