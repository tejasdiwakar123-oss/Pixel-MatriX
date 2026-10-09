
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PixelMatriX:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel MatriX | Matrix Drawing Tool")
        self.root.geometry("1100x720")
        self.root.minsize(900, 600)

        # Triangle vertices in homogeneous coordinates
        self.original = np.array([
            [1, 4, 2],
            [1, 1, 4],
            [1, 1, 1]
        ], dtype=float)

        self.transformed = self.original.copy()

        title = ttk.Label(
            root, text="Pixel MatriX",
            font=("Segoe UI", 22, "bold")
        )
        title.pack(pady=(12, 2))

        ttk.Label(
            root,
            text="Explore 2D shapes using linear algebra",
            font=("Segoe UI", 10)
        ).pack(pady=(0, 12))

        body = ttk.Frame(root, padding=12)
        body.pack(fill="both", expand=True)

        controls = ttk.LabelFrame(
            body, text="Transformation Controls", padding=12
        )
        controls.pack(side="left", fill="y", padx=(0, 12))

        self.operation = tk.StringVar(value="Translation")

        ttk.Label(controls, text="Choose operation").pack(anchor="w")

        self.operation_box = ttk.Combobox(
            controls,
            textvariable=self.operation,
            values=[
                "Translation", "Scaling", "Rotation",
                "Reflection X", "Reflection Y", "Shear"
            ],
            state="readonly",
            width=20
        )
        self.operation_box.pack(fill="x", pady=(4, 12))
        self.operation_box.bind(
            "<<ComboboxSelected>>", self.update_labels
        )

        self.x_label = ttk.Label(controls, text="X value / tx")
        self.x_label.pack(anchor="w")
        self.x_value = ttk.Entry(controls)
        self.x_value.insert(0, "2")
        self.x_value.pack(fill="x", pady=(3, 10))

        self.y_label = ttk.Label(controls, text="Y value / ty")
        self.y_label.pack(anchor="w")
        self.y_value = ttk.Entry(controls)
        self.y_value.insert(0, "1")
        self.y_value.pack(fill="x", pady=(3, 14))

        ttk.Button(
            controls, text="Apply Transformation",
            command=self.apply
        ).pack(fill="x", pady=4)

        ttk.Button(
            controls, text="Reset Shape",
            command=self.reset
        ).pack(fill="x", pady=4)

        ttk.Label(
            controls, text="Matrix Used",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(18, 4))

        self.matrix_text = tk.Text(
            controls, width=27, height=5,
            font=("Consolas", 10), state="disabled"
        )
        self.matrix_text.pack(fill="x")

        ttk.Label(
            controls, text="New Coordinates",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(12, 4))

        self.coordinates_text = tk.Text(
            controls, width=27, height=5,
            font=("Consolas", 10), state="disabled"
        )
        self.coordinates_text.pack(fill="x")

        plot_frame = ttk.LabelFrame(
            body, text="Shape Visualization", padding=8
        )
        plot_frame.pack(side="left", fill="both", expand=True)

        self.figure = Figure(figsize=(7, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(
            self.figure, master=plot_frame
        )
        self.canvas.get_tk_widget().pack(
            fill="both", expand=True
        )

        self.draw()

    def update_labels(self, event=None):
        operation = self.operation.get()

        if operation == "Translation":
            labels = ("X movement (tx)", "Y movement (ty)")
        elif operation == "Scaling":
            labels = ("X scale (sx)", "Y scale (sy)")
        elif operation == "Rotation":
            labels = ("Angle in degrees", "Unused")
        elif operation.startswith("Reflection"):
            labels = ("Unused", "Unused")
        else:
            labels = ("Horizontal shear", "Vertical shear")

        self.x_label.config(text=labels[0])
        self.y_label.config(text=labels[1])

    def make_matrix(self):
        operation = self.operation.get()
        x = float(self.x_value.get() or 0)
        y = float(self.y_value.get() or 0)

        if operation == "Translation":
            return np.array([
                [1, 0, x],
                [0, 1, y],
                [0, 0, 1]
            ], dtype=float)

        if operation == "Scaling":
            return np.diag([x, y, 1.0])

        if operation == "Rotation":
            theta = np.radians(x)
            return np.array([
                [np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]
            ])

        if operation == "Reflection X":
            return np.diag([1.0, -1.0, 1.0])

        if operation == "Reflection Y":
            return np.diag([-1.0, 1.0, 1.0])

        return np.array([
            [1, x, 0],
            [y, 1, 0],
            [0, 0, 1]
        ], dtype=float)

    def apply(self):
        try:
            matrix = self.make_matrix()

            # Apply each new transformation to the current shape
            self.transformed = matrix @ self.transformed

            self.show_text(
                self.matrix_text,
                np.array2string(matrix, precision=3, suppress_small=True)
            )
            self.show_text(
                self.coordinates_text,
                np.array2string(
                    self.transformed[:2].T,
                    precision=3, suppress_small=True
                )
            )
            self.draw()

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numbers in the input fields."
            )

    @staticmethod
    def show_text(widget, text):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.config(state="disabled")

    def reset(self):
        self.transformed = self.original.copy()
        self.show_text(self.matrix_text, "No transformation applied")
        self.show_text(
            self.coordinates_text,
            np.array2string(self.original[:2].T)
        )
        self.draw()

    def draw(self):
        self.ax.clear()

        for points, label in [
            (self.original, "Original"),
            (self.transformed, "Transformed")
        ]:
            x = np.append(points[0], points[0, 0])
            y = np.append(points[1], points[1, 0])
            self.ax.plot(x, y, marker="o", label=label)

        self.ax.axhline(0, color="black", linewidth=0.7)
        self.ax.axvline(0, color="black", linewidth=0.7)
        self.ax.grid(True, alpha=0.35)
        self.ax.set_aspect("equal", adjustable="box")
        self.ax.set_xlabel("X coordinate")
        self.ax.set_ylabel("Y coordinate")
        self.ax.set_title("Matrix Transformations")
        self.ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelMatriX(root)
    root.mainloop()

