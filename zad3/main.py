from Board import Board

if __name__ == "__main__":
    starting_board = Board()
    starting_board.print_board()
    while True:
        starting_board.player_move()