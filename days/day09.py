from types import NoneType

from utils.utils import load_data
from typing import List, Type, Any

def get_list_from_input_data(input_data: str) -> list[int]:
    first_input_line = input_data.split("\n")[0]
    return [int(elem) for elem in first_input_line]

def convert_in_space_representation(input_list: list[int]) -> list[int|None]:
    result_list = []
    is_file_element = True
    file_id = 0

    for input_elem in input_list:
        for i in range(input_elem):
            if is_file_element:
                result_list.append(file_id)

            else:
                result_list.append(None)
        if is_file_element:
            file_id = file_id + 1
        is_file_element = not is_file_element
    return result_list


def find_next_element_type_index(input_list: List[int|None], index: int, search_elem_type: Type, backwards_search: bool = False) -> int|None:
    """Get next element index in List of searched type."""
    while ((-1 <= index < len(input_list) -1) and not backwards_search) or ((0 < index <= len(input_list)) and backwards_search): # to cover edge case for empty first element at index 0

        next_index: int = (index - 1) if backwards_search else (index + 1)
        if isinstance(input_list[next_index], search_elem_type):
            return next_index
        index = next_index
    return None


def compact_files_on_disc(input_list: list[int|None]) -> list[int|None]:
    input_list = input_list.copy()
    l_pointer = find_next_element_type_index(input_list, -1, NoneType)
    r_pointer = find_next_element_type_index(input_list, len(input_list), int, True)
    while l_pointer and r_pointer and l_pointer < r_pointer:
        input_list[l_pointer], input_list[r_pointer] = input_list[r_pointer], input_list[l_pointer]
        l_pointer = find_next_element_type_index(input_list, l_pointer, NoneType)
        r_pointer = find_next_element_type_index(input_list, r_pointer, int, True)
    return input_list


def get_size_of_block_type(input_list: list[int|None], index: int, backwards_search: bool = False) -> int:
    result_size = 1
    starting_index = index
    while True:
        next_index: int = (index - 1) if backwards_search else (index + 1)
        if ((not (0 <= next_index < len(input_list))) or
                (not isinstance(input_list[next_index], type(input_list[starting_index])))):
            break
        if input_list[next_index] is not None and input_list[next_index] is not None:
            if input_list[next_index] != input_list[starting_index]:
                break
        result_size = result_size + 1
        index = next_index


    return result_size

def compact_whole_files_on_disc(input_list: list[int|None]) -> list[int|None]:
    input_list = input_list.copy()

    free_spaces: list[tuple[int, int]] = []
    file_sets: list[tuple[int, int]] = []

    for i in range(2):
        l_pointer = find_next_element_type_index(input_list, -1, NoneType if i == 0 else int)
        while l_pointer is not None:
            l_pointer_size = get_size_of_block_type(input_list, l_pointer)
            free_spaces.append((l_pointer, l_pointer_size)) if i == 0 else file_sets.append((l_pointer, l_pointer_size))
            l_pointer = find_next_element_type_index(input_list, l_pointer+l_pointer_size -1, NoneType if i == 0 else int)

    for file in range(len(file_sets)):
        file_reversed_index = len(file_sets) - file - 1
        for space in range(len(free_spaces)):
            # Check that free space index is not behind actual current file position.
            if free_spaces[space][0] > file_sets[file_reversed_index][0]:
                break
            if free_spaces[space][1] >= file_sets[file_reversed_index][1]:

                for i in range(file_sets[file_reversed_index][1]):
                    input_list[free_spaces[space][0]+i], input_list[file_sets[file_reversed_index][0]+i] = input_list[file_sets[file_reversed_index][0]+i], input_list[free_spaces[space][0]+i]

                if free_spaces[space][1] - file_sets[file_reversed_index][1] <= 0:
                    free_spaces.pop(space)
                else:
                    free_spaces[space] = (free_spaces[space][0] + file_sets[file_reversed_index][1], free_spaces[space][1] - file_sets[file_reversed_index][1])
                break



    return input_list

def get_sum_of_file_ids_times_file_pos(compact_input_list) -> int:
    """Return sum of all file-ids multiplied by their index position"""
    result = 0
    for i in range(len(compact_input_list)):
        curr_list_elem = compact_input_list[i]
        if curr_list_elem is None:
            continue
        result = result + (i * curr_list_elem)
    return result





if __name__ == '__main__':
    input_day09 = load_data('day09.txt')
    input_list_day09 = get_list_from_input_data(input_day09)
    converted_input_list = convert_in_space_representation(input_list_day09)
    compacted_files = compact_files_on_disc(converted_input_list)
    print(get_sum_of_file_ids_times_file_pos(compacted_files))
    compacted_whole_files = compact_whole_files_on_disc(converted_input_list)
    print(get_sum_of_file_ids_times_file_pos(compacted_whole_files))
