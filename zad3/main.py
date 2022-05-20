from BoardEval import BoardEval
from Game import Game
from GameResult import GameResult
from time import process_time

avg_time = 0
avg_turns = 0
white_wins = 0
black_wins = 0
ties = 0

def ai_vs_ai(algo, eval_func_white, eval_func_black, dep, randomStart=True) -> GameResult:
    global avg_time
    global avg_turns
    global white_wins
    global black_wins
    global ties

    new_game = Game()
    is_done = False
    white_turn = True
    eval_func = eval_func_white

    turns = 0
    start_time = process_time() 

    if randomStart:
        new_game.random_start()
        white_turn = False
        eval_func = eval_func_black
        turns += 1

    while not is_done:
        new_game.boardObj.print_board()
        state = new_game.ai_move(algo, eval_func, depth=dep)
        turns += 1
        if state is not None:
            is_done = True
        
        if white_turn:
            white_turn = False
            eval_func = eval_func_black
        else:
            white_turn = True
            eval_func = eval_func_white
    
    if state == GameResult.WHITE_WIN:
        white_wins += 1
    elif state == GameResult.BLACK_WIN:
        black_wins += 1
    else:
        ties += 1
    
    avg_time += process_time() - start_time
    avg_turns += turns

    new_game.boardObj.print_board()
    print(str(state))
    print(process_time() - start_time)
    print("Turns: " + str(turns))


if __name__ == "__main__":
    depth = 3

    for i in range(10):
        ai_vs_ai("alfa", BoardEval.board_value_2, BoardEval.board_value_2, depth)

    print(f"Avg turns: {avg_turns / 10}")
    print(f"Avg time: {avg_time / 10}")
    print(f"Wins (W/B/T): {white_wins}/{black_wins}/{ties}")