from mazegen import Maze


if __name__ == "__main__":
    grid = Maze(5, 5)
    grid.break_wall()
    grid.display()
    grid.remove_dead_ends()
    grid.display()
