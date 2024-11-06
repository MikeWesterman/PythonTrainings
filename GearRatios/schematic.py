from part_number import PartNumber

class Schematic:
    def __init__(self, rows: list[str]):
        self._rows = rows
        
        self._prev_row_symbol_idcs = []
        self._cur_row_symbol_idcs = []
        self._next_row_symbol_idcs = []
        
        self._cur_row_part_nums = []
        self._next_row_part_nums = []
        
        self._cur_row_idx = 0
        
    def sum_part_numbers(self):
        self._next_row_part_nums, self._next_row_symbol_idcs = self._parse_row(0)
        total_sum = 0
        
        for i in range(len(self._rows)):
            self._increment_cur_row()
            for part_num in self._cur_row_part_nums:
                if self._validate_part_num(part_num):
                    total_sum += part_num.value
                    
        return total_sum
                
    def _increment_cur_row(self):
        self._prev_row_symbol_idcs = self._cur_row_symbol_idcs
        self._cur_row_symbol_idcs = self._next_row_symbol_idcs
        self._cur_row_part_nums = self._next_row_part_nums
        
        self._cur_row_idx += 1
        self._next_row_part_nums, self._next_row_symbol_idcs = self._parse_row(self._cur_row_idx)

    def _parse_row(self, row_idx: int) -> tuple[list[PartNumber],list[int]]:
        part_nums = []
        symbol_idcs = []
        
        if row_idx < len(self._rows):
            row = self._rows[row_idx]
            i = 0
            while i < len(row):
                if row[i].isdigit():
                    start_idx = i
                    while not i >= len(row) and row[i].isdigit():
                        i += 1
                        
                    i -= 1
                    part_nums.append(PartNumber(int(row[start_idx : i+1]), start_idx, i))
                elif row[i] != '.':
                    symbol_idcs.append(i)
                    
                i += 1
        
        return part_nums, symbol_idcs
        
    def _validate_part_num(self, part_num: PartNumber):
        minimum_idx = part_num.start_index - 1
        maximum_idx = part_num.end_index + 1

        for idx in set(self._prev_row_symbol_idcs + self._next_row_symbol_idcs):
            if minimum_idx <= idx <= maximum_idx:
                return True
            
        for idx in self._cur_row_symbol_idcs:
            if idx in [minimum_idx, maximum_idx]:
                return True

        return False        