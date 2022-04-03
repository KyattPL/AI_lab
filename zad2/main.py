from typing import Union
from Binary import Binary
from Futoshiki import Futoshiki

solutions = 0
set_of_vals = [1, 2, 3, 4]


def backtrack(puz: Union[Binary, Futoshiki]) -> int:
    global solutions
    next_place = puz.find_next_spot()

    if next_place == None:
        if puz.check_constraints():
            solutions += 1
            puz.print_board()
            print()
        return

    if not puz.check_constraints():
        return

    for char in puz.set_of_vals:
        new_puz = puz.clone()
        new_puz.update_spot(next_place, char)
        backtrack(new_puz)


if __name__ == "__main__":
    #puzzle = Binary("binary_10x10", board_width=10)
    # backtrack(puzzle)
    # print(solutions)
    puz_snd = Futoshiki("futoshiki_6x6", board_width=6)
    backtrack(puz_snd)
    print(solutions)
