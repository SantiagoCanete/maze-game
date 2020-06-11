import maze
import tkinter as tk
from tkinter import messagebox
from time import sleep


class MazeGui(maze.CanvasBuilder):
    def __init__(self):

        self.__cell_size = 10
        self.__sleep_period = 0.1
        self.__maze = []
        self.__button_draw_avatar = []
        self.__button_run_solution = []
        self.__position_dialog_label = []
        self.__orientation_dialog_label = []
        self.__status_dialog_label = []
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
        self.__position_dialog_label = tk.Label(self._window, text="", bg='white', relief='sunken')
        self.__position_dialog_label.grid(row=8, column=2, columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S)
        tk.Label(self._window, text="Avatar Orientation:", bg='white', relief='sunken') \
            .grid(row=9, column=0, columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S)
        self.__orientation_dialog_label = tk.Label(self._window, text="", bg='white', relief='sunken')
        self.__orientation_dialog_label.grid(row=9, column=2, columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S)
        tk.Label(self._window, text="Status", bg='white', relief='sunken') \
            .grid(row=10, column=0, columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S)
        self.__status_dialog_label = tk.Label(self._window, text="", bg='white', relief='sunken')
        self.__status_dialog_label.grid(row=10, column=2, columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S)

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

        self.__button_draw_avatar = tk.Button(self._window, text="Draw Avatar",
                                              command=lambda:
                                              self.__initialize_avatar(int(entry_avatar_position_x.get()),
                                                                       int(entry_avatar_position_y.get())))

        self.__button_draw_avatar.grid(row=5, column=1, columnspan=2)

        self.__disable_button(self.__button_draw_avatar)

        self.__button_run_solution = tk.Button(self._window, text="Run Solution", command=self.__initialize_maze_solver)
        self.__button_run_solution.grid(row=6, column=1)

        self.__disable_button(self.__button_run_solution)

        button_quit = tk.Button(self._window, text="Quit", command=self._window.quit)
        button_quit.grid(row=6, column=2)

        self._canvas.grid(row=0, column=4, rowspan=20, columnspan=20)

        self._window.bind("<KeyPress-Up>", lambda e: self.__move_avatar(e))

        self._window.bind("<KeyPress-Left>", lambda e: self.__turn_avatar(e))

        self._window.mainloop()

    def __draw_maze(self, num_rows, num_columns):
        self._canvas.delete("all")
        self.__clear_dialog_box()
        self.__disable_button(self.__button_run_solution)
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
                                self.__maze[i][j].walls['South'],
                                self.__maze[i][j].walls['North'],
                                self.__maze[i][j].walls['East'],
                                self.__maze[i][j].walls['West'])

        self.__enable_button(self.__button_draw_avatar)

    def __initialize_avatar(self, location_x, location_y):
        self.__avatar = maze.Avatar(self._canvas, self.__maze, location_x, location_y,
                                    self.__cell_size)
        self.__update_dialog_box()

        if self.__avatar.is_end:
            title = "Maze Creator"
            message = "The avatar cannot start at the end of the maze :("
            messagebox.showerror(title, message)
            self.__avatar.__del__()
        else:
            self.__enable_button(self.__button_run_solution)

    def __initialize_maze_solver(self):
        self.__solver = maze.MazeSolver(self.__maze, self.__avatar)
        self.__solver.my_solver()
        self.__update_dialog_box()

    def __move_avatar(self, event):
        self.__avatar.move(event)
        self.__update_dialog_box()

        if self.__avatar.is_end:
            title = "Maze Creator"
            question = "Congratulations, you finished the Maze!!\n\nYou want to play again?"
            answer = messagebox.askquestion(title, question)
            if answer == 'no':
                self._window.quit()
            else:
                self._canvas.delete("all")
                self.__disable_button(self.__button_draw_avatar)
                self.__disable_button(self.__button_run_solution)

    def __turn_avatar(self, event):
        self.__avatar.turn_left(event)
        self.__update_dialog_box()

    def __update_dialog_box(self):
        self.__position_dialog_label.config(text="[{location_x}, {location_y}]"
                                            .format(location_x=str(self.__avatar.location_x),
                                                    location_y=str(self.__avatar.location_y)))
        self.__orientation_dialog_label.config(text=self.__avatar.orientation)

        if self.__avatar.check_obstacle() and not self.__avatar.is_end:
            self.__status_dialog_label.config(text="Wall")
        elif self.__avatar.is_end:
            self.__status_dialog_label.config(text="End")
        elif self.__avatar.check_visited():
            self.__status_dialog_label.config(text="Visited")
        else:
            self.__status_dialog_label.config(text="Clear")

        self._canvas.update()
        sleep(self.__sleep_period)

    def __clear_dialog_box(self):
        self.__position_dialog_label.config(text="")
        self.__orientation_dialog_label.config(text="")
        self.__status_dialog_label.config(text="")
        self._canvas.update()
        sleep(self.__sleep_period)

    @staticmethod
    def __disable_button(button):
        button["state"] = "disabled"

    @staticmethod
    def __enable_button(button):
        button["state"] = "normal"
