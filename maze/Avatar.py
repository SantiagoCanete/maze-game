from time import sleep


class Avatar:
    def __init__(self, canvas, maze, location_x, location_y, cell_size, line_width=2):
        self.__canvas = canvas
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

        self.avatar_orientation = "Right"
        self.avatar = []
        self.is_end = False
        self.check_end()
        self.__square_init = []
        self.__square_end = []
        self.__square_vertices = []
        self.__square = []

        print("Avatar constructor called.")

    def __del__(self):
        self.__canvas.delete(self.avatar)
        self.__canvas.delete(self.__square_init)
        self.__canvas.delete(self.__square_end)
        self.__canvas.delete(self.__square)

        print("Avatar destructor called.")

    def draw_avatar(self):
        self.__square_init = self.__canvas.create_rectangle(self.__square_init_vertices, outline="", fill='red')
        self.__square_end = self.__canvas.create_rectangle(self.__square_end_vertices, outline="", fill='green')
        self.avatar = self.__canvas.create_polygon(self.__avatar_vertices, outline="#476042", fill='blue')

    def move(self, event=0):
        if not self.check_obstacle():
            if not (self.__cell_x == self.__start_cell_x and self.__cell_y == self.__start_cell_y):
                self.__square_vertices = [self.__cell_x + self.__line_width / 2,
                                          self.__cell_y + self.__line_width / 2,
                                          self.__cell_x + self.__cell_size - self.__line_width / 2,
                                          self.__cell_y + self.__cell_size - self.__line_width / 2]
                self.__square = self.__canvas.create_rectangle(self.__square_vertices, outline="", fill='azure')

            if self.avatar_orientation == "Right":
                self.location_x = self.location_x + 1
                self.__cell_x = self.__cell_size * self.location_x + self.__line_width
                move_x = self.__cell_size
                move_y = 0

            elif self.avatar_orientation == "Left":
                self.location_x = self.location_x - 1
                self.__cell_x = self.__cell_size * self.location_x + self.__line_width
                move_x = -self.__cell_size
                move_y = 0

            elif self.avatar_orientation == "Down":
                self.location_y = self.location_y - 1
                self.__cell_y = self.__cell_size * self.location_y + self.__line_width
                move_x = 0
                move_y = -self.__cell_size

            elif self.avatar_orientation == "Up":
                self.location_y = self.location_y + 1
                self.__cell_y = self.__cell_size * self.location_y + self.__line_width
                move_x = 0
                move_y = self.__cell_size

        else:
            move_x = 0
            move_y = 0

        self.check_end()
        self.__canvas.move(self.avatar, move_x, move_y)

    def turn_left(self, event=0):
        if self.avatar_orientation == "Right":
            self.__avatar_vertices = [self.__cell_x + self.__pad_x, self.__cell_y + self.__pad_y,
                                      self.__cell_x + self.__cell_size / 2,
                                      self.__cell_y + self.__cell_size - self.__pad_y,
                                      self.__cell_x + self.__cell_size - self.__pad_x, self.__cell_y + self.__pad_y,
                                      self.__cell_x + self.__cell_size / 2,
                                      self.__cell_y + self.__cell_size / 4 + self.__pad_y / 2]
            self.avatar_orientation = "Up"

        elif self.avatar_orientation == "Up":
            self.__avatar_vertices = [self.__cell_x + self.__cell_size - self.__pad_x, self.__cell_y + self.__pad_y,
                                      self.__cell_x + self.__pad_x, self.__cell_y + self.__cell_size / 2,
                                      self.__cell_x + self.__cell_size - self.__pad_x,
                                      self.__cell_y + self.__cell_size - self.__pad_y,
                                      self.__cell_x + self.__cell_size - self.__cell_size / 4 - self.__pad_x / 2,
                                      self.__cell_y + self.__cell_size / 2]
            self.avatar_orientation = "Left"

        elif self.avatar_orientation == "Left":
            self.__avatar_vertices = [self.__cell_x + self.__pad_x, self.__cell_y + self.__cell_size - self.__pad_y,
                                      self.__cell_x + self.__cell_size / 2, self.__cell_y + self.__pad_y,
                                      self.__cell_x + self.__cell_size - self.__pad_x,
                                      self.__cell_y + self.__cell_size - self.__pad_y,
                                      self.__cell_x + self.__cell_size / 2,
                                      self.__cell_y + self.__cell_size - self.__cell_size / 4 - self.__pad_y / 2]
            self.avatar_orientation = "Down"

        elif self.avatar_orientation == "Down":
            self.__avatar_vertices = [self.__cell_x + self.__pad_x, self.__cell_y + self.__pad_y,
                                      self.__cell_x + self.__cell_size - self.__pad_x,
                                      self.__cell_y + self.__cell_size / 2,
                                      self.__cell_x + self.__pad_x, self.__cell_y + self.__cell_size - self.__pad_y,
                                      self.__cell_x + self.__cell_size / 4 + self.__pad_x / 2,
                                      self.__cell_y + self.__cell_size / 2]
            self.avatar_orientation = "Right"

        self.__canvas.delete(self.avatar)
        self.draw_avatar()

    def check_obstacle(self):
        return self.__maze[self.location_x][self.location_y].walls[self.avatar_orientation]

    def check_end(self):
        print([self.location_x, self.location_y])
        if self.location_x == len(self.__maze) - 1 and self.location_y == len(self.__maze[0]) - 1:
            print("The avatar reached the end of the Maze.")
            self.is_end = True
        else:
            self.is_end = False

    @staticmethod
    def pause(sleep_period):
        sleep(sleep_period)
