import sys

try:
    import a_maze_ing
    from mazegen import Maze
except ModuleNotFoundError as e:
    print(e)
    sys.exit()


class Choices:
    open: bool = True
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
            return

        if choice == "4":
            pass

        else:
            print("\nPlease enter a valid input\n")
            self.choices(maze)
            return
