*This project has been created as part of the 42 curriculum by fulkaya, mkangal.*

# A-Maze-ing

A configurable maze generator written in Python 3.10+ that generates perfect mazes or Pac-Man-style boards, computes the shortest path between an entrance and exit, renders the result in terminal ASCII, and exports the map into a standardized hexadecimal wall format.

## Description

The project produces procedural 2D mazes within a customizable rectangular grid while integrating the mandatory **"42"** pattern in the center.

It supports two distinct generation modes:
1. **Perfect Maze (`PERFECT=True`):** A spanning tree containing exactly one path between the entry and exit points, with zero loops.
2. **Pac-Man Board (`PERFECT=False`):** A fully connected, playable board featuring multiple independent loops, rare dead-ends, and open corridors at all four corners and the center.

The generated board can be displayed in the terminal with interactive options (re-generation, shortest path toggle, and color cycling) and is written to an output file using a 4-bit hexadecimal representation for adjacent walls.

## Instructions

### Requirements
- Python 3.10 or later
- Standard virtual environment (`venv`)

### Installation & Execution
Automate tasks directly using the provided `Makefile`:

1. **Install dependencies and local package:**

   ```bash
   make install
   ```
2. Runs `a_maze_ing.py` using `config.txt` by default. To pass a custom configuration file:
   ```bash
   make run CONFIG=path/to/custom_config.txt
   ```
3. Launches the program using the standard Python interactive debugger (`pdb`).
   ```bash
   make debug
   ```
4. Runs flake8 and mypy against project source files while strictly excluding .venv. 
	```bash
	make lint
	```
	For strict type checking:
	```bash
	make lint-strict
	```
5. Clears `__pycache__` and `.mypy_cache`
	```bash
	make clean
	```
	Cleans cache directories and removes `.venv` entirely
	```bash
	make fclean
	```

## Configuration File

The application reads configuration parameters formatted as `KEY=VALUE`. Blank lines and comment lines starting with `#` are safely ignored.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `WIDTH` | `int` | Yes | Total maze columns (must be >= 1) |
| `HEIGHT` | `int` | Yes | Total maze rows (must be >= 1) |
| `ENTRY` | `int,int` | Yes | Starting coordinates within maze bounds (`x,y`) |
| `EXIT` | `int,int` | Yes | Exit coordinates within maze bounds (`x,y`) |
| `OUTPUT_FILE` | `str` | Yes | Target file path for the serialized output |
| `PERFECT` | `bool` | No | `True` for spanning tree (no loops); `False` for braided/Pac-Man layout (default: `False`) |
| `SEED` | `int` | No | Integer seed for deterministic generation |

### Example `config.txt`

```ini
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
```

Note: If the maze dimensions are smaller than 9x7, a warning will be displayed indicating that the space is insufficient to embed the "42" logo.

## Algorithm Choice & Implementation

### Chosen Algorithm
We implemented **Randomized Depth-First Search (Recursive Backtracker)** for the baseline spanning tree generation, coupled with a custom **braiding pass (dead-end removal)** for the Pac-Man mode.

### Why This Algorithm?
- **High Carve Efficiency:** DFS guarantees that all reachable cells are visited, naturally forming a spanning tree (perfect maze) with zero unreachable islands.
- **Long Winding Paths:** It creates mazes with high branching factors and long corridors, making navigation and solving interesting.
- **Deterministic Seeding:** It integrates smoothly with Python's pseudo-random number generator (`random.seed`), ensuring fully reproducible maps when requested.
- **Braiding Flexibility:** Converting the spanning tree into a Pac-Man board simply required identifying dead-end cells (cells with 3 intact walls) and selectively removing adjacent walls to form cycles.

## Reusable Module (`mazegen`)

The core generation logic is decoupled from the CLI application and packaged as an independent wheel (`mazegen`):

- **Location:** Encapsulated inside the `mazegen/` directory with its own `pyproject.toml`.
- **Packaging:** Built using `setuptools` into a `.whl` distribution and installed via `make install`.
- **How to Reuse:** Third-party developers can install the wheel package and import the maze engine directly into any interface (GUI, web API, game engines):

  ```python
  from mazegen import Maze

  grid = Maze(width=20, height=15, entry=(0, 0), exit=(19, 14), seed=42)
  grid.break_wall()
  path = grid.solve_bfs()
  ```

## File Format & Serialization

The generated output file written to `OUTPUT_FILE` follows a strict structure:

### 1. Grid Bitmask
Each maze cell is represented by a single hexadecimal digit (`0` through `f`) representing the sum of its active walls:
* **Bit 0 (1):** North wall
* **Bit 1 (2):** East wall
* **Bit 2 (4):** South wall
* **Bit 3 (8):** West wall

*(e.g., a completely closed cell with all 4 walls equals 1 + 2 + 4 + 8 = 15, which is `f`)*

### 2. Delimiter
A single empty newline separates the grid from the trajectory data.

### 3. Coordinates & Solution Path
* **Line 1:** `entry_x,entry_y`
* **Line 2:** `exit_x,exit_y`
* **Line 3:** Shortest path directions using cardinal letters: `N` (North), `S` (South), `E` (East), and `W` (West).

## Interactive Menu

Once the maze is printed to the terminal, users can interact with it using terminal input:

1. **Re-generate a new maze:** Generates a new random maze using the existing configuration.
2. **Show / Hide the shortest path:** Toggles BFS shortest path markers (`*`) on the board.
3. **Rotate the wall colours:** Cycles through terminal ANSI wall colors (default, red, blue, yellow, magenta, cyan).
4. **Quit:** Exits the application loop.

## Team & Project Management

### Member Roles

- **fulkaya:**
  - Implemented the core maze architecture, algorithmic generation using Randomized DFS (Recursive Backtracker), and the BFS shortest-path solver.
  - Developed the `mazegen` package structure and ASCII grid rendering engine (`display.py`).
  - Implemented terminal interactive features (shortest-path toggle, maze regeneration, ANSI wall color rotation).

- **mkangal:**
  - Designed the structural configuration parsing pipeline (`configuration.py`) with input validation.
  - Implemented the terminal CLI loop and menu handlers (`interactions.py`).
  - Built the map serialization engine (`output.py`) to generate the standardized 4-bit hexadecimal output format.

- **Collaborative Work:**
  - Managed project dependencies and specification in `requirements.txt`.
  - Configured project licensing (`LICENSE.md`), packaging metadata (`pyproject.toml`), and created the base template `config.txt`.
  - Jointly coordinated local wheel (`.whl`) distribution workflow and packaging setup.
  - Collaborated on Makefile automation targets (`install`, `run`, `lint`, `clean`, `fclean`).
  - Co-authored project documentation across both `mazegen/README.md` and the root `README.md`.

### Planning & Evolution
- **Initial Plan:** 
  We initially planned to develop sequentially from the outside in—starting with the configuration parser before implementing the maze generation, while working simultaneously across the same codebase and testing scripts directly on our local host Python installations.

- **Workflow Evolution:** 
  We realized that testing inputs without a functional display engine was inefficient and that concurrent commits on the same files created integration bottlenecks. We pivoted to a core-first strategy: validating the maze generation and terminal rendering first with static parameters, while splitting the work clearly between the algorithmic engine (fulkaya) and the configuration/CLI infrastructure (mkangal). Concurrently, to eliminate "it works on my machine" issues and ensure clean, reproducible peer evaluations, we shifted from local host execution to fully automating an isolated `.venv` setup, dependency installation, and local wheel building directly inside the Makefile before integrating both components into the final pipeline.

### Retrospective: What Worked Well & What Could Be Improved
- **What Worked Well:**
  - Clear architectural decoupling between the core engine (`mazegen`) and the user interface (`a_maze_ing.py`), allowing parallel development without blocking each other.
  - Automating the workflow with `Makefile` (`make lint`, `make run`, `make install`), which ensured consistent local virtual environments and prevented style regressions early on.
- **What Could Be Improved:**
  - **Automated Unit Testing:** While manual CLI and configuration edge cases were tested, integrating an automated test suite (e.g., `pytest`) from day one would have streamlined regression testing.
  - **Graphical Interface (GUI):** As a future enhancement, supporting an optional graphical renderer (such as MiniLibX or Pygame) alongside the ANSI terminal display would provide a smoother visual representation for very large mazes.

### Specific Tools Used
- **Version Control & Collaboration:** Git, GitHub (branch management and code reviews).
- **Code Quality & Static Analysis:** `flake8` (PEP 8 style guide enforcement), `mypy` (strict static type checking).
- **Packaging & Automation:** GNU Make (workflow orchestration), `setuptools` & `wheel` (building the distributable package).
- **Debugging & Runtime:** Python Interactive Debugger (`pdb`), Python 3.10+ Virtual Environments (`venv`).

## Resources

### References
* [Think Labyrinth: Maze Algorithms](http://www.astrolog.org/labyrnth/algrithm.htm) - Comprehensive reference on maze generation classifications.
* [Randomized Depth-First Search Algorithm for Maze Generation](https://medium.com/@nacerkroudir/randomized-depth-first-search-algorithm-for-maze-generation-fb2d83702742) - Practical guide to grid carving and maze traversal.
* [Solving a Maze Using BFS and DFS](https://aiknowledgehub.in/solving-a-maze-using-bfs-and-dfs/) - Overview of pathfinding algorithms and shortest path retrieval.
* Python standard library documentation (`typing`, `sys`, `os`, `random`).
* [PEP 257](https://peps.python.org/pep-0257/) (Docstring Conventions) and [PEP 8](https://peps.python.org/pep-0008/) (Style Guide for Python Code).

### AI Usage Disclosure
Generative AI tools (LLMs) were consulted during the project for:
* Drafting PEP 257 compliant docstrings across all modules.
* Troubleshooting build configuration conflicts between `pyproject.toml` flat-layouts and Makefile linter exclusions.
* Refining `README.md` documentation to adhere strictly to the 42 evaluation rubric.


## License

Distributed under the MIT License. See [LICENSE.md](LICENSE.md) for full terms.
