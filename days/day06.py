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

def mark_guard_path(matrix: list[list[str]], starting_pos: tuple[int, int]):
    guard_pos: tuple[int, int] = starting_pos
    guard_direction_delta = (-1, 0)  # up
    path_len = 0

    while True:
        next_guard_pos = (guard_pos[0] + guard_direction_delta[0], guard_pos[1] + guard_direction_delta[1])
        if next_guard_pos[0] < 0 or next_guard_pos[0] >= len(matrix) or next_guard_pos[1] < 0 or next_guard_pos[1] >= len(matrix[0]):
            # Path end
            matrix[guard_pos[0]][guard_pos[1]] = 'X' # mark exiting point as visited.
            break
        if matrix[next_guard_pos[0]][next_guard_pos[1]] == '#':
            guard_direction_delta = get_next_guard_delta(guard_direction_delta)
        else:
            matrix[guard_pos[0]][guard_pos[1]] = 'X'
            guard_pos = next_guard_pos
            path_len += 1

def get_guard_path_length(matrix: list[list[str]]) -> int:
    return sum([row.count('X') for row in matrix])


if __name__ == '__main__':
    input_day06 = load_data('day06.txt')
    input_matrix = transform_to_matrix(input_day06)
    mark_guard_path(input_matrix, get_guard_starting_position(input_matrix))
    print(get_guard_path_length(input_matrix))