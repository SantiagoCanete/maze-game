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
            self.avatar.move() -> Avatar will move forward by one cell
            self.avatar.turn_left() -> Avatar will turn left by 90 degrees
            self.avatar.check_obstacle() -> Will return True if obstacle in front
            self.avatar.check_visited() -> Will return True if cell in front has been visited
            self.avatar.orientation -> Will return the orientation of the avatar (e.g. North, South...)
            self.avatar.location_x -> Will return the x location of the avatar
            self.avatar.location_y -> Will return the y location of the avatar
            self.avatar.pause(period) -> Will pause the scene so you have time to see the avatar move
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
