"""User interaction and interactive CLI menu module for A-Maze-ing.

Provides terminal menu options allowing users to toggle shortest path
visibility, cycle through ANSI wall color palettes, regenerate the maze,
or exit the program.
"""

import sys

try:
    import a_maze_ing
    from mazegen import Maze
    from display import display
except ModuleNotFoundError as e:
    print(e)
    sys.exit()


class Choices:
    """Handles CLI interactive menu state and user selections.

    Attributes:
        open: Flag controlling whether the shortest path is shown on
        the display.
        color_index: Current index pointer into the wall ANSI color list.
        colors: List of ANSI escape code sequences for wall color options.
    """
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
        """Display the interactive menu prompt and process user commands.

        Presents options to re-generate the maze, toggle path visibility,
        cycle wall colors, or exit. Recursively calls itself to maintain
        the interaction loop until the user decides to quit.

        Args:
            maze: The current active Maze instance.
        """
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
            display(maze)
            self.choices(maze)
            return

        if choice == "3":
            Choices.color_index = (Choices.color_index + 1
                                   ) % len(Choices.colors)
            display(maze)
            self.choices(maze)
            return

        if choice == "4":
            pass

        else:
            print("\nPlease enter a valid input\n")
            self.choices(maze)
            return
