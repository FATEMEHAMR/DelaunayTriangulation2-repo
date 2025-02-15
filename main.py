from delaunay import delaunay_recursion

def main():
    print("Enter points e.g., [(x1, y1), (x2, y2), ...]:")
    try:
        user_input = input()
        points = eval(user_input)  # Convert string input to a Python list
        if not isinstance(points, list) or not all(isinstance(p, (tuple, list)) and len(p) == 2 for p in points):
            raise ValueError("Wrong input.")

        edges = delaunay_recursion(points)
        if edges is None:
            print("No triangulation could be formed.")
        else:
            print("Delaunay triangulation edges:")
            for edge in edges:
                print(f"{edge.origin} -> {edge.destination }")
    except Exception as e:
        print(f"Invalid input: {e}")

if __name__ == "__main__":
    main()
