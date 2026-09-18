from mazegen import Maze


if __name__ == "__main__":
    grid = Maze(8, 6, (0, 0), (7, 5))
    grid.break_wall()
    grid.remove_dead_ends()
    grid.display()
