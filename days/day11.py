from utils.utils import load_data, ListNode, LinkedList
import math

def get_stones(input_data) -> list[int]:
    input_data: str = input_data.split("\n")
    first_line_stones: list[str]= input_data[0].split(" ")
    return [int(stone) for stone in first_line_stones]

def count_digits(n):
    n = abs(n)
    if n == 0:
        return 1
    return math.floor(math.log10(n)) + 1

def is_number_even(n):
    return (n & 1) == 0


def split_digits_in_halve(n: int):
    digits = count_digits(n)
    return n // 10**(digits//2), n % 10**(digits//2)


def __blink(stones: dict[int, int], calculation_lookup: dict[int, int] = None) -> tuple[dict[int, int], dict[int, int]]:
    next_stones = {}
    for stone in stones.keys():
        stone_count = stones[stone]
        if stone_count == 0:
            continue

        if stone == 0:
            next_stones[1] = stone_count + next_stones.get(1, 0) # next stone probably not set
        elif is_number_even(count_digits(stone)):
            left, right = split_digits_in_halve(stone)
            next_stones[left] = stone_count + next_stones.get(left, 0)
            next_stones[right] = stone_count + next_stones.get(right, 0)
        else:
            lookup: int = calculation_lookup.get(stone, None)
            if lookup:
                next_stones[lookup] = stone_count + next_stones.get(lookup, 0)
            else:
                lookup = stone * 2024
                next_stones[lookup] = stone_count + next_stones.get(lookup, 0)
                calculation_lookup[stone] = lookup
    return next_stones, calculation_lookup


def get_multiple_blinking_stone_count(stones: list[int], times: int) -> int:
    stones_counts = {}
    for stone in stones:
        stones_counts[stone] = stones_counts.get(stone, 0) + 1
    calculation_lookup: dict[int, int] = {}
    for i in range(0, times):
        stones_counts, calculation_lookup = __blink(stones_counts, calculation_lookup)
        print(f"Stones iteration {i+1}.")

    print(stones_counts)

    return sum(stones_counts.values())


if __name__ == '__main__':
    input_day11 = load_data('day11.txt')
    stone_input = get_stones(input_day11)
    print(get_multiple_blinking_stone_count(stone_input, 25)) # part 1
    print(get_multiple_blinking_stone_count(stone_input, 75)) # part 2

