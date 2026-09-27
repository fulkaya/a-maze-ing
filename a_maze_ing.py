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
        if values.perfect is False:
            grid.remove_dead_ends()
        display(grid)
        output.output(grid, values.output_file)
        menu = interactions.Choices()
        menu.choices(grid)

    except ValidationError as e:
        print(ValidationError.errors(e)[0]["msg"].strip("Value error, "))

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
