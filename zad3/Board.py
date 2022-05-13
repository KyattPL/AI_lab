from copy import deepcopy
import typing as tp

from numpy import empty
from Color import Color
from Piece import Piece

class Board:

    BOARD_SIZE: int = 8

    def __init__(self) -> None:
        self.board: list[list[tp.Union[None, Piece]]] = []
        self.whose_turn = Color.White

        for _ in range(Board.BOARD_SIZE):
            temp = []
            for _ in range(Board.BOARD_SIZE):
                temp.append(None)
            self.board.append(temp)
        
        for black_row in range(3):
            for col in range(Board.BOARD_SIZE):
                if (black_row + col) % 2 == 1:
                    self.board[black_row][col] = Piece(Color.Black)

        for white_row in range(5, Board.BOARD_SIZE):
            for col in range(Board.BOARD_SIZE):
                if (white_row + col) % 2 == 1:
                    self.board[white_row][col] = Piece(Color.White)

    @staticmethod
    def clamp_to_board(row, col) -> tp.Union[None, tp.Tuple[int, int]]:
        if row < 0 or row >= Board.BOARD_SIZE:
            return None
        
        if col < 0 or col >= Board.BOARD_SIZE:
            return None
        
        return (row, col)

    def print_board(self) -> None:
        for row in self.board:
            for cell in row:
                if cell == None:
                    print('#', end=' ')
                elif cell.color == Color.White:
                    print('W', end=' ')
                else:
                    print('B', end=' ')
            print()

    def move_piece(self, piece_row, piece_col, dest_row, dest_col) -> None:
        piece = self.board[piece_row][piece_col]
        self.board[piece_row][piece_col] = None
        self.board[dest_row][dest_col] = piece

    def can_piece_move(self, row: int, col: int) -> bool:
        piece_color = self.board[row][col].color
        is_king = self.board[row][col].is_king

        q1 = Board.clamp_to_board(row - 1, col - 1)
        q2 = Board.clamp_to_board(row - 1, col + 1)
        q3 = Board.clamp_to_board(row + 1, col - 1)
        q4 = Board.clamp_to_board(row + 1, col + 1)
        qs = [q1, q2, q3, q4]

        behind_q1 = Board.clamp_to_board(row - 2, col - 2)
        behind_q2 = Board.clamp_to_board(row - 2, col + 2)
        behind_q3 = Board.clamp_to_board(row + 2, col - 2)
        behind_q4 = Board.clamp_to_board(row + 2, col + 2)
        behind_qs = [behind_q1, behind_q2, behind_q3, behind_q4]

        if is_king:
            for (index, q) in enumerate(qs):
                if q is not None:
                    if self.board[q[0]][q[1]] is None:
                        return True
                    if behind_qs[index] is not None and self.board[q[0]][q[1]].color != piece_color \
                        and self.board[behind_qs[index][0]][behind_qs[index][1]] is None:
                        return True 
        else:
            if piece_color == Color.White:
                for (index, q) in enumerate(qs[:2]):
                    if q is not None:
                        if self.board[q[0]][q[1]] is None:
                            return True
                        if behind_qs[index] is not None and self.board[q[0]][q[1]].color != piece_color \
                            and self.board[behind_qs[index][0]][behind_qs[index][1]] is None:
                            return True
            else:
                for (index, q) in enumerate(qs[2:]):
                    if q is not None:
                        if self.board[q[0]][q[1]] is None:
                            return True
                        if behind_qs[index+2] is not None and self.board[q[0]][q[1]].color != piece_color \
                            and self.board[behind_qs[index+2][0]][behind_qs[index+2][1]] is None:
                            return True                

        return False

    def recursive_king_beatings(self, board_copy: list[list[tp.Union[None, Piece]]], row: int, col: int, \
        starting_color: Color, depth: int, beatings_map: tp.Tuple[tp.Tuple[int, int], list[tp.Tuple[int, int]]]):
        
        best_depth = 0
        best_moves = []
        to_beat: dict[tp.Tuple[int, int], list[tp.Tuple[int, int]]] = {}
        qs = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

        for q in qs:
            next_row = row + q[0]
            next_col = col + q[1]

            while next_row > 0 and next_row < self.BOARD_SIZE and next_col > 0 and next_col < self.BOARD_SIZE:
                next_tile = board_copy[next_row][next_col]

                if next_tile is not None and next_tile.color == starting_color:
                    break
                elif next_tile is not None:
                    empty_tiles = []
                    beaten_piece_coords = (next_row, next_col)

                    while next_row > 0 and next_row < self.BOARD_SIZE and next_col > 0 and next_col < self.BOARD_SIZE:
                        next_row += q[0]
                        next_col += q[1]
                        next_tile = board_copy[next_row][next_col]
                        if next_tile is None:
                            empty_tiles.append((next_row, next_col))
                        else:
                            break
                    
                    if len(empty_tiles) == 0:
                        break
                    else:
                        to_beat[beaten_piece_coords] = empty_tiles
                else:
                    next_row += q[0]
                    next_col += q[1]        

        if len(to_beat.keys()) == 0:
            return (depth, beatings_map)
        else:
            for key in to_beat.keys():
                for landing_spot in to_beat[key]:
                    new_board = deepcopy(board_copy)
                    new_board[key[0]][key[1]] = None
                    new_beatings = (landing_spot, beatings_map[1])
                    new_beatings[1].append(key)
                    rec_outcome = self.recursive_king_beatings(new_board, landing_spot[0], landing_spot[1], \
                        starting_color, depth + 1, new_beatings, False)

                    if rec_outcome[0] > best_depth:
                        best_depth = rec_outcome[0]
                        best_moves = [rec_outcome[1]]
                    elif rec_outcome[0] == best_depth:
                        best_moves.append(rec_outcome[1])
        
        return best_depth, best_moves

    # def recursive_best_beating(self, board_copy: list[list[tp.Union[None, Piece]]], row: int, col: int,\
    #     starting_color: Color, current_beaten: int, best_beaten: int, best_spots: list[tp.Tuple[int, int]]):
    #     qs = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

    #     curr_best_spots = []


    #     for q in qs:
    #         next_row = row + q[0]
    #         next_col = col + q[1]

    #         while next_row > 0 and next_row < self.BOARD_SIZE and next_col > 0 and next_col < self.BOARD_SIZE:
    #             next_tile = board_copy[next_row][next_col]

    #             if next_tile is not None and next_tile.color == starting_color:
    #                 break
    #             elif next_tile is not None:
    #                 empty_tiles = []
    #                 beaten_piece_coords = (next_row, next_col)
                    
    #                 next_row += q[0]
    #                 next_col += q[1]

    #                 while next_row > 0 and next_row < self.BOARD_SIZE and next_col > 0 and next_col < self.BOARD_SIZE:
    #                     next_tile = board_copy[next_row][next_col]
    #                     if next_tile is None:
    #                         empty_tiles.append((next_row, next_col))
    #                     else:
    #                         break
                    
    #                 if len(empty_tiles) == 0:
    #                     break
    #                 else:
    #                     for tile in empty_tiles:
    #                         new_copy = deepcopy(board_copy)
    #                         new_copy[beaten_piece_coords[0]][beaten_piece_coords[1]] = None
    #                         repeated_outcome = self.recursive_best_beating(new_copy, tile[0], tile[1], starting_color, current_beaten + 1)
    #                         curr_best_spots.append(tile)
    #             else:
    #                 next_row += q[0]
    #                 next_col += q[1]

    #     if current_beaten > best_beaten:
    #         best_beaten = current_beaten
    #         best_spots = curr_best_spots
    #     elif current_beaten == best_beaten:
    #         best_spots

    #     return current_beaten, best_spots


    def get_king_best_beating(self, row: int, col: int) -> list[tp.Tuple[tp.Tuple[int, int], list[tp.Tuple[int, int]]]]:
        board_copy = deepcopy(self.board)
        _, moves = self.recursive_king_beatings(board_copy, row, col, self.board[row][col].color, 0, [[], []])
        print(moves)
        return moves

    def get_king_moves(self, row: int, col: int, color: Color) -> list[tp.Tuple[int, int]]:
        qs = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        moves_list = []

        for q in qs:
            next_row = row + q[0]
            next_col = col + q[1]
            while next_row > 0 and next_row < self.BOARD_SIZE and next_col > 0 and next_col < self.BOARD_SIZE:
                next_tile = self.board[next_row][next_col]
                if next_tile is not None:
                    break
                else:
                    moves_list.append((next_row, next_col))
                    next_row += q[0]
                    next_col += q[1]

        return moves_list

    def get_piece_best_beating(self, row: int, col: int):
        board_copy = deepcopy(self.board)
        _, moves = self.recursive_piece_beatings(board_copy, row, col, board_copy[row][col].color,\
            0, [[], []])
        print(moves)
        return moves

    def recursive_piece_beatings(self, board_copy: list[list[tp.Union[None, Piece]]], row: int, col: int, \
        starting_color: Color, depth: int, beatings_map: tp.Tuple[tp.Tuple[int, int], list[tp.Tuple[int, int]]]):
        
        best_depth = 0
        best_moves = []
        to_beat: dict[tp.Tuple[int, int], list[tp.Tuple[int, int]]] = {}
        if starting_color == Color.White:
            qs = [(-1, -1), (-1, 1)]
        else:
            qs = [(1, -1), (1, 1)]

        for q in qs:
            next_row = row + q[0]
            next_col = col + q[1]

            next_tile = board_copy[next_row][next_col]

            if next_tile is None or (next_tile is not None and next_tile.color == starting_color):
                break
            else:
                empty_tile = None
                beaten_piece_coords = (next_row, next_col)
                
                if starting_color == Color.White:
                    if next_row + q[0] >= 0 and next_col + q[1] >= 0 and next_col + q[1] < self.BOARD_SIZE:
                        if board_copy[next_row + q[0]][next_col + q[1]] is None:
                            empty_tile = (next_row + q[0], next_col + q[1])
                else:
                    if next_row + q[0] < self.BOARD_SIZE and next_col + q[1] >= 0 and next_col + q[1] < self.BOARD_SIZE:
                        if board_copy[next_row + q[0]][next_col + q[1]] is None:
                            empty_tile = (next_row + q[0], next_col + q[1])
                
                if empty_tile is None:
                    break
                else:
                    to_beat[beaten_piece_coords] = empty_tile      

        if len(to_beat.keys()) == 0:
            return (depth, beatings_map)
        else:
            for key in to_beat.keys():
                for landing_spot in to_beat[key]:
                    new_board = deepcopy(board_copy)
                    new_board[key[0]][key[1]] = None
                    new_beatings = (landing_spot, beatings_map[1])
                    new_beatings[1].append(key)
                    rec_outcome = self.recursive_king_beatings(new_board, landing_spot[0], landing_spot[1], \
                        starting_color, depth + 1, new_beatings, False)

                    if rec_outcome[0] > best_depth:
                        best_depth = rec_outcome[0]
                        best_moves = [rec_outcome[1]]
                    elif rec_outcome[0] == best_depth:
                        best_moves.append(rec_outcome[1])
        
        return best_depth, best_moves

    def get_piece_moves(self, row: int, col: int) -> list[tp.Tuple[int, int]]:
        piece_color = self.board[row][col].color
        is_king = self.board[row][col].is_king

        if is_king:
            beatings = self.get_king_best_beating(row, col)
            if beatings[0][1] != []:
                return beatings
            else:
                moves = self.get_king_moves(row, col, piece_color)
                return moves
        else:
            beatings = self.get_piece_best_beating(row, col)
            if beatings != [] and beatings[1] != []:
                return beatings
            else:
                moves = []
                if piece_color == Color.White:
                    if row - 1 >= 0 and col - 1 >= 0 and self.board[row - 1][col - 1] is None:
                        moves.append((row - 1, col - 1))
                    if row - 1 >= 0 and col + 1 < self.BOARD_SIZE and self.board[row - 1][col + 1] is None:
                        moves.append((row - 1, col + 1))
                else:
                    if row + 1 < self.BOARD_SIZE and col - 1 > 0 and self.board[row + 1][col - 1] is None:
                        moves.append((row + 1, col - 1))
                    if row + 1 < self.BOARD_SIZE and col + 1 < self.BOARD_SIZE and self.board[row + 1][col + 1] is None:
                        moves.append((row + 1, col + 1))
                return moves

    def possible_pieces_to_move(self) -> dict[tp.Tuple[int, int], list[tp.Tuple[int, int]]]:
        pieces_to_move = {}

        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] is not None and self.board[row][col].color == self.whose_turn:
                    if self.can_piece_move(row, col):
                        piece_moves = self.get_piece_moves(row, col)
                        pieces_to_move[(row, col)] = piece_moves

        return pieces_to_move

    def player_move(self) -> bool:
        pieces_to_move = self.possible_pieces_to_move()

        print(pieces_to_move)

        print("Choose piece to move:")
        piece_col = input("Column: ") # A-H
        piece_row = int(input("Row: "))

        if piece_col.lower() < 'a' or piece_col.lower() > 'h' or piece_row < 0 or piece_row > Board.BOARD_SIZE:
            return False
        
        piece_col_num = ord(piece_col) - 97
        piece_row_num = self.BOARD_SIZE - piece_row

        if self.board[piece_row_num][piece_col_num] is None or \
            self.board[piece_row_num][piece_col_num].color != self.whose_turn:
            return False

        # get piece possibilities (possible moves) - func
        
        print("Choose destination:")
        dest_col = input("Column: ") # A-H
        dest_row = int(input("Row: "))

        if dest_col.lower() < 'a' or dest_col.lower() > 'h' or dest_row < 0 or dest_row > Board.BOARD_SIZE:
            return False
        
        dest_col_num = ord(dest_col) - 97
        dest_row_num = self.BOARD_SIZE - dest_row