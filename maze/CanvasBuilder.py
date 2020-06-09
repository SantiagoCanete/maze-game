import tkinter as tk
import math


class CanvasBuilder:
    def __init__(self, canvas_size=800, line_width=2):
        self._canvas_size = canvas_size
        self._line_width = line_width
        self._canvas_width = self._canvas_size + self._line_width
        self._canvas_height = self._canvas_size + self._line_width
        self._window = tk.Tk()
        self._window.resizable(True, True)
        self._frame = tk.Frame(self._window, width=self._canvas_width, height=self._canvas_height)
        self._canvas = tk.Canvas(self._window, width=self._canvas_width, height=self._canvas_height, bg='white')
        self._avatar = 0
        self._avatar_polygon_points = []
        self._avatar_pad_ratio = 1 / 4
        self._move_x = 0
        self._move_y = 0
        self._location_x = 0
        self._location_y = 0

    def __draw_line(self, x1, y1, x2, y2):
        self._canvas.create_line(x1, y1, x2, y2, fill='black', width=self._line_width)

    def _draw_cell(self, location_x, location_y, cell_size, wall_up, wall_down, wall_right, wall_left):
        # Offset location by line width
        location_x = cell_size * location_x + self._line_width
        location_y = cell_size * location_y + self._line_width

        # Draw horizontal lines
        if wall_down:
            self.__draw_line(location_x - self._line_width / 2, location_y,
                             location_x + cell_size + self._line_width / 2, location_y)

        if wall_up:
            self.__draw_line(location_x - self._line_width / 2, location_y + cell_size,
                             location_x + cell_size + self._line_width / 2, location_y + cell_size)

        # Draw vertical lines
        if wall_left:
            self.__draw_line(location_x, location_y - self._line_width / 2, location_x,
                             location_y + cell_size + self._line_width / 2)

        if wall_right:
            self.__draw_line(location_x + cell_size, location_y - self._line_width / 2,
                             location_x + cell_size, location_y + cell_size + self._line_width / 2)
