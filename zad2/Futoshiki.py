from copy import deepcopy
from random import randint
from typing import Tuple, Union


class Futoshiki:

    def __init__(self, file_name="futoshiki_4x4", board_width=4, domains=None) -> None:
        self.board_width = board_width
        self.max_num = board_width
        (brd, boundaries) = self.read_data(file_name)
        self.board = brd
        self.boundaries = boundaries
        self.set_of_vals = list(range(1, board_width + 1))
        self.domains: list[Union[list[int], None]] = domains

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

    @staticmethod
    def check_inequality_domains(dom1, dom2, val2, sign) -> bool:

        if dom2 is None and val2 is None:
            print("yep")

        if sign == '>' and dom2 is not None:
            #print(dom2)
            min_in_snd = min(dom2)
            for num in dom1:
                if num <= min_in_snd:
                    return False
            
            max_in_fst = max(dom1)
            for num in dom2:
                if num >= max_in_fst:
                    return False
        elif sign == '<' and dom2 is not None:
            max_in_snd = max(dom2)
            for num in dom1:
                if num >= max_in_snd:
                    return False

            min_in_fst = min(dom1)
            for num in dom2:
                if num <= min_in_fst:
                    return False
        elif sign == '>' and dom2 is None:
            for num in dom1:
                if num <= val2:
                    return False
        else:
            for num in dom1:
                if num >= val2:
                    return False
        return True

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
                self.domains.append(list(range(1, wid + 1)))
        
        self.check_domains()


    def check_domains(self) -> bool:
        wid = self.board_width

        for row in range(wid):
            for col in range(wid):
                curr_ind = row * wid + col
                curr_val = self.board[curr_ind]
                if curr_val is not None:
                    self.domains[curr_ind] = None
                    
                    for same_row in range(wid):
                        if same_row != col and self.domains[row * wid + same_row] is not None and curr_val in self.domains[row * wid + same_row]:
                            self.domains[row * wid + same_row].remove(curr_val)
                            if len(self.domains[row * wid + same_row]) == 0:
                                self.domains[row * wid + same_row] = None
                    
                    for same_col in range(wid):
                        if same_col != row and self.domains[same_col * wid + col] is not None and curr_val in self.domains[same_col * wid + col]:
                            self.domains[same_col * wid + col].remove(curr_val)
                            if len(self.domains[same_col * wid + col]) == 0:
                                self.domains[same_col * wid + col] = None

        for i in range(wid * wid):
            if self.board[i] is None and self.domains[i] is None:
                return False

        curr_index = 0
        while curr_index != wid * wid:

            boundaries_list = self.boundaries[curr_index]

            row = curr_index // wid
            cell = curr_index % wid
            
            first_doms = self.domains[curr_index]

            # print(f'curr: {curr_index}, row: {row}, cell: {cell}')
            # print(f'up: {(row - 1) * wid + cell}')
            # print(f'right: {row * wid + cell + 1}')
            # print(f'below: {(row + 1) * wid + cell}')
            # print(f'left: {row * wid + cell - 1}')
            # print()

            if first_doms is None:
                curr_index += 1
                continue
            
            if boundaries_list[0] is not None:
                val2 = self.board[(row - 1) * wid + cell]
                snd_doms = self.domains[(row - 1) * wid + cell]
                if not Futoshiki.check_inequality_domains(first_doms, snd_doms, val2, boundaries_list[0]):
                    self.update_domains(first_doms, snd_doms, val2, boundaries_list[0])
                    curr_index = -1
            if boundaries_list[1] is not None:
                val2 = self.board[row * wid + cell + 1]
                snd_doms = self.domains[row * wid + cell + 1]
                if not Futoshiki.check_inequality_domains(first_doms, snd_doms, val2, boundaries_list[1]):
                    self.update_domains(first_doms, snd_doms, val2, boundaries_list[1])
                    curr_index = -1
            if boundaries_list[2] is not None:
                val2 = self.board[(row + 1) * wid + cell]
                snd_doms = self.domains[(row + 1) * wid + cell]
                if not Futoshiki.check_inequality_domains(first_doms, snd_doms, val2, boundaries_list[2]):
                    self.update_domains(first_doms, snd_doms, val2, boundaries_list[2])
                    curr_index = -1
            if boundaries_list[3] is not None:
                val2 = self.board[row * wid + cell - 1]
                snd_doms = self.domains[row * wid + cell - 1]
                if not Futoshiki.check_inequality_domains(first_doms, snd_doms, val2, boundaries_list[3]):
                    self.update_domains(first_doms, snd_doms, val2, boundaries_list[3])
                    curr_index = -1
            
            curr_index += 1

            for i in range(wid * wid):
                if self.board[i] is None and self.domains[i] is None:
                    return False
        
        return True

    def update_domains(self, dom1, dom2, val2, sign) -> None:
        if sign == '>' and dom2 is not None:
            min_in_snd = min(dom2)
            
            index = 0
            while index != len(dom1):
                val = dom1[index]
                if val <= min_in_snd:
                    dom1.remove(val)
                    index -= 1
                index += 1

            if len(dom1) == 0:
                dom1 = None
                print("~idk:")
                print(dom1, dom2)
                print("~end")
                return

            max_in_fst = max(dom1)
            
            index = 0
            while index != len(dom2):
                val = dom2[index]
                if val >= max_in_fst:
                    dom2.remove(val)
                    index -= 1
                index += 1
        elif sign == '<' and dom2 is not None:
            min_in_fst = min(dom1)

            index = 0
            while index != len(dom2):
                val = dom2[index]
                if val <= min_in_fst:
                    dom2.remove(val)
                    index -= 1
                index += 1

            if len(dom2) == 0:
                dom2 = None
                return

            max_in_snd = max(dom2)

            index = 0
            while index != len(dom1):
                val = dom1[index]
                if val >= max_in_snd:
                    dom1.remove(val)
                    index -= 1
                index += 1
        elif sign == '>' and dom2 is None:
            index = 0
            while index != len(dom1):
                val = dom1[index]
                if val <= val2:
                    dom1.remove(val)
                    index -= 1
                index += 1
        else:
            index = 0
            while index != len(dom1):
                val = dom1[index]
                if val >= val2:
                    dom1.remove(val)
                    index -= 1
                index +=1

        if dom1 is not None and len(dom1) == 0:
            dom1 = None
        
        if dom2 is not None and len(dom2) == 0:
            dom2 = None

        # print("prapaare")
        # print(dom1, dom2)
        # print("heregre")

        return