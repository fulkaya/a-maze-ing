"""Entry point for the A-Maze-ing CLI application.

Loads maze generation configurations from a file, constructs the grid,
handles wall carving and braiding logic, displays the maze in terminal,
serializes output, and initiates user interactions.
"""

import sys
import os

try:
    from mazegen import Maze
    from display import display
    import configuration
    import interactions
    import output
    from pydantic import ValidationError
except ModuleNotFoundError as e:
    print(e)
    print("To install the module run: 'make install'")
    sys.exit()


def main() -> None:
    """Parse CLI arguments, initialize the maze, and trigger the UI loop.

    Validates command-line arguments, parses the configuration file,
    instantiates the Maze object, runs path-carving algorithms, displays the
    grid, writes hex output to disk, and opens the interactive menu.
    """
    if len(sys.argv) != 2:
        py_cmd = os.path.basename(sys.executable)
        print(f"Usage: {py_cmd} {sys.argv[0]} <config_file>")
        return

    try:
        values = configuration.parse(sys.argv[1])
        grid = Maze(
            width=values.width,
            height=values.height,
            entry=values.entry,
            exit=values.exit,
            seed=values.seed,
            perfect=values.perfect
        )
        grid.break_wall()
        if not values.perfect:
            grid.remove_dead_ends()
        display(grid)
        output.output(grid, values.output_file)
        menu = interactions.Choices()
        menu.choices(grid, values)

    except KeyboardInterrupt:
        print()

    except ValidationError as e:
        print(ValidationError.errors(e)[0]["msg"].strip("Value error, "))

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
