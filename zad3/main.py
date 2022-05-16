from Board import Board

if __name__ == "__main__":
    starting_board = Board()
    while True:
        starting_board.print_board()
        starting_board.player_move()