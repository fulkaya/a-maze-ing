try:
    from mazegen import Maze
except ModuleNotFoundError as e:
    print(e)


def path_str(path: list[tuple[int, int]]) -> str:
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


def display(maze: Maze) -> None:
    hex = "0123456789abcdef"

    with open("output_maze.txt", "w") as f:

        for line in maze.grid:
            for cell in line:
                print(hex[cell.hex_sum()], file=f, end="")
            print(file=f)

        print(file=f)
        print(maze.entry, file=f)
        print(maze.exit, file=f)
        print(file=f)
        print(path_str(maze.path), file=f)
