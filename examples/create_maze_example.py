import maze


'''Create a simple maze'''

# Set maze size and starting location
number_rows = 30
number_cols = 30
init_row = 0
init_column = 0


# Use the __doc__ method to print the description of any method
print(maze.MazeBuilder.__doc__)

# Call the class constructor
my_maze_obj = maze.MazeBuilder(number_rows, number_cols, init_row, init_column)

# Call the make_maze method and generate a random maze of the given dimensions
my_maze_obj.make_maze()

# Extract the new maze
my_maze = my_maze_obj.maze

# Save maze as an image (SVG)
my_maze_obj.write_svg('maze.svg')
