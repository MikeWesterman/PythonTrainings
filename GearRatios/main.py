from dataclasses import dataclass
from debugpy.common.timestamp import current

@dataclass
class PartNumber:
    value: int
    start_index: int
    end_index: int

def read_schematic(file_path: str) -> list[str]:
    with open(file_path) as f:
        return [line.strip() for line in f.readlines()]

def find_part_numbers(schematic_row: list[str]) -> list[PartNumber]:
    current_part_number = ""
    part_numbers = []
    for i, char in enumerate(schematic_row):
        if char.isdigit():
            current_part_number += char
            if i == len(schematic_row) - 1:
                part_numbers.append(PartNumber(int(current_part_number), i - len(current_part_number), i - 1))
        elif current_part_number != "":
            part_numbers.append(PartNumber(int(current_part_number), i - len(current_part_number), i-1))
            current_part_number = ""

    return part_numbers

def sum_part_numbers(schematic: list[list[str]]) -> int:
    total_sum = 0
    adjacent_rows = [[], schematic[0], schematic[1]]
    for i, row in enumerate(schematic):
        part_numbers = find_part_numbers(row)
        valid_part_numbers = [part_number.value for part_number in part_numbers if check_rows_for_adjacent_symbol(part_number, adjacent_rows)]
        total_sum += sum(valid_part_numbers)

        next_row = schematic[i + 2] if i + 2 < len(schematic) else []
        adjacent_rows = [row, adjacent_rows[-1], next_row]

    return total_sum

def check_rows_for_adjacent_symbol(part_number: PartNumber, rows: list[list[str]]) -> bool:
    for row in rows:
        symbol_indices = [i for i, char in enumerate(row) if char != '.' and not char.isdigit()]
        if any(part_number.start_index - 1 <= idx <= part_number.end_index + 1 for idx in symbol_indices):
            return True

    return False

if __name__ == "__main__":
    schematic = read_schematic("full_input.txt")
    #schematic = read_schematic("test_input.txt")
    print(sum_part_numbers(schematic))