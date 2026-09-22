import sys

try:
    import a_maze_ing
    from mazegen import Maze
except ModuleNotFoundError as e:
    print(e)
    sys.exit()


class Choices:
    open: bool = True
    color_index: int = 0
    colors: list[str] = [
        "\033[0m",   # Default
        "\033[91m",  # Red
        "\033[94m",  # Blue
        "\033[93m",  # Yellow
        "\033[95m",  # Magenta
        "\033[96m",  # Cyan
    ]

    def choices(self, maze: Maze) -> None:
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colours")
        print("4. Quit")

        choice = input("Choice? (1,4): ")

        if choice == "1":
            Choices.open = True
            a_maze_ing.main()
            return

        if choice == "2":
            Choices.open = not Choices.open
            maze.display()
            self.choices(maze)
            return

        if choice == "3":
            Choices.color_index = (Choices.color_index + 1
                                   ) % len(Choices.colors)
            maze.display()
            self.choices(maze)
            return

        if choice == "4":
            pass

        else:
            print("\nPlease enter a valid input\n")
            self.choices(maze)
            return
