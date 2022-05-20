from BoardEval import BoardEval
from Game import Game
from GameResult import GameResult

# TODO: losowy start
# TODO: ai z jedną heurystyką vs ai z inną heurystyką


def ai_vs_ai(eval_func) -> GameResult:
    new_game = Game()
    is_done = False
    while not is_done:
        new_game.boardObj.print_board()
        state = new_game.ai_move("alfa", eval_func, depth=5)
        if state is not None:
            is_done = True
    new_game.boardObj.print_board()
    print(str(state))


if __name__ == "__main__":
    ai_vs_ai(BoardEval.board_value_1)
