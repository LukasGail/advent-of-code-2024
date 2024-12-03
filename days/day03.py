from utils.utils import load_data
import re

def get_valid_instructions_list(input_data: str, advanced_statement_recognition = False) -> list[int|str]:
    lines = input_data.split('\n')
    instructions = []

    for line in lines:
        # find all instructions with regex pattern
        line_result: list[str|int]
        if advanced_statement_recognition:
            line_result = re.findall(r"(?:mul\(\d{1,3},\d{1,3}\))|(?:do\(\))|(?:don't\(\))", line)
        else:
            line_result = re.findall(r"mul\(\d{1,3},\d{1,3}\)", line)

        for elem in line_result:
            elem: str
            if elem.startswith('mul'):
                l,r = elem.replace('mul(', '').replace(')', '').split(',')
                instructions.append(int(l) * int(r))
            else:
                instructions.append(elem)
    return instructions


def task1(mul_num_list: list[int]) -> int:
    return sum(mul_num_list)

def task2(instr_num_list: list[int|str]) -> int:
    result = 0
    enabled = True
    for elem in instr_num_list:
        if isinstance(elem, int):
            if enabled:
                result += elem
            continue
        elif elem.startswith('don'):
            enabled = False
        else:
            enabled = True
    return result


if __name__ == '__main__':
    input_day03 = load_data('day03.txt')
    print(task1(get_valid_instructions_list(input_day03)))
    print(task2(get_valid_instructions_list(input_day03, True)))
    