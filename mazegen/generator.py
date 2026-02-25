"""
Core module for generating mazes using the Recursive Backtracker algorithm.
"""

import random
from typing import Dict, Any, List, Tuple, Set
from .solver import MazeSolver
from .formatters import MazeExporter


class MazeGenerator:
    """
    A class to generate and manage a maze structure.
    """

    # Hexadecimal wall values based on the project requirements
    WALL_N = 1  # 0001 (Bit 0)
    WALL_E = 2  # 0010 (Bit 1)
    WALL_S = 4  # 0100 (Bit 2)
    WALL_W = 8  # 1000 (Bit 3)
    ALL_WALLS = WALL_N | WALL_E | WALL_S | WALL_W  # 15

    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initializes the MazeGenerator with the given configuration.

        Args:
            config: Dictionary containing maze generation parameters.
        """
        self.width: int = config.get('WIDTH', 20)
        self.height: int = config.get('HEIGHT', 15)
        self.entry: Tuple[int, int] = config.get('ENTRY', (0, 0))

        default_exit = (self.width - 1, self.height - 1)
        self.exit: Tuple[int, int] = config.get('EXIT', default_exit)
        self.is_perfect: bool = config.get('PERFECT', True)

        # Optional: Allow seeding for reproducibility
        if 'SEED' in config:
            random.seed(config['SEED'])

        # Initialize grid with all walls closed (value 15)
        self.grid: List[List[int]] = [
            [self.ALL_WALLS for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.visited: Set[Tuple[int, int]] = set()

    def _embed_42(self) -> None:
        """
        Reserves cells to form a '42' pattern in the center of the maze.
        Marked cells remain closed. Prints an error if the grid is too small.
        """
        # The pattern requires at least 7x5, plus a border to remain solvable
        if self.width < 10 or self.height < 7:
            print("Error: Maze too small to embed '42' pattern.")
            return

        # Base 0-indexed pattern for '42' (7 cells wide, 5 cells high)
        base_pattern = [
            # The '4' shape
            (0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1),
            (2, 2), (2, 3), (2, 4),
            # The '2' shape
            (4, 0), (5, 0), (6, 0), (6, 1), (6, 2), (5, 2),
            (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)
        ]

        # Calculate offsets to perfectly center the pattern
        offset_x = (self.width - 7) // 2
        offset_y = (self.height - 5) // 2

        for dx, dy in base_pattern:
            x = offset_x + dx
            y = offset_y + dy
            # Ensure the coordinates stay within bounds just in case
            if 0 <= x < self.width and 0 <= y < self.height:
                self.visited.add((x, y))

    def generate(self) -> None:
        """
        Generates the maze layout using an iterative Recursive Backtracker.
        """
        self._embed_42()

        start_x, start_y = self.entry

        if (start_x, start_y) in self.visited:
            start_x, start_y = (0, 0)
            while (start_x, start_y) in self.visited:
                start_x += 1

        stack: List[Tuple[int, int]] = [(start_x, start_y)]
        self.visited.add((start_x, start_y))

        # Map directions: (dx, dy, wall_to_remove, opposite_wall_to_remove)
        directions = [
            (0, -1, self.WALL_N, self.WALL_S),
            (1, 0, self.WALL_E, self.WALL_W),
            (0, 1, self.WALL_S, self.WALL_N),
            (-1, 0, self.WALL_W, self.WALL_E)
        ]

        while stack:
            cx, cy = stack[-1]
            unvisited_neighbors = []

            for dx, dy, wall, opp_wall in directions:
                nx, ny = cx + dx, cy + dy

                # Check grid bounds and if the neighbor is unvisited
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in self.visited:
                        unvisited_neighbors.append((nx, ny, wall, opp_wall))

            if unvisited_neighbors:
                # Randomly choose an available neighbor
                nx, ny, wall, opp_wall = random.choice(unvisited_neighbors)

                # Tear down the walls between current cell and chosen neighbor
                self.grid[cy][cx] &= ~wall
                self.grid[ny][nx] &= ~opp_wall

                self.visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                # Dead end reached, backtrack
                stack.pop()

        # If the maze doesn't need to be perfect, tear down a few extra walls
        if not self.is_perfect:
            self._make_imperfect()

    def _make_imperfect(self) -> None:
        """Removes random walls to create loops for an imperfect maze."""
        loops_to_create = (self.width * self.height) // 20
        walls = [self.WALL_N, self.WALL_E, self.WALL_S, self.WALL_W]

        for _ in range(loops_to_create):
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if (x, y) not in self.visited:
                continue

            # Randomly remove an internal wall
            direction = random.choice(walls)
            self.grid[y][x] &= ~direction

    def export_to_file(self, filename: str) -> None:
        """
        Exports the generated maze to a file using hex representation.

        Args:
            filename: The path to the output text file.
        """

        # Find the shortest path
        solver = MazeSolver(
            self.grid, self.width, self.height, self.entry, self.exit
        )
        shortest_path = solver.find_shortest_path()

        # Export everything to the file
        exporter = MazeExporter(
            self.grid, self.entry, self.exit, shortest_path
        )
        exporter.export(filename)

        # TODO: Format output and find the shortest path
        pass
