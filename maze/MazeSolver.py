from maze import MazeGui


class MazeSolver:
    def __init__(self, maze_grid, avatar):
        self.maze = maze_grid
        self.avatar = avatar

    def my_solver(self):
        # Write your maze solver here.
        #
        self.avatar.move()
        self.avatar.pause(40.0 / 1000.0)
        self.avatar.move()
        self.avatar.pause(40.0 / 1000.0)
        self.avatar.turn_left()


if __name__ == '__main__':
    # Initialize Maze GUI
    my_gui = MazeGui()
