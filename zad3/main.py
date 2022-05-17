from Game import Game

if __name__ == "__main__":
    new_game = Game()
    while True:
        new_game.boardObj.print_board()
        new_game.player_move()