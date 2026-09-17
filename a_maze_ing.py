from mazegen import Maze


if __name__ == "__main__":
    grid = Maze(20, 15, (0, 0), (19, 14))
    grid.break_wall()
    grid.remove_dead_ends()
    grid.display()
