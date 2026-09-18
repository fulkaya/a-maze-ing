from mazegen import Maze
import sys
import configuration


def main():
    if len(sys.argv) != 2:
        return

    try:
        values = configuration.parse(sys.argv[1])
    except Exception as e:
        print(e)
        return

    grid = Maze(values)
    grid.break_wall()
    grid.remove_dead_ends()
    grid.display()


if __name__ == "__main__":
    main()
