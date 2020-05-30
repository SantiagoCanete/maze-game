import maze


class MazeSolver:
    def __init__(self, maze_grid, avatar):
        self.maze = maze_grid
        self.avatar = avatar

    def my_solver(self):
        print(self.avatar)


if __name__ == '__main__':
    # Initialize Maze GUI
    my_gui = maze.MazeGui()

