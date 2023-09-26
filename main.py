import numpy as np

ROWS = 6
COLS = 7


def create_board():
    return np.zeros((ROWS, COLS), dtype=int)


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROWS - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r


def winning_move(board, piece):
    for c in range(COLS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = 1 if piece == 2 else 2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    center_array = [int(i) for i in list(board[:, COLS // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    for c in range(COLS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return winning_move(board, 1) or winning_move(board, 2) or len(get_valid_locations(board)) == 0


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLS):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, 2):
                return None, 100000000000000
            elif winning_move(board, 1):
                return None, -10000000000000
            else:
                return None, 0
        else:
            return None, score_position(board, 2)

    if maximizing_player:
        value = -np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                board_copy = board.copy()
                drop_piece(board_copy, row, col, 2)
                _, new_score = minimax_alpha_beta(board_copy, depth - 1, alpha, beta, False)
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        return column, value

    else:
        value = np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                board_copy = board.copy()
                drop_piece(board_copy, row, col, 1)
                _, new_score = minimax_alpha_beta(board_copy, depth - 1, alpha, beta, True)
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
        return column, value


def print_board(board):
    print("COLUMNAS: \n1 2 3 4 5 6 7\n-------------")
    for r in range(ROWS - 1, -1, -1):
        for c in range(COLS):
            print(board[r][c], end=" ")
        print()
    print()


def play(board, PLAYER_PIECES, AI_PIECES):
    while True:
        game_over = False
        turn = 0

        while not game_over:
            if turn == 0:  # Player 1 input
                col = int(input("Player 1, choose a column (1-7): "))
                col = col - 1

                if col > 6 or col < 0:
                    print("Error: La columna debe estar entre 1-7")
                    return play(board, PLAYER_PIECES, AI_PIECES)

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    PLAYER_PIECES = PLAYER_PIECES - 1

                    if winning_move(board, 1):
                        print("Player 1 wins!")
                        game_over = True
                else:
                    print("Error: La fila ya está llena")
                    return play(board, PLAYER_PIECES, AI_PIECES)
            else:  # AI input
                col, minimax_score = minimax_alpha_beta(board, 4, -np.Inf, np.Inf, True)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    AI_PIECES = AI_PIECES - 1

                    if winning_move(board, 2):
                        print("Player 2 (AI) wins!")
                        game_over = True

                print_board(board)
                print('PLAYER_PIECES: {}'.format(PLAYER_PIECES))
                print('AI_PIECES: {}'.format(AI_PIECES))
                print()
            turn = (turn + 1) % 2
        break


def main():
    PLAYER_PIECES = 21
    AI_PIECES = 21
    board = create_board()
    play(board, PLAYER_PIECES, AI_PIECES)


if __name__ == "__main__":
    main()
