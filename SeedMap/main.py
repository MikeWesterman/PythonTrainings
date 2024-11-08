from dataclasses import dataclass
import bisect

@dataclass
class SourceDestMap:
    dest: int
    source: int
    length: int

class MapGroup:
    def __init__(self,):
        self.inner_maps: list[SourceDestMap] = []

    def add_inner_map(self, inner_map: SourceDestMap):
        self.inner_maps.append(inner_map)

    def is_empty(self) -> bool:
        return len(self.inner_maps) == 0

    def traverse_maps(self, map_input: int) -> int:
        for inner_map in self.inner_maps:
            if inner_map.source <= map_input < inner_map.source + inner_map.length:
                return map_input - inner_map.source + inner_map.dest

        return map_input

def read_almanac(file_path: str) -> tuple[list[int], list[MapGroup]]:
    with open(file_path) as f:
        seeds = []
        maps = []
        lines = f.readlines()

        current_group = MapGroup()
        for i in range(len(lines)):
            stripped_line = lines[i].strip()
            if i == 0:
                # First line is seeds, parse these
                _, values_str = stripped_line.split(sep = "seeds: ")
                seeds = [int(seed) for seed in values_str.split()]
            elif "map:" in stripped_line or stripped_line == "":
                # Finished the current map group
                if not current_group.is_empty():
                    maps.append(current_group)
                    current_group = MapGroup()
                continue
            else:
                # Parse the current line and add it to the current map group
                source, dest, length = [int(value) for value in stripped_line.split()]
                current_group.add_inner_map(SourceDestMap(source, dest, length))
        maps.append(current_group)

    return seeds, maps

def iterate_through_maps(seed: int, maps: list[MapGroup]) -> int:
    current_value = seed
    for m in maps:
        current_value = m.traverse_maps(current_value)

    return current_value

if __name__ == "__main__":
    seeds, maps = read_almanac("full_input.txt")
    locations = [iterate_through_maps(seed, maps) for seed in seeds]
    print(min(locations))

