from time import sleep


class Avatar:
    def __init__(self, canvas, maze, location_x, location_y, cell_size, line_width=2):
        self._canvas = canvas
        self.__maze = maze
        self.__cell_size = cell_size
        self.__line_width = line_width
        self.location_x = location_x
        self.location_y = location_y
        self.__cell_x = self.__cell_size * self.location_x + self.__line_width
        self.__cell_y = self.__cell_size * self.location_y + self.__line_width
        self.__start_cell_x = self.__cell_x
        self.__start_cell_y = self.__cell_y
        self.__end_cell_x = self.__cell_size * (len(self.__maze) - 1) + self.__line_width
        self.__end_cell_y = self.__cell_size * (len(self.__maze[0]) - 1) + self.__line_width
        self.__cell_pad_ratio = 1 / 6
        self.__cell_center_x = self.__cell_x + self.__cell_size / 2.0
        self.__cell_center_y = self.__cell_y + self.__cell_size / 2.0
        self.__avatar_side = self.__cell_size

        self.__pad_x = self.__cell_pad_ratio * self.__cell_size
        self.__pad_y = self.__cell_pad_ratio * self.__cell_size

        self.__avatar_vertices = [self.__cell_x + self.__pad_x, self.__cell_y + self.__pad_y,
                                  self.__cell_x + self.__cell_size - self.__pad_x, self.__cell_y + self.__cell_size / 2,
                                  self.__cell_x + self.__pad_x, self.__cell_y + self.__cell_size - self.__pad_y,
                                  self.__cell_x + self.__cell_size / 4 + self.__pad_x / 2,
                                  self.__cell_y + self.__cell_size / 2]
        self.__square_init_vertices = [self.__cell_x + self.__line_width / 2,
                                       self.__cell_y + self.__line_width / 2,
                                       self.__cell_x + self.__cell_size - self.__line_width / 2,
                                       self.__cell_y + self.__cell_size - self.__line_width / 2]
        self.__square_end_vertices = [self.__end_cell_x + self.__line_width / 2,
                                      self.__end_cell_y + self.__line_width / 2,
                                      self.__end_cell_x + self.__cell_size - self.__line_width / 2,
                                      self.__end_cell_y + self.__cell_size - self.__line_width / 2]

        self.orientation = "East"
        self.is_end = False
        self.__avatar = []
        self.__check_end()
        self.__square_init = []
        self.__square_end = []
        self.__square_vertices = []
        self.__square = []

        self.__draw_avatar()

        print("Avatar constructor called.")

    def __del__(self):
        self._canvas.delete(self.__avatar)
        self._canvas.delete(self.__square_init)
        self._canvas.delete(self.__square_end)
        self._canvas.delete(self.__square)

        print("Avatar destructor called.")

    def __draw_avatar(self):
        self.__square_init = self._canvas.create_rectangle(self.__square_init_vertices, outline="", fill='red')
        self.__square_end = self._canvas.create_rectangle(self.__square_end_vertices, outline="", fill='green')
        self.__avatar = self._canvas.create_polygon(self.__avatar_vertices, outline="#476042", fill='blue')
        self.__mark_visited()

    def move(self, event=0):
        move_x = 0
        move_y = 0

        if not self.check_obstacle():
            if not (self.__cell_x == self.__start_cell_x and self.__cell_y == self.__start_cell_y):
                self.__square_vertices = [self.__cell_x + self.__line_width / 2,
                                          self.__cell_y + self.__line_width / 2,
                                          self.__cell_x + self.__cell_size - self.__line_width / 2,
                                          self.__cell_y + self.__cell_size - self.__line_width / 2]
                self.__square = self._canvas.create_rectangle(self.__square_vertices, outline="", fill='azure')

            if self.orientation == "East":
                self.location_x = self.location_x + 1
                self.__cell_x = self.__cell_size * self.location_x + self.__line_width
                move_x = self.__cell_size
                move_y = 0

            elif self.orientation == "West":
                self.location_x = self.location_x - 1
                self.__cell_x = self.__cell_size * self.location_x + self.__line_width
                move_x = -self.__cell_size
                move_y = 0

            elif self.orientation == "North":
                self.location_y = self.location_y - 1
                self.__cell_y = self.__cell_size * self.location_y + self.__line_width
                move_x = 0
                move_y = -self.__cell_size

            elif self.orientation == "South":
                self.location_y = self.location_y + 1
                self.__cell_y = self.__cell_size * self.location_y + self.__line_width
                move_x = 0
                move_y = self.__cell_size

        else:
            move_x = 0
            move_y = 0

        self.__check_end()
        self._canvas.move(self.__avatar, move_x, move_y)
        self.__mark_visited()

    def turn_left(self, event=0):
        if self.orientation == "East":
            self.__avatar_vertices = [self.__cell_x + self.__pad_x, self.__cell_y + self.__pad_y,
                                      self.__cell_x + self.__cell_size / 2,
                                      self.__cell_y + self.__cell_size - self.__pad_y,
                                      self.__cell_x + self.__cell_size - self.__pad_x, self.__cell_y + self.__pad_y,
                                      self.__cell_x + self.__cell_size / 2,
                                      self.__cell_y + self.__cell_size / 4 + self.__pad_y / 2]
            self.orientation = "South"

        elif self.orientation == "South":
            self.__avatar_vertices = [self.__cell_x + self.__cell_size - self.__pad_x, self.__cell_y + self.__pad_y,
                                      self.__cell_x + self.__pad_x, self.__cell_y + self.__cell_size / 2,
                                      self.__cell_x + self.__cell_size - self.__pad_x,
                                      self.__cell_y + self.__cell_size - self.__pad_y,
                                      self.__cell_x + self.__cell_size - self.__cell_size / 4 - self.__pad_x / 2,
                                      self.__cell_y + self.__cell_size / 2]
            self.orientation = "West"

        elif self.orientation == "West":
            self.__avatar_vertices = [self.__cell_x + self.__pad_x, self.__cell_y + self.__cell_size - self.__pad_y,
                                      self.__cell_x + self.__cell_size / 2, self.__cell_y + self.__pad_y,
                                      self.__cell_x + self.__cell_size - self.__pad_x,
                                      self.__cell_y + self.__cell_size - self.__pad_y,
                                      self.__cell_x + self.__cell_size / 2,
                                      self.__cell_y + self.__cell_size - self.__cell_size / 4 - self.__pad_y / 2]
            self.orientation = "North"

        elif self.orientation == "North":
            self.__avatar_vertices = [self.__cell_x + self.__pad_x, self.__cell_y + self.__pad_y,
                                      self.__cell_x + self.__cell_size - self.__pad_x,
                                      self.__cell_y + self.__cell_size / 2,
                                      self.__cell_x + self.__pad_x, self.__cell_y + self.__cell_size - self.__pad_y,
                                      self.__cell_x + self.__cell_size / 4 + self.__pad_x / 2,
                                      self.__cell_y + self.__cell_size / 2]
            self.orientation = "East"

        self._canvas.delete(self.__avatar)
        self.__draw_avatar()

    def check_obstacle(self):
        return self.__maze[self.location_x][self.location_y].walls[self.orientation]

    def check_visited(self):
        is_visited = 0

        if self.orientation == "East":
            is_visited = self.__maze[self.location_x + 1][self.location_y].avatar_visited

        elif self.orientation == "West":
            is_visited = self.__maze[self.location_x - 1][self.location_y].avatar_visited

        elif self.orientation == "North":
            is_visited = self.__maze[self.location_x][self.location_y - 1].avatar_visited

        elif self.orientation == "South":
            is_visited = self.__maze[self.location_x][self.location_y + 1].avatar_visited

        return is_visited

    def __mark_visited(self):
        self.__maze[self.location_x][self.location_y].avatar_visited = 1

    def __check_end(self):
        print([self.location_x, self.location_y])
        if self.location_x == len(self.__maze) - 1 and self.location_y == len(self.__maze[0]) - 1:
            print("The avatar reached the end of the Maze.")
            self.is_end = True
        else:
            self.is_end = False

    def pause(self, sleep_period):
        self._canvas.update()
        sleep(sleep_period)
