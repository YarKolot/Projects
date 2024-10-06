import tkinter as tk
from tkinter import colorchooser

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nedopaint")

        self.canvas = tk.Canvas(self.root, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.root.attributes('-alpha', 0.7)

        self.brush_color = 'black'
        self.bg_color = 'white'
        self.saved_brush_color = self.brush_color
        self.brush_size = 5
        self.eraser_mode = False
        self.last_x = None
        self.last_y = None

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-3>", self.create_point)
        self.canvas.bind("<ButtonRelease-1>", self.reset_last_position)

        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("200x450")
        self.settings_window.attributes('-topmost', True)

        self.color_button = tk.Button(self.settings_window, text="Select Brush Color", command=self.choose_brush_color)
        self.color_button.pack(pady=5)

        self.bg_color_button = tk.Button(self.settings_window, text="Select Canvas Color", command=self.choose_bg_color)
        self.bg_color_button.pack(pady=5)

        self.mode_button = tk.Button(self.settings_window, text="Switch to Eraser", command=self.toggle_mode)
        self.mode_button.pack(pady=5)

        self.size_slider = tk.Scale(self.settings_window, from_=1, to=50, orient=tk.HORIZONTAL, label="Brush Size", command=self.update_brush_size)
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(pady=5)

        self.alpha_slider = tk.Scale(self.settings_window, from_=1, to=100, orient=tk.HORIZONTAL, label="Canvas Transparency", command=self.update_canvas_alpha)
        self.alpha_slider.set(70)
        self.alpha_slider.pack(pady=5)

        self.clear_button = tk.Button(self.settings_window, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.settings_window.protocol("WM_DELETE_WINDOW", self.close_app)

    def paint(self, event):
        if self.last_x is not None and self.last_y is not None:
            x1, y1 = self.last_x, self.last_y
            x2, y2 = event.x, event.y
            color = self.bg_color if self.eraser_mode else self.brush_color
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=self.brush_size, capstyle=tk.ROUND, smooth=True)
        self.last_x, self.last_y = event.x, event.y

    def create_point(self, event):
        color = self.bg_color if self.eraser_mode else self.brush_color
        x1, y1 = event.x - self.brush_size // 2, event.y - self.brush_size // 2
        x2, y2 = event.x + self.brush_size // 2, event.y + self.brush_size // 2
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

    def reset_last_position(self, event):
        self.last_x = None
        self.last_y = None

    def choose_brush_color(self):
        color = colorchooser.askcolor(color=self.brush_color)[1]
        if color:
            self.brush_color = color
            self.saved_brush_color = color

    def choose_bg_color(self):
        color = colorchooser.askcolor(color=self.bg_color)[1]
        if color:
            self.bg_color = color
            self.canvas.configure(bg=color)
            if self.eraser_mode:
                self.brush_color = self.bg_color

    def toggle_mode(self):
        if self.eraser_mode:
            self.brush_color = self.saved_brush_color
            self.mode_button.config(text="Switch to Eraser")
        else:
            self.saved_brush_color = self.brush_color
            self.brush_color = self.bg_color
            self.mode_button.config(text="Switch to Brush")
        self.eraser_mode = not self.eraser_mode

    def update_brush_size(self, value):
        self.brush_size = int(value)

    def update_canvas_alpha(self, value):
        alpha = int(value) / 100
        self.root.attributes('-alpha', alpha)

    def clear_canvas(self):
        self.canvas.delete("all")

    def close_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()