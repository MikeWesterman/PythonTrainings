from dataclasses import dataclass

@dataclass
class PartNumber:
    value: int
    start_index: int
    end_index: int