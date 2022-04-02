from typing import Tuple, Union


class Futoshiki:

    def __init__(self, file_name="futoshiki_4x4", board_width=4) -> None:
        self.board_width = board_width
        self.max_num = board_width
        (brd, boundaries) = self.read_data(file_name)
        self.board = brd
        self.boundaries = boundaries

    def print_board(self):
        pass

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
                        cell_boundaries[board_line * wid + ind_in - 1][2] = '>'
                        cell_boundaries[board_line * wid + ind_in + 1][0] = '<'
                if char == '<':
                    if ind_out % 2 == 0:
                        cell_boundaries[board_line * wid +
                                        (ind_in - 1) // 2][1] = '<'
                        cell_boundaries[board_line * wid +
                                        (ind_in + 1) // 2][3] = '>'
                    else:
                        cell_boundaries[board_line * wid + ind_in - 1][2] = '<'
                        cell_boundaries[board_line * wid + ind_in + 1][0] = '>'

        return (board, cell_boundaries)
