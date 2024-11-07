from dataclasses import dataclass
from enum import Enum
from itertools import chain

@dataclass
class PartNumber:
    value: int
    start_index: int
    end_index: int

class EntryType(Enum):
    PART_NUMBER = 1
    SYMBOL = 2
    GEAR = 3

def read_schematic(file_path: str) -> list[str]:
    with open(file_path) as f:
        return [line.strip() for line in f.readlines()]

def parse_schematic_row(schematic_row: str = "") -> dict:
    current_part_number = ""

    schematic_entries = {
        EntryType.PART_NUMBER: [],
        EntryType.SYMBOL: [],
        EntryType.GEAR: [],
    }

    for i, char in enumerate(schematic_row):
        if char.isdigit():
            # Digits may be variable length, add each digit to the current part number we are currently enumerating over
            current_part_number += char
            if i == len(schematic_row) - 1:
                # If we reached the end of the schematic, and we were tracking a part number on the 'cursor',
                # we need to add this part number
                schematic_entries[EntryType.PART_NUMBER].append(PartNumber(int(current_part_number), i - len(current_part_number) + 1, i))
        else:
            if current_part_number != "":
                # We were previously tracking a part number and No longer tracking a part number
                schematic_entries[EntryType.PART_NUMBER].append(PartNumber(int(current_part_number), i - len(current_part_number), i-1))
                current_part_number = ""

            if char != '.':
                schematic_entries[EntryType.SYMBOL].append(i)
                if char == '*':
                    schematic_entries[EntryType.GEAR].append(i)

    return schematic_entries

def sum_part_numbers(schematic: list[str]) -> int:
    total_sum = 0
    # Initialise row triplets s.t. we will iterate the first row to the center correctly
    previous_row, current_row, next_row = parse_schematic_row(), parse_schematic_row(), parse_schematic_row(schematic[0]) if len(schematic) > 0 else {}

    for i, row in enumerate(schematic):
        previous_row, current_row, next_row = iterate_parsed_rows(schematic, i, current_row, next_row)

        # Find the part numbers on the current row, and check if each has a symbol adjacent
        part_numbers = current_row[EntryType.PART_NUMBER]
        symbol_indices = [parsed_row[EntryType.SYMBOL] for parsed_row in [previous_row, current_row, next_row]]
        valid_part_numbers = [part_number.value for part_number in part_numbers if check_rows_for_adjacent_symbol(part_number, symbol_indices)]
        total_sum += sum(valid_part_numbers)

    return total_sum

def iterate_parsed_rows(schematic: list[str], idx: int, current_row: dict, next_row: dict) -> tuple[dict, dict, dict]:
    # Iterate to the next triplet of rows, i.e. the current row becomes the previous row, the next row becomes the current, and we look ahead to the next
    return current_row, next_row, parse_schematic_row(schematic[idx + 1] if idx < len(schematic) - 1 else [])

def check_rows_for_adjacent_symbol(part_number: PartNumber, symbol_indices: list[list[int]]) -> bool:
    for row in symbol_indices:
        # A part number is adjacent to a symbol if the symbol index is contained in or is one index away from the span of the part number
        if any(part_number.start_index - 1 <= idx <= part_number.end_index + 1 for idx in row):
            return True
    return False

def sum_gear_ratios(schematic: list[str]) -> int:
    total_sum = 0
    # Initialise row triplets s.t. we will iterate the first row of the schematic to the center/current correctly
    previous_row, current_row, next_row = parse_schematic_row(), parse_schematic_row(), parse_schematic_row(schematic[0]) if len(schematic) > 0 else {}

    for i, row in enumerate(schematic):
        previous_row, current_row, next_row = iterate_parsed_rows(schematic, i, current_row, next_row)

        # Check each gear, if it is adjacent to exactly two part numbers, add the product of those part numbers
        for gear in current_row[EntryType.GEAR]:
            # Unpack all gear symbols from the surrounding rows
            part_numbers_from_adjacent_rows = list(chain(*[parsed_row[EntryType.PART_NUMBER] for parsed_row in [previous_row, current_row, next_row]]))
            # A part number is adjacent to a gear if the gear index is contained in or is one index away from the span of the part number
            adjacent_part_numbers = [part_number.value for part_number in part_numbers_from_adjacent_rows if part_number.start_index - 1 <= gear <= part_number.end_index + 1]

            # We take only gears that are adjacent to two part numbers
            if len(adjacent_part_numbers) == 2:
                total_sum += adjacent_part_numbers[0] * adjacent_part_numbers[1]

    return total_sum

if __name__ == "__main__":
    schematic = read_schematic("full_input.txt")
    #schematic = read_schematic("test_input.txt")
    #print(sum_part_numbers(schematic))
    print(sum_gear_ratios(schematic))