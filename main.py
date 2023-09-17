def check_connect_four(board):
    # Check horizontally
    for row in board:
        for col in range(4):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] == 'X':
                return "X"
            elif row[col] == row[col + 1] == row[col + 2] == row[col + 3] == 'Y':
                return "Y"

    # Check vertically
    for col in range(7):
        for row in range(3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == 'X':
                return "X"
            elif board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == 'Y':
                return "Y"

    # Check diagonally (bottom-left to top-right)
    for row in range(3, 6):
        for col in range(4):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == 'X':
                return "X"
            elif board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == 'Y':
                return "Y"

    # Check diagonally (top-left to bottom-right)
    for row in range(3):
        for col in range(4):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == 'X':
                return "X"
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == 'Y':
                return "Y"

    return None  # No winner found


# HAY QUE MANDARLE UNA X O UNA Y
board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]


def main():
    if check_connect_four(board) == "X":
        print("Player X wins!")
    elif check_connect_four(board) == "Y":
        print("Player Y wins!")
    else:
        print("Nobody won")


if __name__ == '__main__':
    main()
