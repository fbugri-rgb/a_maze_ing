"""
Module for solving mazes and finding the shortest path.
"""

from typing import List, Tuple
from collections import deque


class MazeSolver:
    """Solves a generated maze to find the shortest path."""

    # Wall bitmasks
    WALL_N = 1
    WALL_E = 2
    WALL_S = 4
    WALL_W = 8

    def __init__(
        self,
        grid: List[List[int]],
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit_pos: Tuple[int, int]
    ) -> None:
        """Initializes the solver with grid and coordinate data."""
        self.grid = grid
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_pos = exit_pos

    def find_shortest_path(self) -> str:
        """
        Finds the shortest path from entry to exit using BFS.

        Returns:
            A string of directions (e.g., 'NNEESW').
        """
        # Queue stores tuples of (current_x, current_y, path_string)
        queue: deque[Tuple[int, int, str]] = deque([
            (self.entry[0], self.entry[1], "")
        ])
        visited = {self.entry}

        # Directions: (dx, dy, wall_flag, direction_char)
        directions = [
            (0, -1, self.WALL_N, 'N'),
            (1, 0, self.WALL_E, 'E'),
            (0, 1, self.WALL_S, 'S'),
            (-1, 0, self.WALL_W, 'W')
        ]

        while queue:
            cx, cy, path = queue.popleft()

            if (cx, cy) == self.exit_pos:
                return path

            current_cell = self.grid[cy][cx]

            for dx, dy, wall, char in directions:
                nx, ny = cx + dx, cy + dy

                # Check grid bounds
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # Check if the wall in this direction is open (bit is 0)
                    if (current_cell & wall) == 0:
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            queue.append((nx, ny, path + char))

        return ""  # Return an empty string if no path is found
