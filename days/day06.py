from utils.utils import load_data

def transform_to_matrix(input_data: str) -> list[list[str]]:
    matrix = [] # matrix[row][col] starting top left
    for line in input_data.split('\n'):
        tokenized_line = []
        if line:
            for char in line:
                tokenized_line.append(char)
            matrix.append(tokenized_line)
    return matrix


def get_guard_starting_position(matrix: list[list[str]]) -> tuple[int, int]:
    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if char == '^':
                return y, x

def get_next_guard_delta(guard_delta: tuple[int, int]) -> tuple[int, int]:
    if guard_delta == (-1, 0):  # up
        return 0, 1  # right
    if guard_delta == (0, 1):  # right
        return 1, 0  # down
    if guard_delta == (1, 0):  # down
        return 0, -1  # left
    if guard_delta == (0, -1):  # left
        return -1, 0  # up

# def mark_guard_path(matrix: list[list[str]], starting_pos: tuple[int, int]) -> int:
#     """Return: possible loops"""
#     guard_pos: tuple[int, int] = starting_pos
#     guard_direction_delta = (-1, 0)  # up
#     possible_loops = 0
#
#     while True:
#         next_guard_pos = (guard_pos[0] + guard_direction_delta[0], guard_pos[1] + guard_direction_delta[1])
#         if next_guard_pos[0] < 0 or next_guard_pos[0] >= len(matrix) or next_guard_pos[1] < 0 or next_guard_pos[1] >= len(matrix[0]):
#             # Path end
#             matrix[guard_pos[0]][guard_pos[1]] = 'X' # mark exiting point as visited.
#             break
#         if matrix[next_guard_pos[0]][next_guard_pos[1]] == '#':
#             guard_direction_delta = get_next_guard_delta(guard_direction_delta)
#         else:
#             if is_loop_possible(matrix, next_guard_pos, guard_direction_delta):
#                 possible_loops += 1
#             matrix[guard_pos[0]][guard_pos[1]] = 'X'
#             guard_pos = next_guard_pos
#     return possible_loops

def get_next_obstacle_cord_in_direction(matrix: list[list[str]], pos: tuple[int, int], direction_delta: tuple[int, int]):
    while True:
        next_pos = (pos[0] + direction_delta[0], pos[1] + direction_delta[1])
        if next_pos[0] < 0 or next_pos[0] >= len(matrix) or next_pos[1] < 0 or next_pos[1] >= len(matrix[0]):
            return None
        if matrix[next_pos[0]][next_pos[1]] == '#':
            return next_pos
        pos = next_pos


def get_guard_path_length(guard_positions_and_directions: list[tuple[tuple[int, int], tuple[int, int]]]) -> int:
    set_of_positions = set()
    for pos, _ in guard_positions_and_directions:
        set_of_positions.add(pos)
    return len(set_of_positions)


def get_guard_path_positions_with_direction(matrix: list[list[str]], starting_pos: tuple[int, int], guard_delta: tuple[int, int]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    guard_positions_with_direction: list[tuple[tuple[int, int], tuple[int, int]]] = []
    guard_pos = starting_pos
    guard_positions_with_direction.append((guard_pos, guard_delta))

    while True:
        next_pos = (guard_pos[0] + guard_delta[0], guard_pos[1] + guard_delta[1])
        if next_pos[0] < 0 or next_pos[0] >= len(matrix) or next_pos[1] < 0 or next_pos[1] >= len(matrix[0]):
            break
        elif matrix[next_pos[0]][next_pos[1]] == '#':
            guard_delta = get_next_guard_delta(guard_delta)
        else:
            guard_pos = next_pos
            guard_positions_with_direction.append((guard_pos, guard_delta))

    return guard_positions_with_direction

def is_loop_possible(matrix: list[list[str]], tmp_obstacle_pos: tuple[int, int], guard_pos: tuple[int, int], guard_dir_delta: tuple[int, int]) -> bool:
    """Check if position in front of obstacle is reahed again."""
    starting_pos = guard_pos
    starting_dir = guard_dir_delta
    default_char = matrix[tmp_obstacle_pos[0]][tmp_obstacle_pos[1]]
    # set_tmp_obstacle
    matrix[tmp_obstacle_pos[0]][tmp_obstacle_pos[1]] = 'O'

    while True:
        next_guard_pos = (guard_pos[0] + guard_dir_delta[0], guard_pos[1] + guard_dir_delta[1])
        if next_guard_pos[0] < 0 or next_guard_pos[0] >= len(matrix) or next_guard_pos[1] < 0 or next_guard_pos[1] >= len(matrix[0]):
            # Path end
            matrix[tmp_obstacle_pos[0]][tmp_obstacle_pos[1]] = default_char
            return False
        elif next_guard_pos[0] == starting_pos[0] and next_guard_pos[1] == starting_pos[1] and guard_dir_delta[0] == starting_dir[0] and guard_dir_delta[1] == starting_dir[1]:
                matrix[tmp_obstacle_pos[0]][tmp_obstacle_pos[1]] = default_char
                return True
        elif matrix[next_guard_pos[0]][next_guard_pos[1]] == '#' or matrix[next_guard_pos[0]][next_guard_pos[1]] == 'O':
            guard_dir_delta = get_next_guard_delta(guard_dir_delta)
        else:
            guard_pos = next_guard_pos
        print(guard_pos)


def get_possible_loops(matrix: list[list[str]], path_positions_and_directions: list[tuple[tuple[int, int], tuple[int, int]]]) -> int:
    possible_loops = 0
    for i, (pos, direct_delta) in enumerate(path_positions_and_directions):
        tmp_obstacle_pos = (pos[0] + direct_delta[0], pos[1] + direct_delta[1])
        if is_loop_possible(matrix, tmp_obstacle_pos, pos, direct_delta):
            possible_loops += 1
            print(possible_loops)

    return possible_loops


if __name__ == '__main__':
    input_day06 = load_data('day06.txt')
    input_matrix = transform_to_matrix(input_day06)
    # res_possible_loops = mark_guard_path(input_matrix, get_guard_starting_position(input_matrix))
    # 4977 task 1
    # print(get_guard_path_length(input_matrix))
    # print(res_possible_loops)
    positions_and_directions = get_guard_path_positions_with_direction(input_matrix, get_guard_starting_position(input_matrix), (-1, 0))
    print(get_guard_path_length(positions_and_directions))
    print(get_possible_loops(input_matrix, positions_and_directions))




