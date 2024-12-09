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
    """Check if position in front of obstacle is reached again."""
    if tmp_obstacle_pos[0] < 0 or tmp_obstacle_pos[0] >= len(matrix) or tmp_obstacle_pos[1] < 0 or tmp_obstacle_pos[1] >= len(matrix[0]):
        return False
    default_char = matrix[tmp_obstacle_pos[0]][tmp_obstacle_pos[1]]
    # set_tmp_obstacle
    matrix[tmp_obstacle_pos[0]][tmp_obstacle_pos[1]] = 'O'
    tmp_obstacle_reached_deltas: list[tuple[int, int]] = []
    obstacle_counter = 0
    fourth_obstacle: tuple = (-1, -1)
    fourth_obstacle_direction: tuple = (-1, -1)

    while True:
        next_guard_pos: tuple[int, int] = (guard_pos[0] + guard_dir_delta[0], guard_pos[1] + guard_dir_delta[1])
        if next_guard_pos[0] < 0 or next_guard_pos[0] >= len(matrix) or next_guard_pos[1] < 0 or next_guard_pos[1] >= len(matrix[0]):
            # Path end
            matrix[tmp_obstacle_pos[0]][tmp_obstacle_pos[1]] = default_char
            return False

        elif matrix[next_guard_pos[0]][next_guard_pos[1]] == '#':
            obstacle_counter = (obstacle_counter + 1)%4
            if obstacle_counter == 0:
                if fourth_obstacle == next_guard_pos and fourth_obstacle_direction == guard_dir_delta:
                    # loop between 4 random obstacles
                    matrix[tmp_obstacle_pos[0]][tmp_obstacle_pos[1]] = default_char
                    return True
                fourth_obstacle = next_guard_pos
                fourth_obstacle_direction = guard_dir_delta

            guard_dir_delta = get_next_guard_delta(guard_dir_delta)

        elif matrix[next_guard_pos[0]][next_guard_pos[1]] == 'O':
            if not guard_dir_delta in tmp_obstacle_reached_deltas:
                tmp_obstacle_reached_deltas.append(guard_dir_delta)
            else:
                # already reached the obstacle in this direction
                matrix[tmp_obstacle_pos[0]][tmp_obstacle_pos[1]] = default_char
                return True

            guard_dir_delta = get_next_guard_delta(guard_dir_delta)

        else:
            guard_pos = next_guard_pos



def get_possible_loops(matrix: list[list[str]], path_positions_and_directions: list[tuple[tuple[int, int], tuple[int, int]]], guard_pos: tuple[int, int], guard_delta: tuple[int, int]) -> int:
    possible_loops = 0
    tested_obstacle_positions = set()

    for i in range(1, len(path_positions_and_directions)-1):
        tmp_obstacle_pos = path_positions_and_directions[i + 1][0]

        if tmp_obstacle_pos in tested_obstacle_positions:
            continue
        else:
            tested_obstacle_positions.add(tmp_obstacle_pos)

        if is_loop_possible(matrix, tmp_obstacle_pos, guard_pos, guard_delta):
            possible_loops += 1
            print(f"({i}) {possible_loops}/{len(path_positions_and_directions)-2}")

    return possible_loops


if __name__ == '__main__':
    input_day06 = load_data('day06.txt')
    input_matrix = transform_to_matrix(input_day06)
    positions_and_directions = get_guard_path_positions_with_direction(input_matrix, get_guard_starting_position(input_matrix), (-1, 0))
    print(get_guard_path_length(positions_and_directions))
    print(get_possible_loops(input_matrix, positions_and_directions, get_guard_starting_position(input_matrix), (-1, 0)))

