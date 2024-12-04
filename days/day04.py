from utils.utils import load_data

# Task 1
def get_all_xmas_occurrences(input_matrix: list[list[str]]) -> int:
    xmax_count = 0
    target_sequence = ["M", "A", "S"]
    directions = [
        (-1, 0),  # Up
        (1, 0),  # Down
        (0, -1),  # Left
        (0, 1),  # Right
        (-1, -1),  # Up-left
        (-1, 1),  # Up-right
        (1, -1),  # Down-left
        (1, 1),  # Down-right
    ]

    for row in range(len(input_matrix)):
        for col in range(len(input_matrix[row])):
            if input_matrix[row][col] == "X":
                # Check up, down, left, right, up-left, up-right, down-left, down-right
                for delta_row, delta_col in directions:
                    if check_pattern_in_direction(input_matrix, row, col, delta_row, delta_col, target_sequence):
                        xmax_count += 1

    return xmax_count


def check_pattern_in_direction(input_matrix, start_row, start_col, delta_row, delta_col, target_sequence):
    rows = len(input_matrix)
    cols = len(input_matrix[0])
    for i in range(1, len(target_sequence)+1):
        row = start_row + i * delta_row
        col = start_col + i * delta_col
        if row < 0 or row >= rows or col < 0 or col >= cols or input_matrix[row][col] != target_sequence[i-1]:
            return False
    return True


# Task 2
def find_xmas_crosses(input_matrix: list[list[str]]) -> int:
    result = 0
    directions = [
        (-1, -1),  # Up-left
        (-1, 1),  # Up-right
        (1, -1),  # Down-left
        (1, 1),  # Down-right
    ]
    for row in range(len(input_matrix)):
        for col in range(len(input_matrix[row])):
            if input_matrix[row][col] == "A":
                # Check up-left, up-right, down-left, down-right 2M 2S X
                x_elements = []

                for delta_row, delta_col in directions:
                    tmp_row = row + delta_row
                    tmp_col = col + delta_col
                    if tmp_row < 0 or tmp_row >= len(input_matrix) or tmp_col < 0 or tmp_col >= len(input_matrix[row]):
                        break
                    x_elements.append(input_matrix[tmp_row][tmp_col])

                if (x_elements.count("M") == 2 and x_elements.count("S") == 2
                        and x_elements[0] != x_elements[3]): # Same token not allowed diagonally.
                    result += 1

    return result



def transform_input_in_2d_token_array(input_data: str) -> list[list[str]]:
    lines = input_data.split('\n')
    matrix_2d: list[list] = [] # 2D matrix[row][column] starting top left 2d[down][right]
    for y in range(len(lines)):
        if len(lines[y]) < 1:
            continue
        matrix_2d.append([])
        for x in range(len(lines[y])):
            matrix_2d[y].append(lines[y][x])
    return matrix_2d


if __name__ == '__main__':
    input_day04 = load_data('day04.txt')
    input_matrix2d = transform_input_in_2d_token_array(input_day04)
    print(get_all_xmas_occurrences(input_matrix2d))
    print(find_xmas_crosses(input_matrix2d))

