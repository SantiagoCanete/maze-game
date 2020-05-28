class Avatar:
    def __init__(self, canvas, maze, location_x, location_y, cell_size, line_width=2):
        self.canvas = canvas
        self.maze = maze
        self.cell_size = cell_size
        self.line_width = line_width
        self.location_x = location_x
        self.location_y = location_y
        self.cell_x = self.cell_size * self.location_x + line_width
        self.cell_y = self.cell_size * self.location_y + line_width
        self.cell_pad_ratio = 1 / 6
        self.cell_center_x = self.cell_x + self.cell_size / 2.0
        self.cell_center_y = self.cell_y + self.cell_size / 2.0
        self.avatar_side = self.cell_size

        self.pad_x = self.cell_pad_ratio * self.cell_size
        self.pad_y = self.cell_pad_ratio * self.cell_size

        self.avatar_vertices = [self.cell_x + self.pad_x, self.cell_y + self.pad_y,
                                self.cell_x + self.cell_size - self.pad_x, self.cell_y + self.cell_size / 2,
                                self.cell_x + self.pad_x, self.cell_y + self.cell_size - self.pad_y,
                                self.cell_x + self.cell_size / 4 + self.pad_x / 2, self.cell_y + self.cell_size / 2]

        self.avatar_orientation = "Right"
        self.avatar = []

        print("Avatar constructor called.")

    def draw_avatar(self):
        self.canvas.delete(self.avatar)
        self.avatar = self.canvas.create_polygon(self.avatar_vertices, outline="#476042", fill='blue')

    def move(self, event):
        print(event.keysym)
        if not self.check_obstacle():
            if self.avatar_orientation == "Right":
                self.location_x = self.location_x + 1
                self.cell_x = self.cell_size * self.location_x + self.line_width
                move_x = self.cell_size
                move_y = 0
            elif self.avatar_orientation == "Left":
                self.location_x = self.location_x - 1
                self.cell_x = self.cell_size * self.location_x + self.line_width
                move_x = -self.cell_size
                move_y = 0
            elif self.avatar_orientation == "Down":
                self.location_y = self.location_y - 1
                self.cell_y = self.cell_size * self.location_y + self.line_width
                move_x = 0
                move_y = -self.cell_size
            elif self.avatar_orientation == "Up":
                self.location_y = self.location_y + 1
                self.cell_y = self.cell_size * self.location_y + self.line_width
                move_x = 0
                move_y = self.cell_size
        else:
            move_x = 0
            move_y = 0

        self.canvas.move(self.avatar, move_x, move_y)

    def rotate(self, event):
        print(event.keysym)
        if self.avatar_orientation == "Right":
            self.avatar_vertices = [self.cell_x + self.pad_x, self.cell_y + self.pad_y,
                                    self.cell_x + self.cell_size / 2, self.cell_y + self.cell_size - self.pad_y,
                                    self.cell_x + self.cell_size - self.pad_x, self.cell_y + self.pad_y,
                                    self.cell_x + self.cell_size / 2, self.cell_y + self.cell_size / 4 + self.pad_y / 2]
            self.avatar_orientation = "Up"

        elif self.avatar_orientation == "Up":
            self.avatar_vertices = [self.cell_x + self.cell_size - self.pad_x, self.cell_y + self.pad_y,
                                    self.cell_x + self.pad_x, self.cell_y + self.cell_size / 2,
                                    self.cell_x + self.cell_size - self.pad_x,
                                    self.cell_y + self.cell_size - self.pad_y,
                                    self.cell_x + self.cell_size - self.cell_size / 4 - self.pad_x / 2,
                                    self.cell_y + self.cell_size / 2]
            self.avatar_orientation = "Left"

        elif self.avatar_orientation == "Left":
            self.avatar_vertices = [self.cell_x + self.pad_x, self.cell_y + self.cell_size - self.pad_y,
                                    self.cell_x + self.cell_size / 2, self.cell_y + self.pad_y,
                                    self.cell_x + self.cell_size - self.pad_x,
                                    self.cell_y + self.cell_size - self.pad_y,
                                    self.cell_x + self.cell_size / 2,
                                    self.cell_y + self.cell_size - self.cell_size / 4 - self.pad_y / 2]
            self.avatar_orientation = "Down"

        elif self.avatar_orientation == "Down":
            self.avatar_vertices = [self.cell_x + self.pad_x, self.cell_y + self.pad_y,
                                    self.cell_x + self.cell_size - self.pad_x, self.cell_y + self.cell_size / 2,
                                    self.cell_x + self.pad_x, self.cell_y + self.cell_size - self.pad_y,
                                    self.cell_x + self.cell_size / 4 + self.pad_x / 2, self.cell_y + self.cell_size / 2]
            self.avatar_orientation = "Right"

        self.draw_avatar()

    def check_obstacle(self):
        return self.maze[self.location_x][self.location_y].walls[self.avatar_orientation]
