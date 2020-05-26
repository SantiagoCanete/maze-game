import maze
import tkinter as tk


class MazeGui(maze.CanvasBuilder):
    def __init__(self):

        self.cell_size = 10

        # Initialize superclasses
        maze.CanvasBuilder.__init__(self)

    def form_gui_structure(self):
        self.window.title("Maze Creator")
        tk.Label(self.window, text="Number of columns:").grid(row=0, column=0)
        tk.Label(self.window, text="Number of rows:   ").grid(row=1, column=0)
        tk.Label(self.window, text="Avatar X position:").grid(row=3, column=0)
        tk.Label(self.window, text="Avatar Y position:").grid(row=4, column=0)

        entry_row = tk.Entry(self.window)
        entry_row.grid(row=0, column=1)
        entry_row.insert(0, "20")

        entry_column = tk.Entry(self.window)
        entry_column.grid(row=1, column=1)
        entry_column.insert(0, "20")

        entry_avatar_position_x = tk.Entry(self.window)
        entry_avatar_position_x.grid(row=3, column=1)
        entry_avatar_position_x.insert(0, "0")

        entry_avatar_position_y = tk.Entry(self.window)
        entry_avatar_position_y.grid(row=4, column=1)
        entry_avatar_position_y.insert(0, "0")

        button_generate_maze = tk.Button(self.window, text="New Maze",
                                         command=lambda: self.draw_maze(int(entry_row.get()),
                                                                        int(entry_column.get())))
        button_generate_maze.grid(row=2, column=0, sticky=tk.W)

        button_quit = tk.Button(self.window, text="Quit", command=self.window.quit)
        button_quit.grid(row=6, column=0, sticky=tk.W)

        button_draw_avatar = tk.Button(self.window, text="Draw Avatar",
                                       command=lambda: self.draw_avatar(int(entry_avatar_position_x.get()),
                                                                        int(entry_avatar_position_y.get()),
                                                                        self.cell_size))
        button_draw_avatar.grid(row=5, column=0, sticky=tk.W)

        self.canvas.grid(row=0, column=2, rowspan=20, columnspan=20)

        self.window.bind("<KeyPress-Up>", lambda e: self.move_forward(e, self.cell_size))

        self.window.mainloop()

    def draw_maze(self, num_rows, num_columns):
        self.canvas.delete("all")
        maze_obj = maze.MazeBuilder(num_rows, num_columns)
        maze_obj.make_maze()
        maze_grid = maze_obj.maze

        if num_rows > num_columns:
            self.cell_size = self.canvas_size / num_rows
        else:
            self.cell_size = self.canvas_size / num_columns

        for i in range(num_columns):
            for j in range(num_rows):
                self.draw_cell(i, j, self.cell_size,
                               maze_grid[i][j].walls['Up'],
                               maze_grid[i][j].walls['Down'],
                               maze_grid[i][j].walls['Right'],
                               maze_grid[i][j].walls['Left'])
