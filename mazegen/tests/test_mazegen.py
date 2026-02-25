"""
Unit tests for the mazegen package.
"""

import unittest
import os
from typing import Dict, Any

from mazegen import MazeGenerator, MazeSolver, MazeExporter


class TestMazeGenerator(unittest.TestCase):
    """Tests for the MazeGenerator class."""

    def setUp(self) -> None:
        """Set up a basic configuration for testing."""
        self.config: Dict[str, Any] = {
            'WIDTH': 10,
            'HEIGHT': 10,
            'ENTRY': (0, 0),
            'EXIT': (9, 9),
            'PERFECT': True,
            'SEED': 42
        }
        self.generator = MazeGenerator(self.config)

    def test_initialization(self) -> None:
        """Test if the generator initializes correctly with config."""
        self.assertEqual(self.generator.width, 10)
        self.assertEqual(self.generator.height, 10)
        self.assertEqual(len(self.generator.grid), 10)
        self.assertEqual(len(self.generator.grid[0]), 10)
        # 15 means all walls are closed (1 | 2 | 4 | 8)
        self.assertEqual(self.generator.grid[0][0], 15)

    def test_generate_perfect(self) -> None:
        """Test that the generation runs and populates the visited set."""
        self.generator.generate()
        # Ensure the grid was traversed
        self.assertTrue(len(self.generator.visited) > 0)


class TestMazeSolver(unittest.TestCase):
    """Tests for the MazeSolver class."""

    def test_shortest_path(self) -> None:
        """
        Test the BFS solver on a simple predefined 2x2 grid.
        Bits: 1=N, 2=E, 4=S, 8=W. 0 means open.
        """
        # 2x2 Grid setup:
        # (0,0): W, N closed (8+1=9), E, S open
        # (1,0): N, E closed (1+2=3), W, S open
        # (0,1): W, S closed (8+4=12), N, E open
        # (1,1): E, S closed (2+4=6), N, W open
        grid = [
            [9, 3],
            [12, 6]
        ]
        solver = MazeSolver(grid, 2, 2, (0, 0), (1, 1))

        # Valid shortest path can be E then S (ES) or S then E (SE)
        path = solver.find_shortest_path()
        self.assertIn(path, ["ES", "SE"])

    def test_unsolvable_maze(self) -> None:
        """Test that the solver returns an empty string if blocked."""
        grid = [
            [15, 15],  # Fully closed walls
            [15, 15]
        ]
        solver = MazeSolver(grid, 2, 2, (0, 0), (1, 1))
        self.assertEqual(solver.find_shortest_path(), "")


class TestMazeExporter(unittest.TestCase):
    """Tests for the MazeExporter class."""

    def test_export_format(self) -> None:
        """Test if the exported text file matches required hex format."""
        grid = [
            [9, 3],
            [12, 6]
        ]
        exporter = MazeExporter(grid, (0, 0), (1, 1), "ES")
        test_file = "test_output.txt"

        # Export the dummy grid
        exporter.export(test_file)

        # Read back and verify
        with open(test_file, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        self.assertEqual(lines[0], "93")
        # 12 is 'C' in Hex
        self.assertEqual(lines[1], "C6")
        self.assertEqual(lines[2], "")
        self.assertEqual(lines[3], "0,0")
        self.assertEqual(lines[4], "1,1")
        self.assertEqual(lines[5], "ES")

        # Clean up the test artifact
        if os.path.exists(test_file):
            os.remove(test_file)


if __name__ == "__main__":
    unittest.main()
