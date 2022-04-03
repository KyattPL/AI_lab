from copy import deepcopy
from typing import Tuple, Union


class Futoshiki:

    def __init__(self, file_name="futoshiki_4x4", board_width=4) -> None:
        self.board_width = board_width
        self.max_num = board_width
        (brd, boundaries) = self.read_data(file_name)
        self.board = brd
        self.boundaries = boundaries
        self.set_of_vals = list(range(1, board_width + 1))

    @staticmethod
    def check_inequality(num1, num2, sign) -> bool:
        if num1 is None or num2 is None:
            return True

        if num1 > num2 and sign == '>':
            return True
        elif num1 < num2 and sign == '<':
            return True
        else:
            return False

    def clone(self):
        return deepcopy(self)

    def update_spot(self, ind, val) -> None:
        self.board[ind] = val

    def print_board(self):
        for line in range(self.board_width):
            between_bounds = ""
            for cell in range(self.board_width):
                val = self.board[line * self.board_width + cell]
                to_right = self.boundaries[line * self.board_width + cell][1]
                to_bottom = self.boundaries[line * self.board_width + cell][2]

                if val is None:
                    print('x', end='')
                else:
                    print(val, end='')

                if to_right is None:
                    print(' ', end='')
                else:
                    print(to_right, end='')

                if to_bottom is None:
                    between_bounds += "  "
                elif to_bottom == ">":
                    between_bounds += "V "
                else:
                    between_bounds += "^ "
            if line != self.board_width - 1:
                print()
                print(between_bounds)

    def read_data(self, file) -> Tuple[list[Union[int, None]], list[list[Union[None, str]]]]:
        with open(file, "r") as f:
            data = f.readlines()

        wid = self.board_width

        board = []
        for line in data:
            for char in line:
                if char == 'x':
                    board.append(None)
                elif char >= '1' and char <= str(self.max_num):
                    board.append(int(char))

        cell_boundaries = []
        for i in range(wid * wid):
            cell_boundaries.append([None] * 4)

        for (ind_out, line) in enumerate(data):
            board_line = ind_out // 2
            for (ind_in, char) in enumerate(line):
                if char == '>':
                    if ind_out % 2 == 0:
                        cell_boundaries[board_line * wid +
                                        (ind_in - 1) // 2][1] = '>'
                        cell_boundaries[board_line * wid +
                                        (ind_in + 1) // 2][3] = '<'
                    else:
                        cell_boundaries[board_line * wid + ind_in][2] = '>'
                        cell_boundaries[(board_line + 1) *
                                        wid + ind_in][0] = '<'
                if char == '<':
                    if ind_out % 2 == 0:
                        cell_boundaries[board_line * wid +
                                        (ind_in - 1) // 2][1] = '<'
                        cell_boundaries[board_line * wid +
                                        (ind_in + 1) // 2][3] = '>'
                    else:
                        cell_boundaries[board_line * wid + ind_in][2] = '<'
                        cell_boundaries[(board_line + 1) *
                                        wid + ind_in][0] = '>'

        return (board, cell_boundaries)

    def check_constraints(self) -> bool:
        first = self.check_no_repeats()
        second = self.check_boundaries()

        return first and second

    def check_no_repeats(self) -> bool:
        wid = self.board_width

        for row in range(self.board_width):
            row_nums = []
            for cell in range(self.board_width):
                val = self.board[row * wid + cell]
                if val is not None:
                    if val in row_nums:
                        return False
                    else:
                        row_nums.append(val)

        for col in range(self.board_width):
            col_nums = []
            for cell in range(self.board_width):
                val = self.board[cell * wid + col]
                if val is not None:
                    if val in col_nums:
                        return False
                    else:
                        col_nums.append(val)

        return True

    def check_boundaries(self) -> bool:
        wid = self.board_width

        for row in range(self.board_width):
            for cell in range(self.board_width):
                boundaries_list = self.boundaries[row * wid + cell]
                val1 = self.board[row * wid + cell]
                if boundaries_list[0] is not None:
                    val2 = self.board[(row - 1) * wid + cell]
                    if not Futoshiki.check_inequality(val1, val2, boundaries_list[0]):
                        return False
                if boundaries_list[1] is not None:
                    val2 = self.board[row * wid + cell + 1]
                    if not Futoshiki.check_inequality(val1, val2, boundaries_list[1]):
                        return False
                if boundaries_list[2] is not None:
                    val2 = self.board[(row + 1) * wid + cell]
                    if not Futoshiki.check_inequality(val1, val2, boundaries_list[2]):
                        return False
                if boundaries_list[3] is not None:
                    val2 = self.board[row * wid + cell - 1]
                    if not Futoshiki.check_inequality(val1, val2, boundaries_list[3]):
                        return False

        return True

    def find_next_spot(self) -> Union[int, None]:
        index = None
        for (ind, spot) in enumerate(self.board):
            if spot == None:
                index = ind
                break

        return index
