from utils.utils import load_data

def get_sorted_lists() -> list[list[int]]:
    input_data = load_data('day01.txt')
    l = []
    r = []
    for line in input_data.split('\n'):
        if line:
            l_elem, r_elem = line.split()
            l.append(int(l_elem))
            r.append(int(r_elem))

    l.sort()
    r.sort()
    return [l,r]

def part1(sorted_lists: list[list[int]]) -> int:
    l, r = sorted_lists
    result = 0
    for i in range(len(l)):
        result = result + abs(l[i] - r[i])

    return result


def part2(sorted_lists: list[list[int]]) -> int:
    l, r = sorted_lists

    multiplication_list = []
    l_last_elem = None # to prevent duplicate calculations

    for i in range(len(l)):
        if l_last_elem and l_last_elem == l[i]:
            multiplication_list.append(multiplication_list[-1])

        else:
            r_same_count = 0
            already_found = False
            for j in range(len(r)):
                if l[i] == r[j]:
                    r_same_count += 1
                    already_found = True
                elif already_found: # because of sorted list the same element cant occur again after the first encounter
                    break

            if r_same_count > 0:
                multiplication_list.append(l[i] * r_same_count)
                l_last_elem = l[i]

    return sum(multiplication_list)


if __name__ == '__main__':
    sorted_lists_input = get_sorted_lists()
    print(part1(sorted_lists_input))
    print(part2(sorted_lists_input))

