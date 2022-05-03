from copy import deepcopy
from random import randint
from time import perf_counter
from typing import Union
from Binary import Binary
from Futoshiki import Futoshiki

solutions = 0
nodes = 0
start_time = perf_counter()
end_time = None


def backtrack(puz: Union[Binary, Futoshiki], isPlaceRandom=False, isValRandom=False) -> None:
    global solutions
    global nodes
    global end_time
    nodes += 1

    if isPlaceRandom:
        next_place = puz.find_next_spot_random()
    else:
        next_place = puz.find_next_spot()

    if next_place == None:
        if puz.check_constraints():
            end_time = perf_counter()
            solutions += 1
            puz.print_board()
            print_single()
            print()
        return

    if not puz.check_constraints():
        return

    if isValRandom:
        chars_left = []
        for char in puz.set_of_vals:
            chars_left.append(char)
        while len(chars_left) != 0:
            rand_ind = randint(0, len(chars_left) - 1)
            rand_char = chars_left[rand_ind]
            new_puz = puz.clone()
            new_puz.update_spot(next_place, rand_char)
            backtrack(new_puz, isPlaceRandom, isValRandom)
            chars_left.remove(rand_char)
    else:
        for char in puz.set_of_vals:
            new_puz = puz.clone()
            new_puz.update_spot(next_place, char)
            backtrack(new_puz, isPlaceRandom, isValRandom)


def forward_checking(puz: Union[Binary, Futoshiki], isPlaceRandom=False, isValRandom=False) -> None:
    global solutions
    global nodes
    global end_time
    nodes += 1

    if isPlaceRandom:
        next_place = puz.find_next_spot_random()
    else:
        next_place = puz.find_next_spot()

    if next_place == None:
        if puz.check_constraints():
            end_time = perf_counter()
            solutions += 1
            puz.print_board()
            print_single()
            print()
        return

    if not puz.check_constraints():
        return

    if isValRandom:
        vals_left = []
        for val in puz.domains[next_place]:
            vals_left.append(val)
        while len(vals_left) != 0:
            rand_ind = randint(0, len(vals_left) - 1)
            rand_val = vals_left[rand_ind]
            new_puz = puz.clone()
            new_puz.update_spot(next_place, rand_val)
            isGood = new_puz.check_domains()
            if isGood:
                forward_checking(new_puz, isPlaceRandom, isValRandom)
            vals_left.remove(rand_val)
    else:
        possible_vals = deepcopy(puz.domains[next_place])
        for val in possible_vals:
            new_puz = puz.clone()
            new_puz.update_spot(next_place, val)
            isGood = new_puz.check_domains()
            if isGood:
                forward_checking(new_puz, isPlaceRandom, isValRandom)

    return


def print_single():
    print()
    print(f'Solutions: {solutions}')
    print(f'Nodes visited: {nodes}')
    print(f'Time: {end_time - start_time}')
    print()
    exit()


if __name__ == "__main__":
    single_width = 6
    # puzzle = Binary(
    #    f'binary_{single_width}x{single_width}', board_width=single_width)
    puzzle = Futoshiki(
        f'futoshiki_{single_width}x{single_width}', board_width=single_width)
    start_time = perf_counter()
    backtrack(puzzle, isPlaceRandom=True, isValRandom=False)
    # puzzle.init_domains()
    #forward_checking(puzzle, isPlaceRandom=True, isValRandom=True)
