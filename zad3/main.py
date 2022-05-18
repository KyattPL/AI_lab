from time import sleep

from BoardEval import BoardEval
from Game import Game
from GameResult import GameResult

def ai_vs_ai(eval_func) -> GameResult:
    new_game = Game()
    is_done = False
    turns = 0
    while not is_done:
        new_game.boardObj.print_board()
        turns += 1
        if turns == 22:
            print("22")
        state = new_game.ai_move("alfa", eval_func, depth=5)
        if state is not None:
            is_done = True
    new_game.boardObj.print_board()
    print(str(state))

if __name__ == "__main__":
    ai_vs_ai(BoardEval.board_value_1)