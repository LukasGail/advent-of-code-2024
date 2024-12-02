from utils.utils import load_data

def level_tolerance_result(input_data, skip_level_tolerance: int = 0):
    save_reports_count = 0
    counter = 0
    for line in input_data.split('\n'):
        if line:
            elements = [int(elem) for elem in line.split()]
            rule_check_result = rule_check(elements, skip_level_tolerance)
            if rule_check_result[0]:
                save_reports_count += 1

            elif skip_level_tolerance > 0:
                # Problem with first setting if list is ascending or descending, 54 56 54 52 51 49 problem,
                # because first could be deleted, and then it would be valid... maby later.
                # if skip_index(elements, rule_check_result[1] + 1) or skip_index(elements, rule_check_result[1] - 1):
                #     save_reports_count += 1

                # bruteforce if simple approach fails
                if brute_force(elements):
                    save_reports_count += 1


        counter += 1

    return save_reports_count

def brute_force(elements) -> bool:
    for i in range(len(elements)):
        elements_copy = elements.copy()
        elements_copy.pop(i)
        rule_check_result = rule_check(elements_copy, 0)
        if rule_check_result[0]:
            return True
    return False

def skip_index(elements, index_to_skip) -> [bool, int]:
    if not -1 < index_to_skip < len(elements)-1:
        return False
    new_elements = elements.copy()
    new_elements.pop(index_to_skip)
    if rule_check(new_elements, 0)[0]:
        return True
    return False


def rule_check(elements, skip_level_tolerance) -> [bool, int]:
    prev_elem = elements[0]
    increasing = elements[0] < elements[1]
    valid_report = True
    skipped_levels = 0
    first_skipped_index = -1
    for i in range(1, len(elements)):
        # rule 1: all increasing or all decreasing
        # rule 2: levels differ by at least one and at most three.
        if (not increasing is (prev_elem < elements[i]) or prev_elem == elements[i]
                or abs(prev_elem - elements[i]) > 3):  # bools are singleton objects
            skipped_levels += 1
            if first_skipped_index == -1:
                first_skipped_index = i

            if skipped_levels > skip_level_tolerance:
                valid_report = False
                break

        else:
            prev_elem = elements[i]

    return [valid_report, first_skipped_index]



if __name__ == '__main__':
    input_day02 = load_data('day02.txt')
    print(level_tolerance_result(input_day02, 0))
    print(level_tolerance_result(input_day02, 1))





