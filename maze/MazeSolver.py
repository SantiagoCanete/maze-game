from maze import MazeGui


class MazeSolver:
    def __init__(self, maze_grid, avatar):
        self.maze = maze_grid
        self.avatar = avatar

    def my_solver(self):
        """
        Write your maze solver here.
        -----------------------------------------
        Here is a list of what the avatar can do:
            self.avatar.move()
            self.avatar.turn_left()

        -----------------------------------------
        Sample code below:
        """
        self.avatar.move()
        self.avatar.pause(0.25)
        self.avatar.move()
        self.avatar.pause(0.25)
        self.avatar.turn_left()
        print([self.avatar.location_x, self.avatar.location_y])


if __name__ == '__main__':
    # Initialize Maze GUI
    my_gui = MazeGui()
