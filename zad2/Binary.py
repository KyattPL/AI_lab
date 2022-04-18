from copy import deepcopy
from random import randint
from typing import Union

from pyparsing import opAssoc


class Binary:

    def __init__(self, file_name="binary_6x6", board_width=6, domains=None) -> None:
        self.board = self.read_data(file_name)
        self.board_width = board_width
        self.set_of_vals = [0, 1]
        self.domains: list[Union[list[int], None]] = domains

    def print_board(self):
        for row in range(self.board_width):
            for col in range(self.board_width):
                print(self.board[row * self.board_width + col], end='')
            print()

    def clone(self):
        return deepcopy(self)

    def update_spot(self, ind, val) -> None:
        self.board[ind] = val

    def read_data(self, file) -> list[Union[int, None]]:
        with open(file, "r") as f:
            data = f.readlines()

        result = []
        for line in data:
            for char in line:
                if char == 'x':
                    result.append(None)
                elif char == '\n':
                    pass
                else:
                    result.append(int(char))

        return result

    def check_constraints(self) -> bool:
        first = self.check_same_amount_constraint()
        second = self.check_unique_constraint()
        third = self.check_threes_constraint()

        return first and second and third

    def check_threes_constraint(self) -> bool:

        is_good = True

        for row in range(self.board_width):
            last_num = None
            how_many_in_row = 1
            for col in range(self.board_width):
                curr_num = self.board[row * self.board_width + col]
                if curr_num is not None:
                    if last_num == curr_num:
                        how_many_in_row += 1
                        if how_many_in_row == 3:
                            is_good = False
                            break
                    else:
                        how_many_in_row = 1
                    last_num = curr_num
                else:
                    how_many_in_row = 1
                    last_num = None

        for col in range(self.board_width):
            last_num = None
            how_many_in_row = 1
            for row in range(self.board_width):
                curr_num = self.board[row * self.board_width + col]
                if curr_num is not None:
                    if last_num == curr_num:
                        how_many_in_row += 1
                        if how_many_in_row == 3:
                            is_good = False
                            break
                    else:
                        how_many_in_row = 1
                    last_num = curr_num
                else:
                    how_many_in_row = 1
                    last_num = None

        return is_good

    def check_unique_constraint(self) -> bool:
        wid = self.board_width

        analyzed_rows = []
        for row in range(wid):
            if self.board[(row) * wid: (row+1) * wid] in analyzed_rows:
                return False
            else:
                if None not in self.board[(row) * wid: (row + 1) * wid]:
                    analyzed_rows.append(
                        self.board[(row) * wid: (row + 1) * wid])

        analyzed_cols = []
        for col in range(wid):
            curr_col = []
            for row in range(wid):
                curr_col.append(self.board[row * wid + col])
            if curr_col in analyzed_cols:
                return False
            else:
                if None not in curr_col:
                    analyzed_cols.append(curr_col)

        return True

    def check_same_amount_constraint(self) -> bool:
        wid = self.board_width

        for row in range(self.board_width):
            no_ones = 0
            no_zeros = 0

            if None in self.board[row * wid: (row + 1) * wid]:
                continue
            else:
                for col in range(self.board_width):
                    if self.board[row * wid + col] == 1:
                        no_ones += 1
                    else:
                        no_zeros += 1

                if no_ones != no_zeros:
                    return False

        for col in range(wid):
            no_ones = 0
            no_zeros = 0
            curr_col = []

            for row in range(wid):
                curr_col.append(self.board[row * wid + col])

            if None in curr_col:
                continue
            else:
                for cell in curr_col:
                    if cell == 1:
                        no_ones += 1
                    else:
                        no_zeros += 1

                if no_ones != no_zeros:
                    return False

        return True

    def find_next_spot(self) -> Union[int, None]:
        index = None
        for (ind, spot) in enumerate(self.board):
            if spot == None:
                index = ind
                break

        return index

    def find_next_spot_random(self) -> Union[int, None]:
        free_spots = []
        for (ind, spot) in enumerate(self.board):
            if spot is None:
                free_spots.append(ind)
        
        if len(free_spots) == 0:
            return None
        else:
            rand_num = randint(0, len(free_spots) - 1)
            return free_spots[rand_num]

    def init_domains(self) -> None:
        self.domains = []
        wid = self.board_width

        for i in range(wid * wid):
            if self.board[i] is not None:
                self.domains.append(None)
            else:
                self.domains.append([0, 1])

        self.check_domains()

    def check_domains(self) -> bool:
        wid = self.board_width

        for row in range(wid):
            for col in range(wid):
                if col >= 2 and col <= wid - 3:
                    curr_doms = self.domains[row * wid + col]
                    left = self.board[row * wid + col-2 : row * wid + col]
                    left_doms = self.domains[row * wid + col-2: row * wid + col]
                    right = self.board[row * wid + col+1 : row * wid + col+3]
                    right_doms = self.domains[row * wid + col+1 : row * wid + col+3]
                    
                    if curr_doms is not None:
                        self.update_domain(curr_doms, left, left_doms, right, right_doms)
                elif col == 1:
                    curr_doms = self.domains[row * wid + col]
                    left = self.board[row * wid + col - 1]
                    left_doms = self.domains[row * wid + col - 1]
                    right = self.board[row * wid + col+1 : row * wid + col+3]
                    right_doms = self.domains[row * wid + col+1 : row * wid + col+3]

                    if curr_doms is not None:
                        self.update_domain(curr_doms, [left], [left_doms], right, right_doms)
                elif col == wid - 2:
                    curr_doms = self.domains[row * wid + col]
                    left = self.board[row * wid + col-2 : row * wid + col]
                    left_doms = self.domains[row * wid + col-2: row * wid + col]
                    right = self.board[row * wid + col+1]
                    right_doms = self.domains[row * wid + col+1]

                    if curr_doms is not None: 
                        self.update_domain(curr_doms, left, left_doms, [right], [right_doms])
                elif col == 0:
                    curr_doms = self.domains[row * wid + col]
                    right = self.board[row * wid + col+1 : row * wid + col+3]
                    right_doms = self.domains[row * wid + col+1 : row * wid + col+3]

                    if curr_doms is not None:
                        self.update_domain(curr_doms, None, None, right, right_doms)
                else:
                    curr_doms = self.domains[row * wid + col]
                    left = self.board[row * wid + col-2 : row * wid + col]
                    left_doms = self.domains[row * wid + col-2 : row * wid + col]

                    if curr_doms is not None:
                        self.update_domain(curr_doms, left, left_doms, None, None)
        
        for i in range(wid * wid):
            if self.board[i] is None and self.domains[i] is None:
                return False

        return True

    def update_domain(self, curr_doms, left, left_doms, right, right_doms) -> None:
        if left is not None and right is not None:
            if len(left) == 1:
                single_left = left[0]
                first_right = right[0]
                second_right = right[1]

                left_decider = Binary.choose_decider(single_left, left_doms)
                fst_right_decider = Binary.choose_decider(first_right, right_doms[0])
                snd_right_decider = Binary.choose_decider(second_right, right_doms[1])

                if left_decider == fst_right_decider and left_decider in curr_doms:
                    curr_doms.remove(left_decider)

                if fst_right_decider == snd_right_decider and fst_right_decider in curr_doms:
                    curr_doms.remove(fst_right_decider)
            elif len(right) == 1:
                first_left = left[0]
                second_left = left[1]
                single_right = right[0]

                fst_left_decider = Binary.choose_decider(first_left, left_doms[0])
                snd_left_decider = Binary.choose_decider(second_left, left_doms[1])
                right_decider = Binary.choose_decider(single_right, right_doms)

                if fst_left_decider == snd_left_decider and fst_left_decider in curr_doms:
                    curr_doms.remove(fst_left_decider)
                
                if snd_left_decider == right_decider and right_decider in curr_doms:
                    curr_doms.remove(right_decider)
            else:
                first_left = left[0]
                second_left = left[1]
                first_right = right[0]
                second_right = right[1]

                fst_left_decider = Binary.choose_decider(first_left, left_doms[0])
                snd_left_decider = Binary.choose_decider(second_left, left_doms[1])
                fst_right_decider = Binary.choose_decider(first_right, right_doms[0])
                snd_right_decider = Binary.choose_decider(second_right, right_doms[1])

                if fst_left_decider == snd_left_decider and fst_left_decider in curr_doms:
                    curr_doms.remove(fst_left_decider)

                if snd_left_decider == fst_right_decider and snd_left_decider in curr_doms:
                    curr_doms.remove(snd_left_decider)

                if fst_right_decider == snd_right_decider and fst_right_decider in curr_doms:
                    curr_doms.remove(fst_right_decider)
        elif left is not None:
            first_left = left[0]
            second_left = left[1]

            fst_left_decider = Binary.choose_decider(first_left, left_doms[0])
            snd_left_decider = Binary.choose_decider(second_left, left_doms[1])

            if fst_left_decider == snd_left_decider and fst_left_decider in curr_doms:
                curr_doms.remove(fst_left_decider)
        else:
            first_right = right[0]
            second_right = right[1]

            fst_right_decider = Binary.choose_decider(first_right, right_doms[0])
            snd_right_decider = Binary.choose_decider(second_right, right_doms[1])

            if fst_right_decider == snd_right_decider and fst_right_decider in curr_doms:
                curr_doms.remove(fst_right_decider)
        
        if len(curr_doms) == 0:
            curr_doms = None

    @staticmethod
    def choose_decider(val, doms) -> Union[int, None]:
        if val is None and len(doms) == 1:
            return doms[0]
        elif val is not None:
            return val
        else:
            return None