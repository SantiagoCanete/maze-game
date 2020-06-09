import maze
import tkinter as tk
from tkinter import messagebox


class MazeGui(maze.CanvasBuilder):
    def __init__(self):

        self.__cell_size = 10
        self.__maze = []
        self.__button_draw_avatar = []
        self.__button_run_solution = []
        self.__solver = []

        # Initialize superclass
        maze.CanvasBuilder.__init__(self)

        self.__form_gui_structure()

    def __form_gui_structure(self):
        self._window.title("Maze Creator")
        tk.Label(self._window, text="Number of columns:", relief='sunken').grid(row=0, column=1, sticky=tk.W)
        tk.Label(self._window, text="Number of rows:", relief='sunken').grid(row=1, column=1, sticky=tk.W)
        tk.Label(self._window, text="Avatar X position:", relief='sunken').grid(row=3, column=1, sticky=tk.W)
        tk.Label(self._window, text="Avatar Y position:", relief='sunken').grid(row=4, column=1, sticky=tk.W)
        tk.Label(self._window, text="Avatar position: ", bg='white', relief='sunken') \
            .grid(row=8, column=0, columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S)
        tk.Label(self._window, text="", bg='white', relief='sunken') \
            .grid(row=8, column=2, columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S)
        tk.Label(self._window, text="Avatar Orientation:", bg='white', relief='sunken') \
            .grid(row=9, column=0, columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S)
        tk.Label(self._window, text="", bg='white', relief='sunken') \
            .grid(row=9, column=2, columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S)
        tk.Label(self._window, text="Status", bg='white', relief='sunken') \
            .grid(row=10, column=0, columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S)
        tk.Label(self._window, text="", bg='white', relief='sunken') \
            .grid(row=10, column=2, columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S)

        entry_row = tk.Entry(self._window)
        entry_row.grid(row=0, column=2, sticky=tk.W)
        entry_row.insert(0, "6")

        entry_column = tk.Entry(self._window)
        entry_column.grid(row=1, column=2, sticky=tk.W)
        entry_column.insert(0, "6")

        entry_avatar_position_x = tk.Entry(self._window)
        entry_avatar_position_x.grid(row=3, column=2, sticky=tk.W)
        entry_avatar_position_x.insert(0, "0")

        entry_avatar_position_y = tk.Entry(self._window)
        entry_avatar_position_y.grid(row=4, column=2, sticky=tk.W)
        entry_avatar_position_y.insert(0, "0")

        button_generate_maze = tk.Button(self._window, text="New Maze",
                                         command=lambda: self.__draw_maze(int(entry_row.get()),
                                                                          int(entry_column.get())))

        button_generate_maze.grid(row=2, column=1, columnspan=2)

        self.button_draw_avatar = tk.Button(self._window, text="Draw Avatar",
                                            command=lambda:
                                            self.__initialize_avatar(int(entry_avatar_position_x.get()),
                                                                     int(entry_avatar_position_y.get())))

        self.button_draw_avatar.grid(row=5, column=1, columnspan=2)

        self.__disable_button(self.button_draw_avatar)

        self.button_run_solution = tk.Button(self._window, text="Run Solution", command=self.__initialize_maze_solver)
        self.button_run_solution.grid(row=6, column=1)

        self.__disable_button(self.button_run_solution)

        button_quit = tk.Button(self._window, text="Quit", command=self._window.quit)
        button_quit.grid(row=6, column=2)

        self._canvas.grid(row=0, column=4, rowspan=20, columnspan=20)

        self._window.bind("<KeyPress-Up>", lambda e: self.__move_avatar(e))

        self._window.bind("<KeyPress-Left>", lambda e: self.avatar.turn_left(e))

        self._window.mainloop()

    def __draw_maze(self, num_rows, num_columns):
        self._canvas.delete("all")
        self.__disable_button(self.button_run_solution)
        maze_obj = maze.MazeBuilder(num_rows, num_columns)
        maze_obj.make_maze()
        self.__maze = maze_obj.maze

        if num_rows > num_columns:
            self.__cell_size = self._canvas_size / num_rows
        else:
            self.__cell_size = self._canvas_size / num_columns

        for i in range(num_columns):
            for j in range(num_rows):
                self._draw_cell(i, j, self.__cell_size,
                                self.__maze[i][j].walls['Up'],
                                self.__maze[i][j].walls['Down'],
                                self.__maze[i][j].walls['Right'],
                                self.__maze[i][j].walls['Left'])

        self.__enable_button(self.button_draw_avatar)

    def __initialize_avatar(self, location_x, location_y):
        self.avatar = maze.Avatar(self._canvas, self.__maze, location_x, location_y,
                                  self.__cell_size)
        if self.avatar.is_end:
            title = "Maze Creator"
            message = "The avatar cannot start at the end of the maze :("
            messagebox.showerror(title, message)
        else:
            self.avatar.draw_avatar()
            self.__enable_button(self.button_run_solution)

    def __initialize_maze_solver(self):
        self.__solver = maze.MazeSolver(self.__maze, self.avatar)
        self.__solver.my_solver()

    def __move_avatar(self, event):
        self.avatar.move(event)

        if self.avatar.is_end:
            title = "Maze Creator"
            question = "Congratulations, you finished the Maze!!\n\nYou want to play again?"
            answer = messagebox.askquestion(title, question)
            if answer == 'no':
                self._window.quit()
            else:
                self._canvas.delete("all")
                self.__disable_button(self.button_draw_avatar)
                self.__disable_button(self.button_run_solution)

    @staticmethod
    def __disable_button(button):
        button["state"] = "disabled"

    @staticmethod
    def __enable_button(button):
        button["state"] = "normal"
