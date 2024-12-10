from utils.utils import load_data


def get_matrix_from_input(input_data: str) -> list[list[int]]:
    """:return: Matrix[row][col] starting from top left."""
    result_data = []
    for line in input_data.split('\n'):
        if not line:
            continue
        line_data = []
        for elem in line:
            line_data.append(int(elem))
        result_data.append(line_data)
    return result_data


def get_all_trailhead_positions(matrix: list[list[int]]) -> list[tuple[int, int]]:
    trailheads = []
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] == 0:
                trailheads.append((row, col))
    return trailheads


def get_trailhead_score(matrix: list[list[int]], trailhead_pos: tuple[int, int], count_distinct_trails: bool = False) -> int:
    reached_hill_positions: list[tuple[int, int]] = []
    current_valid_path_positions: list = [trailhead_pos]

    while current_valid_path_positions:
        path_pos = current_valid_path_positions.pop()

        if matrix[path_pos[0]][path_pos[1]] == 9:
            reached_hill_positions.append(path_pos)
            continue

        if 0 <= path_pos[0] - 1: # Check up
            if matrix[path_pos[0]][path_pos[1]] == matrix[path_pos[0] - 1][path_pos[1]] -1:
                current_valid_path_positions.append((path_pos[0] - 1, path_pos[1]))

        if path_pos[0] + 1 < len(matrix): # Check down
            if matrix[path_pos[0]][path_pos[1]] == matrix[path_pos[0] + 1][path_pos[1]] -1:
                current_valid_path_positions.append((path_pos[0] + 1, path_pos[1]))

        if 0 <= path_pos[1] - 1: # Check left
            if matrix[path_pos[0]][path_pos[1]] == matrix[path_pos[0]][path_pos[1] - 1] -1:
                current_valid_path_positions.append((path_pos[0], path_pos[1] - 1))

        if path_pos[1] + 1 < len(matrix[0]): # Check right
            if matrix[path_pos[0]][path_pos[1]] == matrix[path_pos[0]][path_pos[1] + 1] -1:
                current_valid_path_positions.append((path_pos[0], path_pos[1] +1 ))

    return len(reached_hill_positions) if count_distinct_trails else len(set(reached_hill_positions))


def get_trailhead_score_sum(matrix: list[list[int]], trailhead_positions: list[tuple[int, int]], count_distinct_tails: bool = False) -> int:
    trailhead_score_sum: int = 0
    for trailhead_pos in trailhead_positions:
        trailhead_score_sum += get_trailhead_score(matrix, trailhead_pos, count_distinct_tails)
    return trailhead_score_sum



if __name__ == '__main__':
    input_day10 = load_data('day10.txt')
    input_matrix = get_matrix_from_input(input_day10)
    all_trailhead_positions = get_all_trailhead_positions(input_matrix)
    print(get_trailhead_score_sum(input_matrix, all_trailhead_positions))
    print(get_trailhead_score_sum(input_matrix, all_trailhead_positions, True))
