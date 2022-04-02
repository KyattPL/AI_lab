class Futoshiki:

    def __init__(self, file_name="futoshiki_4x4", board_width=4) -> None:
        self.board_width = board_width
        self.max_num = board_width
        self.board = self.read_data(file_name)

    def print_board(self):
        pass

    def read_data(self, file):
        with open(file, "r") as f:
            data = f.readlines()

        board = []
        for line in data:
            for char in line:
                if char == 'x':
                    board.append(None)
                elif char >= '1' and char <= str(self.max_num):
                    board.append(int(char))

        cell_boundaries = []
        for i in range(self.board_width * self.board_width):
            cell_boundaries.append([None] * 4)

        for (ind_out, line) in enumerate(data):
            for (ind_in, char) in enumerate(line):
                if char == '>':
                    if ind_out % 2 == 0:
                        cell_boundaries[ind_out * self.board_width + ind_in - 1][1] = '>'
                        cell_boundaries[ind_out * self.board_width + ind_in + 1][3] = '<'
                    else:
                        print(ind_out)
                        cell_boundaries[(ind_out - 1) * self.board_width + ind_in][2] = '>'
                        cell_boundaries[(ind_out + 1) * self.board_width + ind_in][0] = '<'
                if char == '<':
                    if ind_out % 2 == 0:
                        cell_boundaries[ind_out * self.board_width + ind_in - 1][1] = '<'
                        cell_boundaries[ind_out * self.board_width + ind_in + 1][3] = '>'
                    else:
                        cell_boundaries[(ind_out - 1) * self.board_width + ind_in][2] = '<'
                        cell_boundaries[(ind_out + 1) * self.board_width + ind_in][0] = '>'
        
        print(cell_boundaries)