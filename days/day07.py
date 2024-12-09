from utils.utils import load_data

def transform_input_to_list(input_data: str) -> list[list[int]]:
    """First element in list is the compare value"""
    result_data = []
    for line in input_data.split('\n'):
        if not line:
            continue
        line_data = []
        compare_val, elem_list = line.split(':')
        elem_list = elem_list.strip()
        line_data.append(int(compare_val))
        for elem in elem_list.split(' '):
            line_data.append(int(elem))
        result_data.append(line_data)
    return result_data


def calculate_with_str_operator(elem1: int, elem2: int, operator: str) -> int:
    if operator == '+':
        return elem1 + elem2
    elif operator == '*':
        return elem1 * elem2
    elif operator == '||':
        length_of_elem2 = len(str(elem2))
        return elem1 * (10 ** length_of_elem2) + elem2
    else:
        raise ValueError(f"Operator {operator} is not valid")

def calculate_possible_results_with_different_operator_combinations(line_data: list[int], operators: list[str]) -> list[int]:
    tmp_results_last_iteration = []
    tmp_results = []

    compare_val = line_data[0]
    tmp_results_last_iteration.append(line_data[1])
    for i in range(2, len(line_data)):
        for elem in tmp_results_last_iteration:
            for operator in operators:
                elem_result = calculate_with_str_operator(elem, line_data[i], operator)
                if elem_result <= compare_val:
                    tmp_results.append(elem_result)
        tmp_results_last_iteration = tmp_results
        tmp_results = []

    return tmp_results_last_iteration


def get_sum_of_possible_test_values(input_data: list[list[int]], operators: list[str]) -> int:
    sum_of_possible_values = 0
    for line_data in input_data:
        possible_values = calculate_possible_results_with_different_operator_combinations(line_data, operators)
        if line_data[0] in possible_values:
            sum_of_possible_values += line_data[0]
    return sum_of_possible_values


if __name__ == '__main__':
    input_day07 = load_data('day07.txt')
    input_lines = transform_input_to_list(input_day07)

    print(get_sum_of_possible_test_values(input_lines, ['+', '*']))
    print(get_sum_of_possible_test_values(input_lines, ['+', '*', '||']))
