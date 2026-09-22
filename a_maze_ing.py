import sys

try:
    from mazegen import Maze
    import configuration
    import interactions
    import output
    from pydantic import ValidationError
except ModuleNotFoundError as e:
    print(e)
    sys.exit()


def main() -> None:
    if len(sys.argv) != 2:
        return

    try:
        values = configuration.parse(sys.argv[1])
        grid = Maze(values)
        grid.break_wall()
        if values.perfect is False:
            grid.remove_dead_ends()
        grid.display()
        output.display(grid)
        menu = interactions.Choices()
        menu.choices(grid)

    except ValidationError as e:
        print(ValidationError.errors(e)[0]["msg"].strip("Value error, "))

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
