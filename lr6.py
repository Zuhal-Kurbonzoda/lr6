import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def cohen_sutherland(x1, y1, x2, y2, x_min, y_min, x_max, y_max):
    INSIDE = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 4
    TOP = 8

    def compute_code(x, y):
        code = INSIDE
        if x < x_min:
            code |= LEFT
        elif x > x_max:
            code |= RIGHT
        if y < y_min:
            code |= BOTTOM
        elif y > y_max:
            code |= TOP
        return code

    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)

    while True:
        if code1 == INSIDE and code2 == INSIDE:
            return True, x1, y1, x2, y2
        elif code1 & code2 != 0:
            return False, None, None, None, None
        elif code1 != INSIDE:
            if code1 & TOP != 0:
                x1 = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y1 = y_max
            elif code1 & BOTTOM != 0:
                x1 = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y1 = y_min
            elif code1 & RIGHT != 0:
                y1 = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x1 = x_max
            elif code1 & LEFT != 0:
                y1 = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x1 = x_min
            code1 = compute_code(x1, y1)
        else:
            if code2 & TOP != 0:
                x2 = x2 + (x1 - x2) * (y_max - y2) / (y1 - y2)
                y2 = y_max
            elif code2 & BOTTOM != 0:
                x2 = x2 + (x1 - x2) * (y_min - y2) / (y1 - y2)
                y2 = y_min
            elif code2 & RIGHT != 0:
                y2 = y2 + (y1 - y2) * (x_max - x2) / (x1 - x2)
                x2 = x_max
            elif code2 & LEFT != 0:
                y2 = y2 + (y1 - y2) * (x_min - x2) / (x1 - x2)
                x2 = x_min
            code2 = compute_code(x2, y2)

def midpoint_clipping(x1, y1, x2, y2, x_min, y_min, x_max, y_max):
    def compute_midpoint(x1, y1, x2, y2):
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    def is_inside(x, y):
        return x_min <= x <= x_max and y_min <= y <= y_max

    mid_x, mid_y = compute_midpoint(x1, y1, x2, y2)

    if is_inside(mid_x, mid_y):
        return True, x1, y1, x2, y2
    else:
        if not is_inside(x1, y1) and not is_inside(x2, y2):
            return False, None, None, None, None
        elif not is_inside(x1, y1):
            x1, y1 = mid_x, mid_y
        else:
            x2, y2 = mid_x, mid_y
        return midpoint_clipping(x1, y1, x2, y2, x_min, y_min, x_max, y_max)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.algorithm_frame = tk.Frame(self)
        self.algorithm_frame.pack(side=tk.TOP, fill=tk.X)

        self.cohen_sutherland_button = tk.Button(self.algorithm_frame, text="Алгоритм Сазерленда-Коэна", command=self.cohen_sutherland_algorithm)
        self.cohen_sutherland_button.pack(side=tk.TOP, fill=tk.X)

        self.midpoint_clipping_button = tk.Button(self.algorithm_frame, text="Алгоритм разбиения средней точкой", command=self.midpoint_clipping_algorithm)
        self.midpoint_clipping_button.pack(side=tk.TOP, fill=tk.X)

        self.coordinates_frame = tk.Frame(self)
        self.coordinates_frame.pack(side=tk.TOP, fill=tk.X)
    

        self.line_coordinates_frame = tk.Frame(self)
        self.line_coordinates_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.x1_label = tk.Label(self.line_coordinates_frame, text="x1:")
        self.x1_label.pack(side=tk.TOP)
        self.x1_entry = tk.Entry(self.line_coordinates_frame)
        self.x1_entry.pack(side=tk.TOP)
        
        self.y1_label = tk.Label(self.line_coordinates_frame, text="y1:")
        self.y1_label.pack(side=tk.TOP)
        self.y1_entry = tk.Entry(self.line_coordinates_frame)
        self.y1_entry.pack(side=tk.TOP)
        
        self.x2_label = tk.Label(self.line_coordinates_frame, text="x2:")
        self.x2_label.pack(side=tk.TOP)
        self.x2_entry = tk.Entry(self.line_coordinates_frame)
        self.x2_entry.pack(side=tk.TOP)
        
        self.y2_label = tk.Label(self.line_coordinates_frame, text="y2:")
        self.y2_label.pack(side=tk.TOP)
        self.y2_entry = tk.Entry(self.line_coordinates_frame)
        self.y2_entry.pack(side=tk.TOP)

    def cohen_sutherland_algorithm(self):
        x_min = 0
        y_min = 0
        x_max = 1000
        y_max = 1000
        x1 = int(self.x1_entry.get())
        y1 = int(self.y1_entry.get())
        x2 = int(self.x2_entry.get())
        y2 = int(self.y2_entry.get())

        visible, x1, y1, x2, y2 = cohen_sutherland(x1, y1, x2, y2, x_min, y_min, x_max, y_max)

        if visible:
            plt.plot([x1, x2], [y1, y2], 'b-')
            plt.xlim(x_min, x_max)
            plt.ylim(y_min, y_max)
            plt.gca().set_aspect('equal')
            plt.show()
        else:
            print("Отрезок не виден")

    def midpoint_clipping_algorithm(self):
        x_min = 0
        y_min = 0
        x_max = 1000
        y_max = 1000
        x1 = int(self.x1_entry.get())
        y1 = int(self.y1_entry.get())
        x2 = int(self.x2_entry.get())
        y2 = int(self.y2_entry.get())

        visible, x1, y1, x2, y2 = midpoint_clipping(x1, y1, x2, y2, x_min, y_min, x_max, y_max)

        if visible:
            plt.plot([x1, x2], [y1, y2], 'b-')
            plt.xlim(x_min, x_max)
            plt.ylim(y_min, y_max)
            plt.gca().set_aspect('equal')
            plt.show()
        else:
            print("Отрезок не виден")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
