import pytest
from main import *

def create_test_map_groups() -> list[MapGroup]:
    first_map_group, second_map_group = MapGroup(), MapGroup()
    first_map_group.add_inner_map(SourceDestMap(5, 2, 5))
    second_map_group.add_inner_map(SourceDestMap(10, 5, 5))
    return [first_map_group, second_map_group]

def test_traverse_maps_value_inside_map_range():
    first_map_group, _ = create_test_map_groups()
    result = first_map_group.traverse_maps(3)
    assert result == 6

def test_traverse_maps_value_outside_map_range():
    first_map_group, _ = create_test_map_groups()
    result = first_map_group.traverse_maps(11)
    assert result == 11

def test_iterate_through_maps():
    result = iterate_through_maps(3, create_test_map_groups())
    assert result == 11

def test_iterate_through_maps_with_range():
    result = iterate_through_maps_with_range((1, 10), create_test_map_groups())
    expected_results = [(1, 1), (10, 14), (12, 14), (10, 10)]

    # Sequence equal? Ignoring order?
    for expected in expected_results:
        assert expected in result