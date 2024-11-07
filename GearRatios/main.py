from dataclasses import dataclass
from enum import Enum

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
            current_part_number += char
            if i == len(schematic_row) - 1:
                schematic_entries[EntryType.PART_NUMBER].append(PartNumber(int(current_part_number), i - len(current_part_number), i-1))
        else:
            if current_part_number != "":
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
    parsed_rows = [parse_schematic_row(), parse_schematic_row(), parse_schematic_row(schematic[0]) if len(schematic) > 0 else {}]

    for i, row in enumerate(schematic):
        parsed_rows = iterate_parsed_rows(schematic, i, parsed_rows)

        # Check the part numbers on the current row, and check if each has a symbol adjacent
        part_numbers = parsed_rows[1][EntryType.PART_NUMBER]
        symbol_indices = [parsed_row[EntryType.SYMBOL] for parsed_row in parsed_rows]

        valid_part_numbers = [part_number.value for part_number in part_numbers if check_rows_for_adjacent_symbol(part_number, symbol_indices)]
        total_sum += sum(valid_part_numbers)

    return total_sum

def iterate_parsed_rows(schematic: list[str], idx: int, parsed_rows: list[dict]) -> list[dict]:
    # Iterate row triplets s.t. the previous row is first, the current row is in the center and the next row is at the end
    parsed_rows[0] = parsed_rows[1]
    parsed_rows[1] = parsed_rows[2]
    parsed_rows[-1] = parse_schematic_row(schematic[idx + 1] if idx < len(schematic) - 1 else [])
    return parsed_rows

def check_rows_for_adjacent_symbol(part_number: PartNumber, symbol_indices: list[list[int]]) -> bool:
    for row in symbol_indices:
        if any(part_number.start_index - 1 <= idx <= part_number.end_index + 1 for idx in row):
            return True
    return False


if __name__ == "__main__":
    schematic = read_schematic("full_input.txt")
    #schematic = read_schematic("test_input.txt")
    print(sum_part_numbers(schematic))