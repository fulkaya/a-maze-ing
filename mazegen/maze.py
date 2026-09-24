import random
from configuration import Values


class Cell():

    def __init__(self, north: int, east: int, south: int, west: int):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.is_visited = False

    def sum(self) -> int:
        return self.north + self.east + self.south + self.west

    def hex_sum(self) -> int:
        return self.north * 1 + self.east * 2 + self.south * 4 + self.west * 8


class Maze():

    def __init__(self, values: Values):
        self.width: int = values.width
        self.height: int = values.height
        self.entry: tuple[int, int] = values.entry
        self.exit: tuple[int, int] = values.exit
        self.grid: list[list[Cell]] = self.create_grid()
        self.logo: bool = self.logo_bool()
        self.logo_cells: set[tuple[int, int]] = self.logo_42()
        self.path: list[tuple[int, int]] = []

        if values.entry in self.logo_cells or values.exit in self.logo_cells:
            raise ValueError(
                "The Entry or Exit coordinates overlap with the 42 logo "
                "pattern.\nPlease enter valid coordinates outside the logo."
            )

    def logo_bool(self) -> bool:
        if self.width >= 9 and self.height >= 7:
            return True
        return False

    def create_grid(self) -> list[list[Cell]]:
        grid: list[list[Cell]] = []

        for _ in range(self.height):
            row: list[Cell] = []
            for _ in range(self.width):
                cell = Cell(1, 1, 1, 1)
                row.append(cell)
            grid.append(row)
        return grid

    def display(self) -> None:
        from interactions import Choices
        GREEN = "\033[92m"
        WHITE = "\033[97m"
        RESET = "\033[0m"
        WALL = Choices.colors[Choices.color_index]
        path = set(self.solve_bfs())
        for y, row in enumerate(self.grid):
            if row:
                first_cell = row[0]
                for cell in row:
                    if cell is first_cell:
                        print(f"{WALL}+{RESET}", end="")
                    if cell.north == 1:
                        print(f"{WALL}---+{RESET}", end="")
                    else:
                        print(f"{WALL}   +{RESET}", end="")
                print()

                for x, cell in enumerate(row):
                    if cell.west == 1 and cell is first_cell:
                        print(f"{WALL}|{RESET}", end="")
                    if (x, y) == self.entry:
                        print("🇸​​​​  ", end="")
                    elif (x, y) == self.exit:
                        print("🇫  ", end="")
                    elif (x, y) in self.logo_cells and self.logo:
                        print(f"{WHITE}███{RESET}", end="")
                    elif (x, y) in path and Choices.open is True:    
                        print(f"{GREEN} * {RESET}", end="")
                    else:
                        print("   ", end="")

                    if cell.east == 1:
                        print(f"{WALL}|{RESET}", end="")
                    else:
                        print(" ", end="")
                print()

        last_cell = self.grid[-1]
        for cell in last_cell:
            if cell.south == 1 and cell is first_cell:
                print(f"{WALL}+{RESET}", end="")
            print(f"{WALL}---+{RESET}", end="")
        print()

    def break_wall(self) -> None:
        current_pos: tuple[int, int] = (0, 0)

        new_list: list[tuple[int, int]] = [current_pos]

        while new_list:
            way_list: list[tuple[int, int]] = []
            x, y = current_pos

            current_pos_north: tuple[int, int] = x, y - 1
            current_pos_south: tuple[int, int] = x, y + 1
            current_pos_west: tuple[int, int] = x - 1, y
            current_pos_east: tuple[int, int] = x + 1, y

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

    def remove_dead_ends(self) -> None:
        while True:
            changed = False

            for y in range(self.height):
                for x in range(self.width):
                    way_list: list[str] = []
                    if self.grid[y][x].sum() == 3:

                        if (x - 1 >= 0 and self.grid[y][x].west == 1
                                and ((x - 1, y) not in self.logo_cells
                                     if self.logo else True)):
                            way_list.append('W')

                        if (x + 1 < self.width and self.grid[y][x].east == 1
                                and ((x + 1, y) not in self.logo_cells
                                     if self.logo else True)):
                            way_list.append('E')

                        if (y - 1 >= 0 and self.grid[y][x].north == 1
                                and ((x, y - 1) not in self.logo_cells
                                     if self.logo else True)):
                            way_list.append('N')

                        if (y + 1 < self.height and self.grid[y][x].south == 1
                                and ((x, y + 1) not in self.logo_cells
                                     if self.logo else True)):
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
        start: tuple[int, int] = self.entry
        finish: tuple[int, int] = self.exit
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
                if (self.grid[y][x].east == 0 and
                        current_pos_east not in visited):
                    way_list.append('E')
                if (self.grid[y][x].west == 0 and
                        current_pos_west not in visited):
                    way_list.append('W')
                if (self.grid[y][x].north == 0 and
                        current_pos_north not in visited):
                    way_list.append('N')
                if (self.grid[y][x].south == 0 and
                        current_pos_south not in visited):
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
                self.path = current_path
                return current_path
        return []

    def logo_42(self) -> set[tuple[int, int]]:
        if not self.logo:
            return set()

        pattern = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]
        pattern_height = len(pattern)
        pattern_width = len(pattern[0])
        start_x = (self.width - pattern_width) // 2
        start_y = (self.height - pattern_height) // 2

        logo_cells: set[tuple[int, int]] = set()

        for y in range(start_y, start_y + pattern_height):
            for x in range(start_x, start_x + pattern_width):
                if pattern[y - start_y][x - start_x] == 1:
                    self.grid[y][x].is_visited = True
                    logo_cells.add((x, y))
                    self.grid[y][x].north = 1
                    self.grid[y][x].south = 1
                    self.grid[y][x].east = 1
                    self.grid[y][x].west = 1
        return logo_cells
