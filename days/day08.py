from utils.utils import load_data

def get_matrix_from_input(input_data: str) -> list[list[str]]:
    """:return: Matrix[row][col] starting from top left."""
    result_data = []
    for line in input_data.split('\n'):
        if not line:
            continue
        line_data = []
        for elem in line:
            line_data.append(elem)
        result_data.append(line_data)
    return result_data

def get_map_of_antennas(matrix: list[list[str]]) -> dict[str, list[tuple[int, int]]]:
    antenna_map = {}
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            curr_elem = matrix[row][col]
            if curr_elem != '.':
                if curr_elem not in antenna_map:
                    antenna_map[curr_elem] = []
                antenna_map[curr_elem].append((row, col))
    return antenna_map


def get_vector_between_two_points(point1: tuple[int, int], point2: tuple[int, int]) -> tuple[int, int]:
    return (point2[0] - point1[0], point2[1] - point1[1])

def negate_vector(vector: tuple[int, int]) -> tuple[int, int]:
    return (-vector[0], -vector[1])

def get_list_of_all_antinodes(antenna_map: dict[str, list[tuple[int, int]]], matrix_dim: tuple[int, int], with_resonant_harmonics: bool = False) -> list[tuple[int, int]]:
    antinode_list = []
    for antenna_type in antenna_map:
        antenna_positions = antenna_map[antenna_type]
        for i in range(len(antenna_positions)):
            for j in range(len(antenna_positions)):
                if i == j:
                    continue
                vector = get_vector_between_two_points(antenna_positions[i], antenna_positions[j])
                negative_vec = negate_vector(vector)
                if not with_resonant_harmonics:
                    antinode_pos = (antenna_positions[i][0] + negative_vec[0], antenna_positions[i][1] + negative_vec[1])
                    if 0 <= antinode_pos[0] < matrix_dim[0] and 0 <= antinode_pos[1] < matrix_dim[1]:
                        antinode_list.append(antinode_pos)
                else:
                    harmonic_multiplicator = 1
                    antinode_list.append((antenna_positions[i][0], antenna_positions[i][1]))
                    while True:
                        antinode_pos = (antenna_positions[i][0] + (negative_vec[0]*harmonic_multiplicator), antenna_positions[i][1] + (negative_vec[1]* harmonic_multiplicator))
                        if 0 <= antinode_pos[0] < matrix_dim[0] and 0 <= antinode_pos[1] < matrix_dim[1]:
                            antinode_list.append(antinode_pos)
                            harmonic_multiplicator += 1
                        else:
                            break

    return antinode_list


if __name__ == '__main__':
    input_day08 = load_data('day08.txt')
    input_matrix = get_matrix_from_input(input_day08)
    antenna_map = get_map_of_antennas(input_matrix)
    antinodes = get_list_of_all_antinodes(antenna_map, (len(input_matrix), len(input_matrix[0])))
    print(len(set(antinodes)))
    antinodes_with_resonant_harmonics = get_list_of_all_antinodes(antenna_map, (len(input_matrix), len(input_matrix[0])), with_resonant_harmonics=True)
    print(len(set(antinodes_with_resonant_harmonics)))