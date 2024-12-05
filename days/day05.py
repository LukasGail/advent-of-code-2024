from utils.utils import load_data

def get_rules_and_updates(input_data: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
    rules = []
    updates = []
    inputrules = True
    for line in input_data.split('\n'):
        if not line:
            inputrules = False
            continue
        if inputrules:
            rule = line.split('|')
            rules.append((int(rule[0]), int(rule[1])))
        else:
            updates.append([int(x) for x in line.split(',')])
    return rules, updates

def get_relevant_rules_for_update(rules: list[tuple[int, int]], update: list[int]):
    relevant_rules = []
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            relevant_rules.append(rule)
    return relevant_rules

def is_update_in_correct_order(rules: list[tuple[int, int]], update: list[int]):
    # rewrite all rules with their corresponding indices of the element and check if first is smaller than the second one => correct rule
    rules_as_indices: list[tuple[int|None, int|None]] = [(None, None) for _ in range(len(rules))]

    for i, elem in enumerate(update):
        for j, rule in enumerate(rules):
            if elem == rule[0]:
                rules_as_indices[j] = (i, rules_as_indices[j][1])
            if elem == rule[1]:
                rules_as_indices[j] = (rules_as_indices[j][0], i)

    if all(rules_as_indices[i][0] <= rules_as_indices[i][1] for i in range(len(rules))):
        return True
    return False


def get_all_correct_updates(rules: list[tuple[int, int]], updates: list[list[int]]) -> list[list[int]]:
    return [update for update in updates if is_update_in_correct_order(get_relevant_rules_for_update(rules, update), update)]

def get_all_incorrect_updates(rules: list[tuple[int, int]], updates: list[list[int]]) -> list[list[int]]:
    return [update for update in updates if not is_update_in_correct_order(get_relevant_rules_for_update(rules, update), update)]

def get_middle_page_number(update: list[int]) -> int:
    return update[len(update)//2]

def get_sum_of_middle_page_numbers(updates: list[list[int]]) -> int:
    return sum([get_middle_page_number(update) for update in updates])


def correctly_order_update(rules: list[tuple[int, int]], update: list[int]) -> [int]:
    for i in range(len(rules)):
        for j in range(i, len(rules)):
            correct_next_rule = True
            for k in range(i, len(rules)):
                if rules[j][0] == rules[k][1]:
                    # wrong continue
                    correct_next_rule = False
                    break
            if correct_next_rule:
                rules[i], rules[j] = rules[j], rules[i]
                break

    reordered_update = []
    for rule in rules:
        if rule[0] not in reordered_update:
            reordered_update.append(rule[0])

    reordered_update.extend([x for x in update if x not in reordered_update])
    return reordered_update


def reorder_updates(rules: list[tuple[int, int]], updates: list[list[int]]) -> list[list[int]]:
    return [correctly_order_update(get_relevant_rules_for_update(rules, update), update) for update in updates]


if __name__ == '__main__':
    input_day05 = load_data('day05.txt')
    all_rules, all_updates = get_rules_and_updates(input_day05)
    # Task1
    print(get_sum_of_middle_page_numbers(get_all_correct_updates(all_rules, all_updates)))
    # Task2
    print(get_sum_of_middle_page_numbers(reorder_updates(all_rules, get_all_incorrect_updates(all_rules, all_updates))))