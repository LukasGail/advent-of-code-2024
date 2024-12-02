from utils.utils import load_data, time_decorator

@time_decorator
def level_tolerance_result(input_data, skip_level: bool = False, use_brute_force: bool = False) -> int:
    save_reports_count = 0
    for line in input_data.split('\n'):
        if line:
            elements = [int(elem) for elem in line.split()]
            rule_check_result = rule_check(elements, skip_level)
            if rule_check_result[0]:
                save_reports_count += 1

            elif skip_level:
                if not use_brute_force:
                    if skip_index(elements, rule_check_result[1] - 1):
                        save_reports_count += 1

                else:
                    # bruteforce (works too)
                    if brute_force(elements):
                        save_reports_count += 1

    return save_reports_count

def brute_force(elements) -> bool:
    for i in range(len(elements)):
        elements_copy = elements.copy()
        elements_copy.pop(i)
        rule_check_result = rule_check(elements_copy, False)
        if rule_check_result[0]:
            return True
    return False

def skip_index(elements, index_to_skip) -> [bool, int]:
    if not -1 < index_to_skip < len(elements)-1:
        return False
    new_elements = elements.copy()
    new_elements.pop(index_to_skip)
    if rule_check(new_elements, False)[0]:
        return True
    return False


def rule_check(elements, skip_level: bool) -> [bool, int]:
    prev_elem = elements[0]
    # Simple check for increasing or decreasing in first values, if not, check detailed.
    increasing = True if elements[0] < elements[1] < elements[2] else is_ascending(elements)
    valid_report = True
    skipped_level = False
    first_skipped_index = -1
    for i in range(1, len(elements)):
        # rule 1: all increasing or all decreasing
        # rule 2: levels differ by at least one and at most three.
        if (not increasing is (prev_elem < elements[i]) or prev_elem == elements[i]
                or abs(prev_elem - elements[i]) > 3):  # bools are singleton objects
            if first_skipped_index == -1:
                first_skipped_index = i

            if skipped_level is skip_level:
                valid_report = False
                break
            skipped_level = True # only once if skip_level is True

        else:
            prev_elem = elements[i]

    return [valid_report, first_skipped_index]

def is_ascending(elements):
    ascending = 0
    descending = 0
    for i in range(1, len(elements)):
        if elements[i] > elements[i-1]:
            ascending += 1
        else:
            descending += 1
    return ascending > descending

if __name__ == '__main__':
    input_day02 = load_data('day02.txt')
    #Task1
    print(level_tolerance_result(input_day02, skip_level=False, use_brute_force=False))
    print(level_tolerance_result(input_day02, skip_level=False, use_brute_force=True))

    #Task2
    print(level_tolerance_result(input_day02, skip_level=True, use_brute_force=False))
    print(level_tolerance_result(input_day02, skip_level=True, use_brute_force=True))

