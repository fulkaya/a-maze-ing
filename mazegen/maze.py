import random


class Cell():

    def __init__(self, north: bool, east: bool, south: bool, west: bool):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.is_visited = False

    def sum(self):
        return self.north + self.east + self.south + self.west


class Maze():

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
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
        GREEN = "\033[92m"
        RESET = "\033[0m"
        path = set(self.solve_bfs())
        for y, row in enumerate(self.grid):
            if row:
                first_cell = row[0]
                for cell in row:
                    if cell is first_cell:
                        print("+", end="")
                    if cell.north == 1:
                        print("---+", end="")
                    else:
                        print("   +", end="")
                print()

                for x, cell in enumerate(row):
                    if cell.west == 1 and cell is first_cell:
                        print("|", end="")
                    if (x, y) in path:
                        print(f"{GREEN} * {RESET}", end="")
                    else:
                        print("   ", end="")

                    if cell.east == 1:
                        print("|", end="")
                    else:
                        print(" ", end="")
                print()

        last_cell = self.grid[-1]
        for cell in last_cell:
            if cell.south == 1 and cell is first_cell:
                print("+", end="")
            print("---+", end="")
        print()

    def break_wall(self):
        current_pos: tuple[int, int] = (0, 0)

        new_list: list[tuple[int, int]] = [current_pos]

        while new_list:
            way_list: list[tuple[int, int]] = []
            x, y = current_pos

            current_pos_north: tuple = x, y - 1
            current_pos_south: tuple = x, y + 1
            current_pos_west: tuple = x - 1, y
            current_pos_east: tuple = x + 1, y

            self.grid[y][x].is_visited = True

            if (
                0 <= current_pos_north[0] < self.width and
                0 <= current_pos_north[1] < self.height and not
                self.grid[current_pos_north[1]][current_pos_north[0]]
                .is_visited
            ):
                way_list.append(current_pos_north)

            if (
                0 <= current_pos_south[0] < self.width and
                0 <= current_pos_south[1] < self.height and not
                self.grid[current_pos_south[1]][current_pos_south[0]]
                .is_visited
            ):
                way_list.append(current_pos_south)

            if (
                0 <= current_pos_west[0] < self.width and
                0 <= current_pos_west[1] < self.height and
                not self.grid[current_pos_west[1]][current_pos_west[0]]
                .is_visited
            ):
                way_list.append(current_pos_west)

            if (
                0 <= current_pos_east[0] < self.width and
                0 <= current_pos_east[1] < self.height and not
                self.grid[current_pos_east[1]][current_pos_east[0]]
                .is_visited
            ):
                way_list.append(current_pos_east)

            if way_list:
                selected_pos = random.choice(way_list)
                nx, ny = selected_pos
                if selected_pos == current_pos_north:
                    self.grid[y][x].north = 0
                    self.grid[ny][nx].south = 0
                if selected_pos == current_pos_south:
                    self.grid[y][x].south = 0
                    self.grid[ny][nx].north = 0
                if selected_pos == current_pos_west:
                    self.grid[y][x].west = 0
                    self.grid[ny][nx].east = 0
                if selected_pos == current_pos_east:
                    self.grid[y][x].east = 0
                    self.grid[ny][nx].west = 0
                current_pos = selected_pos
                new_list.append(current_pos)
            else:
                new_list.pop()
                if new_list:
                    current_pos = new_list[-1]

    def remove_dead_ends(self):
        while True:
            changed = False

            for y in range(self.height):
                for x in range(self.width):
                    way_list: list[str] = []
                    if self.grid[y][x].sum() == 3:

                        if x - 1 >= 0 and self.grid[y][x].west == 1:
                            way_list.append('W')

                        if x + 1 < self.width and self.grid[y][x].east == 1:
                            way_list.append('E')

                        if y - 1 >= 0 and self.grid[y][x].north == 1:
                            way_list.append('N')

                        if y + 1 < self.height and self.grid[y][x].south == 1:
                            way_list.append('S')

                        if way_list:
                            selected_way = random.choice(way_list)

                            if selected_way == 'W':
                                self.grid[y][x].west = 0
                                self.grid[y][x - 1].east = 0
                            if selected_way == 'E':
                                self.grid[y][x].east = 0
                                self.grid[y][x + 1].west = 0
                            if selected_way == 'N':
                                self.grid[y][x].north = 0
                                self.grid[y - 1][x].south = 0
                            if selected_way == 'S':
                                self.grid[y][x].south = 0
                                self.grid[y + 1][x].north = 0

                            changed = True

            if not changed:
                break

    def solve_bfs(self) -> list[tuple[int, int]]:
        start: tuple[int, int] = (0, 0)
        finish: tuple[int, int] = (self.width - 1, self.height - 1)
        choices: list[list[tuple[int, int]]] = [[start]]
        visited: list[tuple[int, int]] = [start]

        while choices:
            current_path = choices.pop(0)
            current_pos = current_path[-1]
            x, y = current_pos
            way_list: list[str] = []
            current_pos_east = x + 1, y
            current_pos_west = x - 1, y
            current_pos_north = x, y - 1
            current_pos_south = x, y + 1

            if current_pos != finish:
                if self.grid[y][x].east == 0 and current_pos_east not in visited:
                    way_list.append('E')
                if self.grid[y][x].west == 0 and current_pos_west not in visited:
                    way_list.append('W')
                if self.grid[y][x].north == 0 and current_pos_north not in visited:
                    way_list.append('N')
                if self.grid[y][x].south == 0 and current_pos_south not in visited:
                    way_list.append('S')

                if 'E' in way_list:
                    choices.append(current_path + [current_pos_east])
                if 'W' in way_list:
                    choices.append(current_path + [current_pos_west])
                if 'N' in way_list:
                    choices.append(current_path + [current_pos_north])
                if 'S' in way_list:
                    choices.append(current_path + [current_pos_south])
                visited.append(current_pos)
            else:
                return current_path
        return []
