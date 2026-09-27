# Mazegen

A standalone Python 3 module for procedural 2D maze generation and pathfinding.

## Installation

Install the wheel package directly using pip:

```bash
pip install mazegen-0.1.0-py3-none-any.whl
```

### Quick Start & Usage

```python
from mazegen import Maze

# 1. Instantiate the maze with custom parameters
# width, height, entry, exit, seed (optional), perfect (optional)
maze = Maze(
    width=21,
    height=15,
    entry=(0, 0),
    exit=(20, 14),
    seed=42,
    perfect=False
)

# 2. Carve paths through the grid
maze.break_wall()

# 3. For braided layouts with multiple paths (when perfect=False):
if not maze.perfect:
    maze.remove_dead_ends()

# 4. Access the generated grid structure
# maze.grid is a 2D list of Cell objects: [row][column]
cell = maze.grid[0][0]
print(f"Cell walls (N, E, S, W): {cell.north}, {cell.east}, {cell.south}, {cell.west}")
print(f"Cell 4-bit hex sum: {hex(cell.hex_sum())}")

# 5. Access the shortest path solution
solution_path = maze.solve_bfs()
print("Solution path coordinates:", solution_path)
```

### Configuration Parameters

* **`width`** (`int`): The horizontal size of the maze grid (number of columns). Must be a positive integer.
* **`height`** (`int`): The vertical size of the maze grid (number of rows). Must be a positive integer.
* **`entry`** (`tuple[int, int]`): The `(x, y)` coordinate pair defining the starting position on the grid.
* **`exit`** (`tuple[int, int]`): The `(x, y)` coordinate pair defining the destination target on the grid.
* **`perfect`** (`bool`, optional): Maze topology configuration (defaults to `True`):
  * `True`: Generates a standard spanning-tree maze with a single unique path between any two points and zero loops.
  * `False`: Braids the grid by stripping away dead ends to provide multiple alternative routes and loops (suitable for arcade layouts such as Pac-Man).
* **`seed`** (`int` | `None`, optional): Random seed value for deterministic generation. Defaults to `None` for pseudo-random mazes.

*** Note on Constraints: If the grid is large enough (width >= 9 and height >= 7), a centered '42' pattern is carved as an impassable obstacle. A ValueError is raised if entry or exit coordinates overlap with this logo pattern.

### Core Data Structures & Methods

* **`Cell`**: Represents an individual node within the maze grid, maintaining wall boundary states:
  * **`north`**, **`east`**, **`south`**, **`west`** (`int`): Directional wall states where `1` indicates a solid wall and `0` indicates an open passage.
  * **`sum()`** -> `int`: Returns the count of closed walls (ranging from `0` to `4`).
  * **`hex_sum()`** -> `int`: Computes a 4-bit integer mask (`0`–`15`) representing the cell's wall layout (North = 1, East = 2, South = 4, West = 8).

* **`Maze.grid`** (`list[list[Cell]]`):
  * A 2D list matrix indexed by row and column (`grid[y][x]`), providing direct programmatic access to the generated map topology.

* **`Maze.solve_bfs()`** -> `list[tuple[int, int]]`:
  * Solves the shortest path from `entry` to `exit` using Breadth-First Search (BFS).
  * Returns an ordered sequence of coordinate tuples `[(x1, y1), (x2, y2), ...]`, or an empty list if no valid route exists.

### License

This project is licensed under the MIT License.