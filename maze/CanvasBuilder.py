import tkinter as tk
import math


class CanvasBuilder:
    def __init__(self, canvas_size=1000, line_width=2):
        self.canvas_size = canvas_size
        self.line_width = line_width
        self.canvas_width = self.canvas_size + self.line_width
        self.canvas_height = self.canvas_size + self.line_width
        self.window = tk.Tk()
        self.frame = tk.Frame(self.window, width=self.canvas_width, height=self.canvas_height)
        self.canvas = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.avatar = []
        self.avatar_polygon_points = []
        self.avatar_pad_ratio = 1 / 4
        self.move_x = 0
        self.move_y = 0
        self.location_x = 0
        self.location_y = 0

    def draw_line(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2, fill='black', width=self.line_width)

    def draw_cell(self, location_x, location_y, cell_size, wall_up, wall_down, wall_right, wall_left):
        # Offset location by line width
        location_x = cell_size * location_x + self.line_width
        location_y = cell_size * location_y + self.line_width

        # Draw horizontal lines
        if wall_down:
            self.draw_line(location_x, location_y, location_x + cell_size, location_y)

        if wall_up:
            self.draw_line(location_x, location_y + cell_size, location_x + cell_size,
                           location_y + cell_size)

        # Draw vertical lines
        if wall_left:
            self.draw_line(location_x, location_y, location_x, location_y + cell_size)

        if wall_right:
            self.draw_line(location_x + cell_size, location_y, location_x + cell_size,
                           location_y + cell_size)
