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
        bisect.insort(self.inner_maps, inner_map, key=lambda m: m.source)

    def is_empty(self) -> bool:
        return len(self.inner_maps) == 0

    def traverse_maps(self, map_input: int) -> int:
        for inner_map in self.inner_maps:
            # If the input is within the source range, map it to the corresponding destination
            if inner_map.source <= map_input < inner_map.source + inner_map.length:
                return map_input - inner_map.source + inner_map.dest

        # Input was not between any source range. Map to itself
        return map_input

    def traverse_maps_with_range(self, map_inputs: tuple[int, int]) -> list[tuple[int, int]]:
        output_ranges = []
        inputs_mapped = []
        input_start, input_end = map_inputs[0], map_inputs[1]

        # Iterate through maps. If (map source, : source + length) intersects with the input range, find this intersection
        for inner_map in self.inner_maps:
            map_start = inner_map.source
            map_end = inner_map.source + inner_map.length - 1
            intersection = range(max(input_start, map_start), min(input_end, map_end) + 1)
            if intersection:
                # If these intersect, add corresponding destination range for the intersection
                output_ranges.append( (intersection[0] - map_start + inner_map.dest, intersection[-1] - map_start + inner_map.dest) )
                # Keep track of which input range subset we have mapped so far
                inputs_mapped.append( (intersection[0], intersection[-1]) )

        # Next, need to check the input range for any unmapped values, and map them to themselves
        gap_start = input_start
        gaps = []
        for input_map in sorted(inputs_mapped, key=lambda x: x[0]):
            if gap_start < input_map[0]:
                gaps.append( (gap_start, input_map[0] - 1) )
            # Check for gaps after the next range of inputs that are known to have been mapped
            gap_start = input_map[1] + 1

        # And finally check if any of the input range exceeds the highest source value in the mapping, and map to itself
        if gap_start <= map_inputs[1]:
            gaps.append( (gap_start, map_inputs[1]) )

        output_ranges += gaps
        return output_ranges

def read_almanac(file_path: str) -> tuple[list[int], list[MapGroup]]:
    with open(file_path) as f:
        lines = [line.strip() for line in f.readlines()]

    maps = []
    current_group = MapGroup()

    for i, line in enumerate(lines):
        if i == 0:
            # First line is seeds, parse these
            _, values_str = line.split(sep = "seeds: ")
            seeds = [int(seed) for seed in values_str.split()]
        elif line.endswith("map:"):
            # Finished the current map group
            if not current_group.is_empty():
                maps.append(current_group)
                current_group = MapGroup()
            continue
        elif line:
            # Parse the current line and add it to the current map group
            source, dest, length = [int(value) for value in line.split()]
            current_group.add_inner_map(SourceDestMap(source, dest, length))

    # Make sure to include the current group ending on the final line
    maps.append(current_group)
    return seeds, maps

def iterate_through_maps(seed: int, maps: list[MapGroup]) -> int:
    current_value = seed
    for m in maps:
        current_value = m.traverse_maps(current_value)

    return current_value

def iterate_through_maps_with_range(map_inputs: tuple[int, int], maps: list[MapGroup]) -> list[tuple[int, int]]:
    cur_inputs = [map_inputs]
    for m in maps:
        next_inputs = []
        for input_range in cur_inputs:
            next_inputs += m.traverse_maps_with_range(input_range)
        cur_inputs = next_inputs

    return cur_inputs

if __name__ == "__main__":
    second_task = True

    #seeds, maps = read_almanac("test_input.txt")
    seeds, maps = read_almanac("full_input.txt")

    if second_task:
        # Need ranges of seeds where each consecutive pair of seeds represents a range,
        # e.g. (1, 2, 3, 4) corresponds to the ranges (1, 1+2=3) and (3, 3+4=7)
        seed_ranges = [(first, first + second) for first, second in zip(seeds[::2], seeds[1::2])]

        # For each seed range, find the ranges of eventual locations
        all_location_ranges = []
        for seed_range in seed_ranges:
            all_location_ranges += iterate_through_maps_with_range(seed_range, maps)

        # Lastly, find the minimum location possible from all seed ranges
        min_location_number = min([loc_range[0] for loc_range in all_location_ranges])
        print(min_location_number)
    else:
        # Traverse the set of maps with each seed value and find the minimum
        locations = [iterate_through_maps(seed, maps) for seed in seeds]
        print(min(locations))

