# Required due to reference of Node in Node constructor
from __future__ import annotations
from enum import Enum
import math

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

def validate_adjacent_symbol(row: int, col: int, valid_symbols: str, maze: list[str]):
    return maze[row][col] in valid_symbols

def find_adjacent(previous: Coord, current: Coord, maze: list[str]):

    possible_adjacent_coords = []

    # Check above
    if current.row > 0 and current.symbol in UPWARD_SYMBOLS and maze[current.row - 1][current.col] in DOWNWARD_SYMBOLS:
        possible_adjacent_coords.append(Coord(current.row - 1, current.col, maze))
    # Check below
    if current.row < len(maze) - 1 and current.symbol in DOWNWARD_SYMBOLS and maze[current.row + 1][current.col] in UPWARD_SYMBOLS:
        possible_adjacent_coords.append(Coord(current.row + 1, current.col, maze))
    # Check to the left
    if current.col > 0 and current.symbol in LEFTWARD_SYMBOLS and maze[current.row][current.col - 1] in RIGHTWARD_SYMBOLS:
        possible_adjacent_coords.append(Coord(current.row, current.col - 1, maze))
    # Check to the right
    if current.col < len(maze[0]) - 1 and current.symbol in RIGHTWARD_SYMBOLS and maze[current.row][current.col + 1] in LEFTWARD_SYMBOLS:
        possible_adjacent_coords.append(Coord(current.row, current.col + 1, maze))

    for coord in possible_adjacent_coords:
        if not coord.__eq__(previous):
            return coord

    return None

def task_one(path: str):
    maze = read_maze(path)
    start_row, start_column = find_start_index(maze)

    previous_coordinate = Coord(-1, -1, maze)
    current_coordinate = Coord(start_row, start_column, maze)
    loop_found = False
    iterations = 0
    while not loop_found:
        next_coordinate = find_adjacent(previous_coordinate, current_coordinate, maze)
        iterations += 1

        previous_coordinate = current_coordinate
        current_coordinate = next_coordinate

        loop_found = next_coordinate.symbol == "S"

    max_distance = math.ceil(iterations // 2)
    print(max_distance)

if __name__ == "__main__":
    path = "full_input.txt"
    task_one(path)