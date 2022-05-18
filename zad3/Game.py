from copy import deepcopy
from Board import Board
from BoardEval import BoardEval
from GameResult import GameResult
from Color import Color

# TODO: min-max i alfa-beta
# TODO: zrobić 3 kontrolery: PvP, PvAI, AIvAI
# TODO: 4 osobne funkcje oceniające stan planszy

class Game:

    def __init__(self) -> None:
        self.boardObj = Board()
        self.kings_only = False
        self.turns_with_kings_only = 0

    def are_kings_only(self) -> bool:
        white_pieces = 0
        black_pieces = 0
        for row in range(self.boardObj.BOARD_SIZE):
            for col in range(self.boardObj.BOARD_SIZE):
                if self.boardObj.board[row][col] is not None:
                    if self.boardObj.board[row][col].color == Color.Black \
                        and not self.boardObj.board[row][col].is_king:
                            black_pieces += 1
                    
                    if self.boardObj.board[row][col].color == Color.White \
                        and not self.boardObj.board[row][col].is_king:
                            white_pieces += 1
        
        if white_pieces == 0 or black_pieces == 0:
            return True
        else:
            return False

    def are_pieces_left(self) -> bool:
        white_pieces = 0
        black_pieces = 0
        for row in range(self.boardObj.BOARD_SIZE):
            for col in range(self.boardObj.BOARD_SIZE):
                if self.boardObj.board[row][col] is not None:
                    if self.boardObj.board[row][col].color == Color.Black:
                            black_pieces += 1
                    
                    if self.boardObj.board[row][col].color == Color.White:
                            white_pieces += 1
        
        if white_pieces == 0 or black_pieces == 0:
            return False
        else:
            return True

    def player_move(self) -> GameResult:
        pieces_to_move = self.boardObj.possible_pieces_to_move()

        if pieces_to_move == {}:
            if self.boardObj.whose_turn == Color.Black:
                return GameResult.WHITE_WIN
            else:
                return GameResult.BLACK_WIN

        print(pieces_to_move)
        print("Pieces to move: ", end='')

        for piece in pieces_to_move.keys():
            print(f'{chr(piece[1] + 65)}{Board.BOARD_SIZE - piece[0]}', end=' ')

        print("\nChoose piece to move:")
        piece_col = input("Column: ")  # A-H
        piece_row = int(input("Row: "))

        if piece_col.lower() < 'a' or piece_col.lower() > 'h' or piece_row < 0 or piece_row > Board.BOARD_SIZE:
            return False

        piece_col_num = ord(piece_col) - 65
        piece_row_num = Board.BOARD_SIZE - piece_row

        if self.boardObj.board[piece_row_num][piece_col_num] is None or \
                self.boardObj.board[piece_row_num][piece_col_num].color != self.boardObj.whose_turn:
            return False

        print("Possbile spots: ", end='')
        possible_spots = pieces_to_move[(piece_row_num, piece_col_num)]
        if isinstance(possible_spots, list):
            for spot in possible_spots:
                print(
                    f"{chr(spot[1] + 65)}{Board.BOARD_SIZE - spot[0]}", end=' ')
        else:
            for spot in possible_spots.keys():
                print(
                    f"{chr(spot[1] + 65)}{Board.BOARD_SIZE - spot[0]}", end=' ')

        dest_col = input("\nColumn: ")  # A-H
        dest_row = int(input("Row: "))

        if dest_col.lower() < 'a' or dest_col.lower() > 'h' or dest_row < 0 or dest_row > Board.BOARD_SIZE:
            return False

        dest_col_num = ord(dest_col) - 65
        dest_row_num = Board.BOARD_SIZE - dest_row

        if isinstance(possible_spots, list):
            self.boardObj.move_piece(piece_row_num, piece_col_num,
                            dest_row_num, dest_col_num)
        else:
            self.boardObj.move_piece(piece_row_num, piece_col_num,
                            dest_row_num, dest_col_num)
            for dest in possible_spots[dest_row_num, dest_col_num]:
                self.boardObj.destroy_piece(dest[0], dest[1])

        if not self.are_pieces_left():
            if self.boardObj.whose_turn == Color.White:
                return GameResult.WHITE_WIN
            else:
                return GameResult.BLACK_WIN

        if self.kings_only:
            self.turns_with_kings_only += 1

        self.boardObj.check_kings()

        if self.are_kings_only():
            self.kings_only = True

        if self.turns_with_kings_only == 15:
            return GameResult.TIE

        if self.boardObj.whose_turn == Color.White:
            self.boardObj.whose_turn = Color.Black
        else:
            self.boardObj.whose_turn = Color.White

    def ai_move(self, board_eval) -> GameResult:
        pieces_to_move = self.boardObj.possible_pieces_to_move()

        if pieces_to_move == {}:
            if self.boardObj.whose_turn == Color.Black:
                return GameResult.WHITE_WIN
            else:
                return GameResult.BLACK_WIN

        # to całe niżej useless
        # trzeba zrobić tak, że przekazuje boarda
        # do minmax() albo alfabeta()
        # i on w środku dla planszy generuje sobie
        # magicznie listę dzieci
        
        new_board = self.boardObj.board
        BoardEval.min_max(new_board, 3, True, BoardEval.board_value_1)
        BoardEval.alfa_beta(new_board, 3, float("-inf"), float("inf"), True, BoardEval.board_value_1)

        # for piece in pieces_to_move.keys():
        #     possible_spots = pieces_to_move[piece]
        #     new_board = deepcopy(self.boardObj.board)
            
        #     if isinstance(possible_spots, list):
        #         for spot in possible_spots:
        #             new_board.move_piece(piece[0], piece[1], spot[0], spot[1])
        #             # eval here
        #     else:
        #         for spot in possible_spots.keys():
        #             new_board.move_piece(piece[0], piece[1], spot[0], spot[1])
        #             for dest in possible_spots[spot[0], spot[1]]:
        #                 new_board.destroy_piece(dest[0], dest[1])
        #             # eval here