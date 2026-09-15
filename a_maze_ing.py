from mazegen import Maze


if __name__ == "__main__":
    grid = Maze(20, 15)
    grid.break_wall()
    grid.remove_dead_ends()
    grid.display()
