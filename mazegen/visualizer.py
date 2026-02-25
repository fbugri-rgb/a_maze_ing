"""
Module for visualizing the maze in the terminal using ASCII characters.
"""

from typing import List, Dict, Any
from .generator import MazeGenerator
from .solver import MazeSolver


class TerminalVisualizer:
    """Handles the ASCII terminal visualization and user interaction."""

    # ANSI Color Codes
    COLORS = [
        '\033[97m',  # White
        '\033[91m',  # Red
        '\033[92m',  # Green
        '\033[93m',  # Yellow
        '\033[94m',  # Blue
        '\033[95m',  # Magenta
        '\033[96m',  # Cyan
    ]
    RESET = '\033[0m'

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initializes the visualizer with the current config."""
        self.config = config
        self.color_idx = 0
        self.show_path = False
        self.generator = MazeGenerator(self.config)
        self.shortest_path = ""
        self._generate_new_maze()

    def _generate_new_maze(self) -> None:
        """Generates a new maze and solves it."""
        self.generator = MazeGenerator(self.config)
        self.generator.generate()

        solver = MazeSolver(
            self.generator.grid,
            self.generator.width,
            self.generator.height,
            self.generator.entry,
            self.generator.exit
        )
        self.shortest_path = solver.find_shortest_path()

    def _build_canvas(self) -> List[List[str]]:
        """
        Builds a 2D text canvas of the maze.
        Returns a grid of characters.
        """
        w, h = self.generator.width, self.generator.height
        grid = self.generator.grid

        # Create a blank canvas of walls: (2*h + 1) by (2*w + 1)
        canvas = [['█' for _ in range(w * 2 + 1)] for _ in range(h * 2 + 1)]

        for y in range(h):
            for x in range(w):
                cy, cx = y * 2 + 1, x * 2 + 1
                canvas[cy][cx] = ' '  # The room itself

                cell = grid[y][x]
                if not (cell & MazeGenerator.WALL_N):
                    canvas[cy - 1][cx] = ' '
                if not (cell & MazeGenerator.WALL_S):
                    canvas[cy + 1][cx] = ' '
                if not (cell & MazeGenerator.WALL_E):
                    canvas[cy][cx + 1] = ' '
                if not (cell & MazeGenerator.WALL_W):
                    canvas[cy][cx - 1] = ' '

        # Mark Entry (S) and Exit (E)
        ey, ex = self.generator.entry[1] * 2 + \
            1, self.generator.entry[0] * 2 + 1
        canvas[ey][ex] = 'S'
        xy, xx = self.generator.exit[1] * 2 + 1, self.generator.exit[0] * 2 + 1
        canvas[xy][xx] = 'E'

        # Draw path if toggled
        if self.show_path and self.shortest_path:
            curr_x, curr_y = self.generator.entry
            for step in self.shortest_path:
                if step == 'N':
                    curr_y -= 1
                elif step == 'S':
                    curr_y += 1
                elif step == 'E':
                    curr_x += 1
                elif step == 'W':
                    curr_x -= 1

                # Mark path avoiding overwriting Entry/Exit chars
                py, px = curr_y * 2 + 1, curr_x * 2 + 1
                if canvas[py][px] not in ('S', 'E'):
                    canvas[py][px] = '·'

        return canvas

    def render(self) -> None:
        """Prints the canvas to the terminal with colors."""
        canvas = self._build_canvas()
        color = self.COLORS[self.color_idx]

        # Clear screen (optional, helps keep the terminal clean)
        print('\033[2J\033[H', end='')
        print("A-Maze-ing\n======\n")

        for row in canvas:
            line = ""
            for char in row:
                if char == '█':
                    line += f"{color}{char}{self.RESET}"
                elif char == 'S':
                    line += f"{self.COLORS[2]}{char}{self.RESET}"  # Green
                elif char == 'E':
                    line += f"{self.COLORS[1]}{char}{self.RESET}"  # Red
                elif char == '·':
                    line += f"{self.COLORS[4]}{char}{self.RESET}"  # Blue
                else:
                    line += char
            print(line)
        print()

    def run(self) -> None:
        """Main loop for user interaction."""
        while True:
            self.render()
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")

            choice = input("Choice? (1-4): ").strip()

            if choice == '1':
                # Remove seed to allow random generation on redraw
                if 'SEED' in self.config:
                    del self.config['SEED']
                self._generate_new_maze()
            elif choice == '2':
                self.show_path = not self.show_path
            elif choice == '3':
                self.color_idx = (self.color_idx + 1) % len(self.COLORS)
            elif choice == '4':
                print("Exiting A-Maze-ing. Goodbye!")
                break
            else:
                print("Invalid choice, please select 1-4.")
