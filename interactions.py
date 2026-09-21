import sys

try:
    import a_maze_ing
except ModuleNotFoundError as e:
    print(e)
    sys.exit()


def choices() -> None:
    print("=== A-Maze-ing ===")
    print("1. Re-generate a new maze")
    print("2. Show / Hide the shortest path")
    print("3. Rotate the wall colours")
    print("4. Quit")

    choice = input("Choice? (1,4): ")

    if choice == "1":
        a_maze_ing.main()
        return

    if choice == "2":
        return

    if choice == "3":
        return

    if choice == "4":
        pass

    else:
        print("\nPlease enter a valid input\n")
        choices()
        return
