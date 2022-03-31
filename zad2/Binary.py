from typing import Union


class Binary:

    def __init__(self, file_name="binary_6x6", board_width=6) -> None:
        self.board = self.read_data(file_name)
        self.board_width = board_width

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
                    last_num = curr_num
            if how_many_in_row >= 3:
                is_good = False
                break

        for col in range(self.board_width):
            last_num = None
            how_many_in_row = 1
            for row in range(self.board_width):
                curr_num = self.board[row * self.board_width + col]
                if curr_num is not None:
                    if last_num == curr_num:
                        how_many_in_row += 1
                    last_num = curr_num
            if how_many_in_row >= 3:
                is_good = False
                break

        return is_good

    def check_unique_constraint(self) -> bool:
        wid = self.board_width

        analyzed_rows = []
        for row in range(wid):
            if self.board[(row) * wid : (row+1) * wid] in analyzed_rows:
                return False
            else:
                if None not in self.board[(row) * wid : (row + 1) * wid]:
                    analyzed_rows.append(self.board[(row) * wid : (row + 1) * wid])
        
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

            if None in self.board[row * wid : (row + 1) * wid]:
                continue
            else:
                for col in range(self.board_width):
                    if self.board[row * wid + col] == '1':
                        no_ones += 1
                    else:
                        no_zeros += 1
                
                if no_ones != no_zeros:
                    return False

        for col in range(self.board_width):
            no_ones = 0
            no_zeros = 0
            curr_col = []

            for row in range(self.board_width):
                curr_col.append(self.board[row * wid + col])

            if None in curr_col:
                continue
            else:
                for cell in curr_col:
                    if cell == '1':
                        no_ones += 1
                    else:
                        no_zeros += 1
                
                if no_ones != no_zeros:
                    return False

        return True
