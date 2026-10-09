
import numpy as np
import matplotlib.pyplot as plt

# Original triangle in homogeneous coordinates
points = np.array([
    [1, 4, 2, 1],
    [1, 1, 4, 1],
    [1, 1, 1, 1]
], dtype=float)

def transformation_matrix():
    print("\n=== Pixel MatriX ===")
    print("1. Translation")
    print("2. Scaling")
    print("3. Rotation")
    print("4. Reflection")
    print("5. Shear")

    choice = input("Choose transformation (1-5): ")

    if choice == "1":
        tx = float(input("Move horizontally (tx): "))
        ty = float(input("Move vertically (ty): "))
        return np.array([
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ])

    elif choice == "2":
        sx = float(input("Scaling factor x: "))
        sy = float(input("Scaling factor y: "))
        return np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ])

    elif choice == "3":
        angle = float(input("Rotation angle in degrees: "))
        theta = np.radians(angle)
        return np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ])

    elif choice == "4":
        print("1. Reflect across x-axis")
        print("2. Reflect across y-axis")
        axis = input("Choose axis (1-2): ")

        if axis == "1":
            return np.diag([1, -1, 1])
        elif axis == "2":
            return np.diag([-1, 1, 1])
        else:
            print("Invalid axis.")
            return None

    elif choice == "5":
        shx = float(input("Horizontal shear factor: "))
        shy = float(input("Vertical shear factor: "))
        return np.array([
            [1, shx, 0],
            [shy, 1, 0],
            [0, 0, 1]
        ])

    print("Invalid choice.")
    return None


def main():
    matrix = transformation_matrix()

    if matrix is None:
        return

    # Apply the transformation to every vertex
    transformed = matrix @ points

    print("\nTransformation Matrix:")
    print(matrix)

    print("\nOriginal Coordinates:")
    print(points[:2].T)

    print("\nTransformed Coordinates:")
    print(transformed[:2].T)

    # Plot both shapes
    fig, ax = plt.subplots()

    ax.plot(
        *np.column_stack((points[0], points[1], points[0])),
        marker="o", label="Original"
    )
    ax.plot(
        *np.column_stack((
            transformed[0], transformed[1], transformed[0]
        )),
        marker="o", label="Transformed"
    )

    ax.axhline(0, color="black", linewidth=0.7)
    ax.axvline(0, color="black", linewidth=0.7)
    ax.grid(True)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("X coordinate")
    ax.set_ylabel("Y coordinate")
    ax.set_title("Pixel MatriX - Matrix Drawing Tool")
    ax.legend()

    plt.show()


if __name__ == "__main__":
    main()

