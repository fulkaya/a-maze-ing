"""Terminal visualization module for rendering maze grids and solution paths.

Renders cell walls, borders, entrance/exit markers, embedded logos, and active
solution paths using ANSI color sequences in the terminal.
"""

from mazegen import Maze


def display(maze: Maze) -> None:
    """Render the maze grid, walls, special points, and solution
    path to stdout.

    Iterates over each row and cell of the maze to construct horizontal and
    vertical walls, marks the entry and exit coordinates with flag symbols,
    renders embedded 42 logo blocks if enabled, and traces the solution path
    using ANSI color codes based on current UI state.

    Args:
        maze: The Maze instance to be displayed.
    """
    from interactions import Choices
    GREEN = "\033[92m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
    WALL = Choices.colors[Choices.color_index]
    path = set(maze.solve_bfs())
    for y, row in enumerate(maze.grid):
        if row:
            first_cell = row[0]
            for cell in row:
                if cell is first_cell:
                    print(f"{WALL}+{RESET}", end="")
                if cell.north == 1:
                    print(f"{WALL}---+{RESET}", end="")
                else:
                    print(f"{WALL}   +{RESET}", end="")
            print()

            for x, cell in enumerate(row):
                if cell.west == 1 and cell is first_cell:
                    print(f"{WALL}|{RESET}", end="")
                if (x, y) == maze.entry:
                    print("🇸​​​​  ", end="")
                elif (x, y) == maze.exit:
                    print("🇫  ", end="")
                elif (x, y) in maze.logo_cells and maze.logo:
                    print(f"{WHITE}███{RESET}", end="")
                elif (x, y) in path and Choices.open is True:
                    print(f"{GREEN} * {RESET}", end="")
                else:
                    print("   ", end="")

                if cell.east == 1:
                    print(f"{WALL}|{RESET}", end="")
                else:
                    print(" ", end="")
            print()

    last_cell = maze.grid[-1]
    for cell in last_cell:
        if cell.south == 1 and cell is first_cell:
            print(f"{WALL}+{RESET}", end="")
        print(f"{WALL}---+{RESET}", end="")
    print()
