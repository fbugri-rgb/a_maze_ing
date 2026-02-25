"""
Main entry point for the A-Maze-ing project.
Parses the configuration file and initializes the maze generator.
"""

import sys
from typing import Dict, Any


def parse_config(filepath: str) -> Dict[str, Any]:
    """
    Parses the configuration file into a dictionary.

    Args:
        filepath: The path to the configuration text file.

    Returns:
        A dictionary containing the parsed key-value pairs.
    """
    config: Dict[str, Any] = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                # Ignore comments and empty lines
                if not line or line.startswith('#'):
                    continue

                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip().upper()
                    value = value.strip()

                    # Basic type casting based on expected keys
                    if key in ('WIDTH', 'HEIGHT'):
                        config[key] = int(value)
                    elif key in ('ENTRY', 'EXIT'):
                        x_str, y_str = value.split(',')
                        config[key] = (int(x_str.strip()), int(y_str.strip()))
                    elif key == 'PERFECT':
                        config[key] = value.lower() in ('true', '1', 'yes')
                    else:
                        config[key] = value
                else:
                    print(f"Warning: Skipping malformed line: {line}")

    except FileNotFoundError:
        print(f"Error: Configuration file '{filepath}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid value in configuration file. Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading the config: {e}")
        sys.exit(1)

    return config


def main() -> None:
    """Main execution function."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config.txt>")
        sys.exit(1)

    config_file: str = sys.argv[1]
    config_data: Dict[str, Any] = parse_config(config_file)

    # Validate mandatory keys
    required_keys = {'WIDTH', 'HEIGHT', 'ENTRY',
                     'EXIT', 'OUTPUT_FILE', 'PERFECT'}
    if not required_keys.issubset(config_data.keys()):
        missing = required_keys - config_data.keys()
        print(f"Error: Missing mandatory configuration keys: {missing}")
        sys.exit(1)

    print("Configuration loaded successfully:")
    for key, val in config_data.items():
        print(f"  {key}: {val}")

    # TODO: Instantiate MazeGenerator from your mazegen module here
    # generator = MazeGenerator(config_data)
    # generator.generate()

    # Instantiate components from the mazegen module
    from mazegen import (
        MazeGenerator, MazeSolver,
        MazeExporter, TerminalVisualizer
    )

    # 1. Generate and Export the maze to the text file as required
    generator = MazeGenerator(config_data)
    generator.generate()

    solver = MazeSolver(
        generator.grid, generator.width, generator.height,
        generator.entry, generator.exit
    )
    shortest_path = solver.find_shortest_path()

    output_file = config_data.get('OUTPUT_FILE', 'maze.txt')
    exporter = MazeExporter(
        generator.grid, generator.entry, generator.exit, shortest_path
    )
    exporter.export(output_file)
    print(f"Maze successfully generated and saved to {output_file}\n")

    # 2. Launch the Interactive Terminal UI
    visualizer = TerminalVisualizer(config_data)
    visualizer.run()


if __name__ == "__main__":
    main()
