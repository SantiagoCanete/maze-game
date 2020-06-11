import random


class MazeBuilder:
    """
    --------------------------------------------------------------------------------------------------------------------
    The MazeBuilder class generates a random maze using the Depth-First algorithm.
    --------------------------------------------------------------------------------------------------------------------
    List of methods in class:
        - Class constructor: __init__(num_rows, num_columns, init_row=0, init_column=0)
        - Generate maze: make_maze()
        - Save maze as image: write_svg(filename)
    --------------------------------------------------------------------------------------------------------------------
    """

    def __init__(self, num_rows, num_columns, init_row=0, init_column=0):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.__init_row = init_row
        self.__init_column = init_column
        self.grid = []
        self.maze = []

        print("Maze constructor called.")

    def make_maze(self):
        """make_maze given a number of rows and columns and an initial location in the maze"""

        # Get total number of cells in maze
        total_cells = self.num_columns * self.num_rows

        # Initialize a grid where all cells have four walls and ar unvisited.
        self.grid = [[Cell(cols, rows) for rows in range(self.num_rows)] for cols in range(self.num_columns)]

        # Define initial cell
        current_cell = [self.grid[self.__init_column][self.__init_row].x,
                        self.grid[self.__init_column][self.__init_row].y]

        # Initialize number of cells visited and stack
        visited_stack = []
        cells_visited = 1

        # Mark initial cell as visited
        self.grid[self.__init_column][self.__init_row].mark_visited()

        # Generate random paths through the maze until all cells have been visited
        while cells_visited < total_cells:
            # Find an available random direction
            available_directions = self._get_available_directions(current_cell)
            direction = self._generate_random_direction(available_directions)

            if direction:
                # Remove wall from current cell
                self.grid[current_cell[0]][current_cell[1]].remove_wall(direction)

                # Define new current cell
                current_cell = [self.grid[current_cell[0] + direction[0]][current_cell[1] + direction[1]].x,
                                self.grid[current_cell[0] + direction[0]][current_cell[1] + direction[1]].y]

                visited_stack.append(current_cell)

                # Remove walls of new cell from previous cell
                self.grid[current_cell[0]][current_cell[1]].remove_wall([-direction[0], -direction[1]])

            else:
                current_cell = visited_stack.pop()
                continue

            # Mark new current cell as visited and add to stack
            self.grid[current_cell[0]][current_cell[1]].mark_visited()

            # Increase the number of cells visited
            cells_visited += 1

        # Save the final maze in a variable
        self.maze = self.grid

        print("New maze generated.")

    @staticmethod
    def _generate_random_direction(directions):
        """Randomize a set of possible directions and return one"""

        # Initialize new direction list. IDE complains if not set before hand
        new_direction = []

        # Check if any available directions have been found
        if directions:
            random.shuffle(directions)
            select_direction = directions[0]

            if select_direction == 1:
                new_direction = [1, 0]
            elif select_direction == 2:
                new_direction = [-1, 0]
            elif select_direction == 3:
                new_direction = [0, 1]
            elif select_direction == 4:
                new_direction = [0, -1]

        return new_direction

    def _get_available_directions(self, current_cell):
        """Get a random direction from current cell that has not been visited and is inside the given grid"""

        # Initialize an empty array of available directions if no directions are available the array will remain empty
        available_directions = []

        # Append an integer for each direction that is available
        if self._check_if_in_maze(current_cell[0] + 1, current_cell[1]) and not self._check_if_visited(
                current_cell[0] + 1,
                current_cell[1]):
            available_directions.append(1)
        if self._check_if_in_maze(current_cell[0] - 1, current_cell[1]) and not self._check_if_visited(
                current_cell[0] - 1,
                current_cell[1]):
            available_directions.append(2)
        if self._check_if_in_maze(current_cell[0], current_cell[1] + 1) and not self._check_if_visited(current_cell[0],
                                                                                                       current_cell[
                                                                                                           1] + 1):
            available_directions.append(3)
        if self._check_if_in_maze(current_cell[0], current_cell[1] - 1) and not self._check_if_visited(current_cell[0],
                                                                                                       current_cell[
                                                                                                           1] - 1):
            available_directions.append(4)

        return available_directions

    def _check_if_in_maze(self, check_col, check_row):
        """Check if a cell is inside the given grid"""

        is_in_maze = False
        if 0 <= check_row <= (self.num_rows - 1) and 0 <= check_col <= (self.num_columns - 1):
            is_in_maze = True

        return is_in_maze

    def _check_if_visited(self, check_col, check_row):
        """Check if a cell has already been visited"""

        is_visited = False
        if self.grid[check_col][check_row].visited:
            is_visited = True

        return is_visited


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'South': 1, 'North': 1, 'East': 1, 'West': 1}
        self.visited = 0
        self.avatar_visited = 0

    def remove_wall(self, direction):
        if direction[0] == 1:
            self.walls['East'] = 0
        elif direction[0] == -1:
            self.walls['West'] = 0
        elif direction[1] == 1:
            self.walls['South'] = 0
        elif direction[1] == -1:
            self.walls['North'] = 0

    def mark_visited(self):
        self.visited = 1
