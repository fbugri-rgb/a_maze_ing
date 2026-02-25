"""
Module for formatting and exporting the maze.
"""

from typing import List, Tuple


class MazeExporter:
    """Handles exporting the maze to the required file format."""

    def __init__(
        self,
        grid: List[List[int]],
        entry: Tuple[int, int],
        exit_pos: Tuple[int, int],
        path: str
    ) -> None:
        """Initializes the exporter with maze data."""
        self.grid = grid
        self.entry = entry
        self.exit_pos = exit_pos
        self.path = path

    def export(self, filename: str) -> None:
        """
        Writes the maze data to a file in hexadecimal format.

        Args:
            filename: The target output file path.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                # Write grid row by row using hexadecimal digits
                for row in self.grid:
                    # f"{cell:X}" format the integer to an uppercase Hex string
                    row_hex = "".join(f"{cell:X}" for cell in row)
                    file.write(f"{row_hex}\n")

                # After an empty line, insert entry, exit, and path
                file.write("\n")
                file.write(f"{self.entry[0]},{self.entry[1]}\n")
                file.write(f"{self.exit_pos[0]},{self.exit_pos[1]}\n")
                file.write(f"{self.path}\n")

        except IOError as e:
            print(f"Error: Could not write to file '{filename}'. Details: {e}")
