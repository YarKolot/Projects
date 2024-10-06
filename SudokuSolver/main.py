def if_contains_right_c(board):
    for c in '"[],".':
        if c not in board:
            return False
    return True

def is_right(user_input):
    symbols = []
    for c in user_input:
        if c in "123456789.":
            symbols.append(c)
    if len(symbols) != 81:
        return False
    return symbols

def board_creator(arr):
    board = []
    row = []

    for i in range(81):
        row.append(arr[i])
        if (i + 1) % 9 == 0:
            board.append(row)
            row = []

    print("Your board:")
    for r in board:
        print(r)

    return board
    
def board_out_of_nums():
    user_input = input()
    if is_right(user_input):
        return board_creator(is_right(user_input))
    else:
        print("Number of elements is not equell 81. Check if all elements were inputed from suggested range. Try again: ")
        return board_out_of_nums()

def ready_board():
    user_input = input()
    if len(user_input) == 343 and if_contains_right_c(user_input):
        if is_right(user_input):
            return board_creator(is_right(user_input))
        else:
            print("The board doesn't look legit. Try again:")
            return ready_board()
    elif user_input == "":
        print("Enter 81 numbers of the board (in range '123456789') somehow. If the cell is empty enter '.':")
        return board_out_of_nums()
    print("Something went wrong. Try again:")
    return ready_board()

def app():
    print("If you already have a board (array with arrays (rows) built of 9 elements) paste it here. If you don't have actual board leave this input empty:")
    return ready_board()
    
def find_empty_location(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == ".":
                return i, j
    return None

def is_safe(board, row, col, num):
    if num in board[row]:
        return False

    for i in range(len(board)):
        if board[i][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(board):
    empty_location = find_empty_location(board)
    if not empty_location:
        return True
    row, col = empty_location

    for num in "123456789":
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = "."

    return False

def main():
    i = 0
    while True:
        if i == 0:
            print("THIS IS SUDOKU SOLVER")
            print("Instruction: Just follow the references on each step and there won't be any problems")
        board = app()
        if solve_sudoku(board):
            print("Solution:")
            for row in board:
                print(row)
        else:
            print("No solution exists")
        if_stop = input("Enter '0' if you want to stop programm or whatever you want if you want to continue: ")
        if if_stop == "0":
            return 0
        i = 1

if __name__ == "__main__":
    import sys
    sys.exit(main())