from copy import deepcopy
import os
import typing as tp

from Color import Color
from GameResult import GameResult
from Piece import Piece


class Board:

    BOARD_SIZE: int = 8

    def __init__(self) -> None:
        self.board: list[list[tp.Union[None, Piece]]] = []
        self.whose_turn = Color.White
        self.kings_only = False
        self.turns_with_kings_only = 0

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
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        for row in self.board:
            for cell in row:
                if cell == None:
                    print('.', end=' ')
                elif cell.color == Color.White and not cell.is_king:
                    print('W', end=' ')
                elif cell.color == Color.Black and not cell.is_king:
                    print('B', end=' ')
                elif cell.color == Color.White and cell.is_king:
                    print('w', end=' ')
                else:
                    print('b', end=' ')
            print()

    def move_piece(self, piece_row, piece_col, dest_row, dest_col) -> None:
        piece = self.board[piece_row][piece_col]
        self.board[piece_row][piece_col] = None
        self.board[dest_row][dest_col] = piece

    def destroy_piece(self, piece_row, piece_col) -> None:
        self.board[piece_row][piece_col] = None

    def can_piece_move(self, row: int, col: int) -> bool:
        piece_color = self.board[row][col].color
        is_king = self.board[row][col].is_king

        q1 = Board.clamp_to_board(row - 1, col - 1)  # WHITE
        q2 = Board.clamp_to_board(row - 1, col + 1)  # WHITE
        q3 = Board.clamp_to_board(row + 1, col - 1)  # BLACK
        q4 = Board.clamp_to_board(row + 1, col + 1)  # BLACK
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
                for (index, q) in enumerate(qs):
                    if q is not None:
                        if index < 2 and self.board[q[0]][q[1]] is None:
                            return True
                        if behind_qs[index] is not None and self.board[q[0]][q[1]] is not None \
                                and self.board[q[0]][q[1]].color != piece_color \
                                and self.board[behind_qs[index][0]][behind_qs[index][1]] is None:
                            return True
            else:
                for (index, q) in enumerate(qs):
                    if q is not None:
                        if index > 1 and self.board[q[0]][q[1]] is None:
                            return True
                        if behind_qs[index] is not None and self.board[q[0]][q[1]] is not None \
                                and self.board[q[0]][q[1]].color != piece_color \
                                and self.board[behind_qs[index][0]][behind_qs[index][1]] is None:
                            return True

        return False

    def recursive_king_beatings(self, board_copy: list[list[tp.Union[None, Piece]]], row: int, col: int,
                                starting_color: Color, depth: int, beatings_map: tp.Tuple[tp.Tuple[int, int], list[tp.Tuple[int, int]]]):

        best_depth = 0
        best_moves = []
        to_beat: dict[tp.Tuple[int, int], list[tp.Tuple[int, int]]] = {}
        qs = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

        for q in qs:
            next_row = row + q[0]
            next_col = col + q[1]

            while next_row > 0 and next_row < self.BOARD_SIZE - 1 and next_col > 0 and next_col < self.BOARD_SIZE - 1:
                next_tile = board_copy[next_row][next_col]

                if next_tile is not None and next_tile.color == starting_color:
                    break
                elif next_tile is not None:
                    empty_tiles = []
                    beaten_piece_coords = (next_row, next_col)

                    while next_row + q[0] >= 0 and next_row + q[0] < self.BOARD_SIZE and next_col + q[1] >= 0 and next_col + q[1] < self.BOARD_SIZE:
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
                        break
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
                    new_board[landing_spot[0]][landing_spot[1]
                                               ] = Piece(starting_color, True)
                    new_board[row][col] = None
                    new_beatings = (landing_spot, deepcopy(beatings_map[1]))
                    new_beatings[1].append(key)
                    rec_outcome = self.recursive_king_beatings(new_board, landing_spot[0], landing_spot[1],
                                                               starting_color, depth + 1, new_beatings)

                    if rec_outcome[0] > best_depth:
                        best_depth = rec_outcome[0]
                        if isinstance(rec_outcome[1], tuple):
                            best_moves = [rec_outcome[1]]
                        elif isinstance(rec_outcome[1], list):
                            best_moves = rec_outcome[1]
                    elif rec_outcome[0] == best_depth:
                        if isinstance(rec_outcome[1], list):
                            for outc in rec_outcome[1]:
                                best_moves.append(outc)
                        else:
                            best_moves.append(rec_outcome[1])

        return best_depth, best_moves

    def get_king_best_beating(self, row: int, col: int) -> list[tp.Tuple[tp.Tuple[int, int], list[tp.Tuple[int, int]]]]:
        board_copy = deepcopy(self.board)
        beaten_no, moves = self.recursive_king_beatings(
            board_copy, row, col, board_copy[row][col].color, 0, [[], []])
        return beaten_no, moves

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
        beaten_no, moves = self.recursive_piece_beatings(board_copy, row, col, board_copy[row][col].color,
                                                         0, [[], []])
        return beaten_no, moves

    def recursive_piece_beatings(self, board_copy: list[list[tp.Union[None, Piece]]], row: int, col: int,
                                 starting_color: Color, depth: int, beatings_map: tp.Tuple[tp.Tuple[int, int], list[tp.Tuple[int, int]]]):

        best_depth = 0
        best_moves = []
        to_beat: dict[tp.Tuple[int, int], list[tp.Tuple[int, int]]] = {}
        qs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for q in qs:
            clamped = Board.clamp_to_board(row + q[0], col + q[1])

            if clamped is None:
                continue

            next_row = clamped[0]
            next_col = clamped[1]

            next_tile = board_copy[next_row][next_col]

            if next_tile is None or (next_tile is not None and next_tile.color == starting_color):
                continue
            else:
                empty_tile = None
                beaten_piece_coords = (next_row, next_col)

                if next_row + q[0] >= 0 and next_row + q[0] < self.BOARD_SIZE and next_col + q[1] >= 0 and next_col + q[1] < self.BOARD_SIZE:
                    if board_copy[next_row + q[0]][next_col + q[1]] is None:
                        empty_tile = (next_row + q[0], next_col + q[1])

                if empty_tile is None:
                    continue
                else:
                    if beaten_piece_coords in to_beat.keys():
                        to_beat[beaten_piece_coords].append(empty_tile)
                    else:
                        to_beat[beaten_piece_coords] = [empty_tile]

        if len(to_beat.keys()) == 0:
            return (depth, beatings_map)
        else:
            for key in to_beat.keys():
                for landing_spot in to_beat[key]:
                    new_board = deepcopy(board_copy)
                    new_board[key[0]][key[1]] = None
                    new_board[landing_spot[0]][landing_spot[1]
                                               ] = Piece(starting_color)
                    new_board[row][col] = None
                    new_beatings = (landing_spot, deepcopy(beatings_map[1]))
                    new_beatings[1].append(key)
                    rec_outcome = self.recursive_piece_beatings(new_board, landing_spot[0], landing_spot[1],
                                                                starting_color, depth + 1, new_beatings)

                    if rec_outcome[0] > best_depth:
                        best_depth = rec_outcome[0]
                        if isinstance(rec_outcome[1], tuple):
                            best_moves = [rec_outcome[1]]
                        elif isinstance(rec_outcome[1], list):
                            best_moves = rec_outcome[1]
                    elif rec_outcome[0] == best_depth:
                        if isinstance(rec_outcome[1], list):
                            for outc in rec_outcome[1]:
                                best_moves.append(outc)
                        else:
                            best_moves.append(rec_outcome[1])

        return best_depth, best_moves

    def get_piece_moves(self, row: int, col: int) -> tp.Tuple[list[tp.Tuple[int, int]], bool]:
        piece_color = self.board[row][col].color
        is_king = self.board[row][col].is_king

        if is_king:
            beaten_no, beatings = self.get_king_best_beating(row, col)
            if beatings != [[], []]:
                return beatings, True, beaten_no
            else:
                moves = self.get_king_moves(row, col, piece_color)
                return moves, False, None
        else:
            beaten_no, beatings = self.get_piece_best_beating(row, col)
            if beatings != [[], []]:
                return beatings, True, beaten_no
            else:
                moves = []
                if piece_color == Color.White:
                    if row - 1 >= 0 and col - 1 >= 0 and self.board[row - 1][col - 1] is None:
                        moves.append((row - 1, col - 1))
                    if row - 1 >= 0 and col + 1 < self.BOARD_SIZE and self.board[row - 1][col + 1] is None:
                        moves.append((row - 1, col + 1))
                else:
                    if row + 1 < self.BOARD_SIZE and col - 1 >= 0 and self.board[row + 1][col - 1] is None:
                        moves.append((row + 1, col - 1))
                    if row + 1 < self.BOARD_SIZE and col + 1 < self.BOARD_SIZE and self.board[row + 1][col + 1] is None:
                        moves.append((row + 1, col + 1))
                return moves, False, None

    def possible_pieces_to_move(self) -> dict[tp.Tuple[int, int], list[tp.Tuple[int, int]]]:
        pieces_to_move = {}
        best_beating_no = 0

        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] is not None and self.board[row][col].color == self.whose_turn:
                    if self.can_piece_move(row, col):
                        piece_moves, is_beating, beaten_no = self.get_piece_moves(
                            row, col)
                        if is_beating and beaten_no > 0:
                            if beaten_no >= best_beating_no:
                                if beaten_no > best_beating_no:
                                    pieces_to_move = {}
                                    best_beating_no = beaten_no
                                outcomes = {}
                                for beating in piece_moves:
                                    landing_spot = beating[0]
                                    to_dest = beating[1]
                                    outcomes[landing_spot] = to_dest
                                pieces_to_move[(row, col)] = outcomes
                        elif not is_beating and best_beating_no == 0:
                            pieces_to_move[(row, col)] = piece_moves

        return pieces_to_move

    def check_kings(self) -> None:
        for col in range(self.BOARD_SIZE):
            if self.board[self.BOARD_SIZE - 1][col] is not None \
                    and self.board[self.BOARD_SIZE - 1][col].color == Color.Black:
                self.board[self.BOARD_SIZE - 1][col].become_king()
            if self.board[0][col] is not None and self.board[0][col].color == Color.White:
                self.board[0][col].become_king()

    def are_kings_only(self) -> bool:
        white_pieces = 0
        black_pieces = 0
        for row in range(Board.BOARD_SIZE):
            for col in range(Board.BOARD_SIZE):
                if self.board[row][col] is not None:
                    if self.board[row][col].color == Color.Black \
                            and not self.board[row][col].is_king:
                        black_pieces += 1

                    if self.board[row][col].color == Color.White \
                            and not self.board[row][col].is_king:
                        white_pieces += 1

        if white_pieces == 0 or black_pieces == 0:
            return True
        else:
            return False

    def are_pieces_left(self) -> bool:
        white_pieces = 0
        black_pieces = 0
        for row in range(Board.BOARD_SIZE):
            for col in range(Board.BOARD_SIZE):
                if self.board[row][col] is not None:
                    if self.board[row][col].color == Color.Black:
                        black_pieces += 1

                    if self.board[row][col].color == Color.White:
                        white_pieces += 1

        if white_pieces == 0 or black_pieces == 0:
            return False
        else:
            return True

    def check_end(self) -> tp.Union[GameResult, None]:
        if not self.are_pieces_left():
            if self.whose_turn == Color.White:
                return GameResult.WHITE_WIN
            else:
                return GameResult.BLACK_WIN

        if self.kings_only:
            self.turns_with_kings_only += 1

        self.check_kings()

        if self.are_kings_only():
            self.kings_only = True

        if self.turns_with_kings_only == 15:
            return GameResult.TIE

        return None

    def next_boards(self):
        pieces_to_move = self.possible_pieces_to_move()
        boards = []

        for piece in pieces_to_move.keys():
            possible_spots = pieces_to_move[piece]

            if isinstance(possible_spots, list):
                for spot in possible_spots:
                    new_board = deepcopy(self)
                    new_board.move_piece(piece[0], piece[1], spot[0], spot[1])
                    if new_board.whose_turn == Color.White:
                        new_board.whose_turn = Color.Black
                    else:
                        new_board.whose_turn = Color.White
                    Board.update_kings_next_boards(new_board)
                    boards.append(new_board)
            else:
                for spot in possible_spots.keys():
                    new_board = deepcopy(self)
                    new_board.move_piece(piece[0], piece[1], spot[0], spot[1])
                    for dest in possible_spots[spot[0], spot[1]]:
                        new_board.destroy_piece(dest[0], dest[1])
                    if new_board.whose_turn == Color.White:
                        new_board.whose_turn = Color.Black
                    else:
                        new_board.whose_turn = Color.White
                    Board.update_kings_next_boards(new_board)
                    boards.append(new_board)

        return boards

    @staticmethod
    def update_kings_next_boards(board) -> None:
        if board.kings_only:
            board.turns_with_kings_only += 1

        board.check_kings()
