from Binary import Binary

solutions = 0

def backtrack(puz: Binary) -> int:
    global solutions
    next_place = puz.find_next_spot()
    
    if next_place == None:
        #puz.print_board()
        if puz.check_constraints():
            solutions += 1
            puz.print_board()
            print()
        return

    if not puz.check_constraints():
        #print("here")
        return
    
    for char in [0, 1]:
        new_puz = puz.clone()
        new_puz.update_spot(next_place, char)
        print(new_puz.board)
        backtrack(new_puz)

if __name__ == "__main__":
    puzzle = Binary("binary_8x8", board_width=8)
    backtrack(puzzle)
    print(solutions)