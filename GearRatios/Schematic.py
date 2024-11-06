from PartNumber import PartNumber

class Schematic:
    def __init__(self, rows: list[str]):
        self.__rows = rows
        
        self.__prev_row_symbol_idcs = []
        self.__cur_row_symbol_idcs = []
        self.__next_row_symbol_idcs = []
        
        self.__cur_row_part_nums = []
        self.__next_row_part_nums = []
        
        self.__cur_row_idx = 0
        
    def Sum_Part_Numbers(self):
        self.__next_row_part_nums, self.__next_row_symbol_ics = self.__Parse_Row(0)
        total_sum = 0
        
        for i in range(len(self.__rows)):
            self.__Increment_Cur_Row()
            for part_num in self.__cur_row_part_nums:
                if self.__Validate_Part_Num(part_num):
                    total_sum += part_num.value
                    
        return total_sum
                
    def __Increment_Cur_Row(self):
        self.__prev_row_symbol_idcs = self.__cur_row_symbol_idcs
        self.__cur_row_symbol_idcs = self.__next_row_symbol_idcs
        self.__cur_row_part_nums = self.__next_row_part_nums
        
        self.__cur_row_idx += 1
        self.__next_row_part_nums, self.__next_row_symbol_idcs = self.__Parse_Row(self.__cur_row_idx)

    def __Parse_Row(self, row_idx: int):
        part_nums = []
        symbol_idcs = []
        
        if row_idx < len(self.__rows):
            row = self.__rows[row_idx]
            i = 0
            while i < len(row):
                if row[i].isdigit():
                    start_idx = i
                    while row[i].isdigit() and not i >= len(row):
                        i += 1
                        
                    i -= 1
                    part_nums.append(PartNumber(int(row[start_idx : i+1]), start_idx, i))
                elif row[i] != '.':
                    symbol_idcs.append(i)
                    
                i += 1
        
        return part_nums, symbol_idcs
        
    def __Validate_Part_Num(self, part_num: PartNumber):
        minimum_idx = part_num.start_index - 1
        maximum_idx = part_num.end_index + 1

        for idx in set(self.__prev_row_symbol_idcs + self.__next_row_symbol_idcs):
            if minimum_idx <= idx <= maximum_idx:
                return True
            
        for idx in self.__cur_row_symbol_idcs:
            if idx in [minimum_idx, maximum_idx]:
                return True

        return False        