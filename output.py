"""Output serialization module for the A-Maze-ing project.

Handles encoding maze cell wall configurations into hexadecimal
representations, translating step-by-step path coordinates into
directional string sequences, and writing final representations
to text files according to 42 specifications.
"""

try:
    from mazegen import Maze
except ModuleNotFoundError as e:
    print(e)


def path_str(path: list[tuple[int, int]]) -> str:
    """Convert an ordered coordinate path into a cardinal direction
    sequence string.

    Iterates over successive coordinate pairs and maps transitions to
    'N' (North), 'S' (South), 'E' (East), or 'W' (West).

    Args:
        path: List of (x, y) coordinates representing the maze traversal.

    Returns:
        A string composed of cardinal direction characters (e.g., 'EESSWNN').
    """
    direction: str = ""

    for index, cell in enumerate(path):
        if index < len(path) - 1:
            next_cell = path[index + 1]

            if next_cell[0] > cell[0]:
                direction += 'E'

            elif next_cell[0] < cell[0]:
                direction += 'W'

            elif next_cell[1] > cell[1]:
                direction += 'S'

            elif next_cell[1] < cell[1]:
                direction += 'N'

    return direction


def output(maze: Maze, filename: str) -> None:
    """Serialize the generated maze and its solution into a text file.

    Writes the hexadecimal bitmask representation of all maze cells line
    by line, followed by an empty line, entry coordinates, exit coordinates,
    and the cardinal direction sequence representing the shortest path.

    Args:
        maze: The solved or configured Maze instance to be serialized.
        filename: Destination path of the output text file.
    """
    hex = "0123456789abcdef"

    with open(filename, "w") as f:

        for line in maze.grid:
            for cell in line:
                print(hex[cell.hex_sum()], file=f, end="")
            print(file=f)

        print(file=f)
        print(f"{maze.entry[0]},{maze.entry[1]}", file=f)
        print(f"{maze.exit[0]},{maze.exit[1]}", file=f)
        print(path_str(maze.path), file=f)
