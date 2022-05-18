import typing as tp

from Board import Board
from Color import Color

class BoardEval:

    counter = 0

    @staticmethod
    def board_value_1(board: Board) -> int:
        white_pieces = 0
        black_pieces = 0
        for row in range(Board.BOARD_SIZE):
            for col in range(Board.BOARD_SIZE):
                if board.board[row][col] is not None:
                    if board.board[row][col].color == Color.Black:
                            black_pieces += 1
                    
                    if board.board[row][col].color == Color.White:
                            white_pieces += 1
        
        return white_pieces - black_pieces

    @staticmethod
    def board_value_2(board: Board) -> int:
        pass

    @staticmethod
    def board_value_3(board: Board) -> int:
        pass

    @staticmethod
    def board_value_4(board: Board) -> int:
        pass

    @staticmethod
    def min_max(position: Board, depth: int, is_max: bool, eval_func) -> tp.Tuple[int, Board]:
        
        if depth == 0 or position.check_end() is not None:
           return eval_func(position), position
        
        if depth == 1:
            BoardEval.counter += 1
        
        if BoardEval.counter == 26614:
            print(BoardEval.counter)

        if is_max:
            maxEval = float("-inf")
            best_board = position
            for child in position.next_boards():
                eval = BoardEval.min_max(child, depth - 1, False, eval_func)
                if eval[0] > maxEval:
                    maxEval = eval[0]
                    best_board = child
            return maxEval, best_board
        else:
            minEval = float("inf")
            best_board = position
            for child in position.next_boards():
                eval = BoardEval.min_max(child, depth - 1, True, eval_func)
                if eval[0] < minEval:
                    minEval = eval[0]
                    best_board = child
            return minEval, best_board

    @staticmethod
    def alpha_beta(position: Board, depth: int, alpha: int, beta: int, is_max: bool, eval_func) -> tp.Tuple[int, Board]:
        if depth == 0 or position.check_end() is not None:
           return eval_func(position), position
        
        if is_max:
            maxEval = float("-inf")
            best_board = position
            for child in position.next_boards():
                eval = BoardEval.alpha_beta(child, depth - 1, alpha, beta, False, eval_func)
                if eval[0] > maxEval:
                    maxEval = eval[0]
                    best_board = child
                alpha = max(alpha, eval[0])
                if beta <= alpha:
                    break
            return maxEval, best_board
        else:
            minEval = float("inf")
            best_board = position
            for child in position.next_boards():
                eval = BoardEval.alpha_beta(child, depth - 1, alpha, beta, True, eval_func)
                if eval[0] < minEval:
                    minEval = eval[0]
                    best_board = child
                beta = min(beta, eval[0])
                if beta <= alpha:
                    break
            return minEval, best_board