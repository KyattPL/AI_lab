from Board import Board

class BoardEval:

    @staticmethod
    def board_value_1(board: Board) -> int:
        pass

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
    def min_max(position: Board, depth: int, is_max: bool, eval_func) -> int:
        pass
        #if depth == 0 or game over in position
        #    return eval_func(position)
        
        #if is_max:
            #maxEval = float("-inf")
            # for each child in position:
                # eval = min_max(child, depth - 1, False, eval_func)
                # maxEval = max(maxEval, eval)
            # return maxEval
        #else:
            # minEval = float("inf")
            # for each child in position:
                # eval = min_max(child, depth - 1, True, eval_func)
                # minEval = min(minEval, eval)
            # return minEval

    @staticmethod
    def alfa_beta(position: Board, depth: int, alpha: int, beta: int, is_max: bool, eval_func) -> int:
        pass
        #if depth == 0 or game over in position
        #    return eval_func(position)
        
        #if is_max:
            #maxEval = float("-inf")
            # for each child in position:
                # eval = min_max(child, depth - 1, alpha, beta, False, eval_func)
                # maxEval = max(maxEval, eval)
                # alpha = max(alpha, eval)
                # if beta <= alpha
                    # break
            # return maxEval
        #else:
            # minEval = float("inf")
            # for each child in position:
                # eval = min_max(child, depth - 1, alpha, beta, True, eval_func)
                # minEval = min(minEval, eval)
                # beta = min(beta, eval)
                # if beta <= alpha
                    # break
            # return minEval