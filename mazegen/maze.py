class Cell():

    def __init__(self, north, east, south, west):
        self.north = north
        self.east = east
        self.south = south
        self.west = west

    def sum(self):
        return self.north + self.east + self.south + self.west


class Maze():

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid: list[list[Cell]] = self.create_grid()

    def create_grid(self):
        grid: list[list[Cell]] = []

        for _ in range(self.height):
            row: list[Cell] = []
            for _ in range(self.width):
                cell = Cell(1, 1, 1, 1)
                row.append(cell)
            grid.append(row)
        return grid

    def display(self):
        for row in self.grid:
            if row:
                first_cell = row[0]
                for cell in row:
                    if cell.north == 1 and cell is first_cell:
                        print("+", end="")
                    print("---+", end="")
                print()

                for cell in row:
                    if cell.west == 1 and cell is first_cell:
                        print("|", end="")
                    if cell.east == 1:
                        print("   |", end="")
                print()

        last_cell = self.grid[-1]
        for cell in last_cell:
            if cell.south == 1 and cell is first_cell:
                print("+", end="")
            print("---+", end="")
        print()
