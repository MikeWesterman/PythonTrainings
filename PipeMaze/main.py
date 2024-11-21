from __future__ import annotations # Required due to reference of Node in Node constructor
import math
import numpy as np

UPWARD_SYMBOLS = "S|JL"
DOWNWARD_SYMBOLS = "S|7F"
LEFTWARD_SYMBOLS = "S-7J"
RIGHTWARD_SYMBOLS = "S-LF"

class Coord:
    def __init__(self, row_idx: int, col_idx: int, maze: list[str]):
        self.row = row_idx
        self.col = col_idx
        self.symbol = maze[row_idx][col_idx]

    def __eq__(self, other: Coord):
        return self.row == other.row and self.col == other.col and self.symbol == other.symbol

def read_maze(path: str):
    with open(path) as f:
        return [line.strip() for line in f.readlines()]

def find_start_index(maze: list[str]):
    for i, row in enumerate(maze):
        if 'S' in row:
            return i, row.index('S')

    raise ValueError("No start 'S' character in Maze.")

def find_adjacent(previous: Coord, current: Coord, maze: list[str]):
    # Making the assumption that adjacent pipes must also be on the loop, i.e. that we don't have dead ends.
    # Logic could be adjusted to account for these, but KISS.
    possible_adjacent_coordinates = []
    # Check above
    if current.row > 0 and current.symbol in UPWARD_SYMBOLS and maze[current.row - 1][current.col] in DOWNWARD_SYMBOLS:
        possible_adjacent_coordinates.append(Coord(current.row - 1, current.col, maze))
    # Check below
    if current.row < len(maze) - 1 and current.symbol in DOWNWARD_SYMBOLS and maze[current.row + 1][current.col] in UPWARD_SYMBOLS:
        possible_adjacent_coordinates.append(Coord(current.row + 1, current.col, maze))
    # Check to the left
    if current.col > 0 and current.symbol in LEFTWARD_SYMBOLS and maze[current.row][current.col - 1] in RIGHTWARD_SYMBOLS:
        possible_adjacent_coordinates.append(Coord(current.row, current.col - 1, maze))
    # Check to the right
    if current.col < len(maze[0]) - 1 and current.symbol in RIGHTWARD_SYMBOLS and maze[current.row][current.col + 1] in LEFTWARD_SYMBOLS:
        possible_adjacent_coordinates.append(Coord(current.row, current.col + 1, maze))

    for coord in possible_adjacent_coordinates:
        if not coord.__eq__(previous):
            return coord

    return None

def find_all_points_on_loop(maze: list[str]):
    start_row, start_column = find_start_index(maze)

    previous_coordinate = Coord(-1, -1, maze)
    current_coordinate = Coord(start_row, start_column, maze)
    loop_found = False

    loop_coordinates = []
    while not loop_found:
        loop_coordinates.append(current_coordinate)
        next_coordinate = find_adjacent(previous_coordinate, current_coordinate, maze)

        previous_coordinate = current_coordinate
        current_coordinate = next_coordinate

        loop_found = next_coordinate.symbol == "S"

    return loop_coordinates

def find_area_of_loop(points_on_loop: list[Coord]):
    vertices = [(coord.row, coord.col) for coord in points_on_loop if coord.symbol not in "-|"]

    # Shoelace formula: https://en.wikipedia.org/wiki/Shoelace_formula
    x_values = np.array([vertex[0] for vertex in vertices])
    y_values = np.array([vertex[1] for vertex in vertices])
    xrange = np.arange(len(x_values))
    return np.abs(np.sum(x_values[xrange - 1] * y_values[xrange] - x_values[xrange] * y_values[xrange - 1]) * 0.5)

def task_one(path: str):
    maze = read_maze(path)
    loop_coordinates = find_all_points_on_loop(maze)
    max_distance = math.ceil(len(loop_coordinates) // 2)
    print(max_distance)

def task_two(path: str):
    maze = read_maze(path)
    loop_coordinates = find_all_points_on_loop(maze)

    loop_area = find_area_of_loop(loop_coordinates)

    # Pick's theorem: https://en.wikipedia.org/wiki/Pick%27s_theorem (assuming no holes, hopefully...)
    num_interior_points = loop_area - (len(loop_coordinates) / 2) + 1
    print(num_interior_points)

if __name__ == "__main__":
    input_path = "full_input.txt"
    #task_one(input_path)
    task_two(input_path)