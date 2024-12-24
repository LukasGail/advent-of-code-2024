from utils.utils import load_data
from collections import deque

def get_matrix_from_input(input_data: str) -> list[list[str|None]]:
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



def get_all_garden_plots_with_border_plots(garden_matrix: list[list[str | None]]) -> list[tuple[ set[tuple[int, int]], list[tuple[tuple[int, int], tuple[int, int]]]]]:
    garden_plots: list[tuple[set[tuple[int, int]], list[tuple[tuple[int, int], tuple[int, int]]]]] = [] # set of plots with border count to other plots.

    direction_deltas = [
        (-1, 0), # up
        (1, 0), # down
        (0, -1), # left
        (0, 1), # right
    ]
    already_processed_tiles: set[tuple[int, int]] = set()

    for row in range(len(garden_matrix)):
        for col in range(len(garden_matrix[0])):
            if (row, col) not in already_processed_tiles: # If tile was already processed in garden_plot, skip.
                curr_plot_queue: deque[tuple[int, int]] = deque()
                curr_plot = set()
                curr_plot_queue.append((row, col))
                curr_plot_borders: list[tuple[tuple[int,int], tuple[int, int]]] = [] # (plot, border_direction_delta)
                while curr_plot_queue: # tree search
                    curr_elem_coord = curr_plot_queue.popleft()
                    already_processed_tiles.add(curr_elem_coord)

                    curr_plot.add(curr_elem_coord)

                    for direction_delta in direction_deltas:
                        relativ_dir_tile = (curr_elem_coord[0] + direction_delta[0], curr_elem_coord[1] + direction_delta[1])
                        if (0 <= relativ_dir_tile[0] < len(garden_matrix) and 0 <= relativ_dir_tile[1] < len(garden_matrix[0])) and (garden_matrix[curr_elem_coord[0] + direction_delta[0]][curr_elem_coord[1]+direction_delta[1]] == garden_matrix[curr_elem_coord[0]][curr_elem_coord[1]]):
                            if relativ_dir_tile not in curr_plot and relativ_dir_tile not in curr_plot_queue: # can be added multiple times to queue. Could add tile on first discovery to plot
                                curr_plot_queue.append((curr_elem_coord[0]+direction_delta[0], curr_elem_coord[1]+direction_delta[1]))
                        else:
                            curr_plot_borders.append((curr_elem_coord, direction_delta))
                garden_plots.append((curr_plot, curr_plot_borders))

    return garden_plots



def get_total_fence_price_for_single_tiles(plot_list: list[tuple[set[tuple[int, int]], list[tuple[tuple[int, int], tuple[int, int]]]]]) -> int:
    total_fence_price = 0
    for plot in plot_list:
        total_fence_price = total_fence_price + (len(plot[0]) * len(plot[1]))
    return total_fence_price


def get_plot_fence_sides(plot: tuple[set[tuple[int, int]], list[tuple[tuple[int, int], tuple[int, int]]]]) -> int:
    fence_sides = 0
    fence_tiles_with_fence_direction = plot[1]
    processed_fence_tiles: set[tuple[tuple[int, int],tuple[int, int]]] = set()
    for fence_tile_with_fence_direction in fence_tiles_with_fence_direction:
        if fence_tile_with_fence_direction not in processed_fence_tiles:
            main_fence_tile_pos = fence_tile_with_fence_direction[0]
            main_fence_tile_dir = fence_tile_with_fence_direction[1]
            check_fence_directions = [(-1, 0), (1 , 0)] if main_fence_tile_dir[0] == 0 else [(0, -1), (0, 1)]
            processed_fence_tiles.add(fence_tile_with_fence_direction)


            # go in both directions of the fence and check if there is a tile with a continuous fence.
            # if not, add fence side and remove all fence tiles from list.
            for i in range(2): # traverse up/down or left/right
                fence_traverse_pos = main_fence_tile_pos

                while True:
                    possible_next_traverse_pos = (fence_traverse_pos[0] + check_fence_directions[i][0], fence_traverse_pos[1] + check_fence_directions[i][1])
                    if (possible_next_traverse_pos, main_fence_tile_dir) in fence_tiles_with_fence_direction:
                        fence_traverse_pos = possible_next_traverse_pos
                        processed_fence_tiles.add((fence_traverse_pos, main_fence_tile_dir))
                    else:
                        break
            fence_sides += 1
    return fence_sides


def get_total_fence_price_for_plot_sides(plot_list: list[tuple[set[tuple[int, int]], list[tuple[tuple[int, int], tuple[int, int]]]]]) -> int:
    total_fence_price = 0
    for plot in plot_list:
        total_fence_price = total_fence_price + (len(plot[0]) * get_plot_fence_sides(plot))
    return total_fence_price


if __name__ == '__main__':
    input_day12 = load_data('day12.txt')
    garden_matrix_day12 = get_matrix_from_input(input_day12)
    garden_plots_day12 = get_all_garden_plots_with_border_plots(garden_matrix_day12)

    print(get_total_fence_price_for_single_tiles(garden_plots_day12))
    print(get_total_fence_price_for_plot_sides(garden_plots_day12))
