import numpy as np


class ConnectFour:
    def __init__(self):
        self.ROWS = 6
        self.COLS = 7
        self.board = self.create_board()
        self.AI_PIECES = 21
        self.PLAYER_PIECES = 21

    def create_board(self):
        return np.zeros((self.ROWS, self.COLS), dtype=int)

    def drop_piece(self, board_copy, row, col, piece):
        board_copy[row][col] = piece

    def is_valid_location(self, col):
        return self.board[self.ROWS - 1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.ROWS):
            if self.board[r][col] == 0:
                return r

    def winning_move(self, piece):
        for c in range(self.COLS - 3):
            for r in range(self.ROWS):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece and self.board[r][c + 3] == piece:
                    return True

        for c in range(self.COLS):
            for r in range(self.ROWS - 3):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece and self.board[r + 3][c] == piece:
                    return True

        for c in range(self.COLS - 3):
            for r in range(self.ROWS - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][c + 2] == piece and self.board[r + 3][c + 3] == piece:
                    return True

        for c in range(self.COLS - 3):
            for r in range(3, self.ROWS):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][c + 2] == piece and self.board[r - 3][c + 3] == piece:
                    return True

    def evaluate_window(self, window, piece):
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

    def score_position(self, piece):
        score = 0

        center_array = [int(i) for i in list(self.board[:, self.COLS // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        for r in range(self.ROWS):
            row_array = [int(i) for i in list(self.board[r, :])]
            for c in range(self.COLS - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)

        for c in range(self.COLS):
            col_array = [int(i) for i in list(self.board[:, c])]
            for r in range(self.ROWS - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, piece)

        for r in range(self.ROWS - 3):
            for c in range(self.COLS - 3):
                window = [self.board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        for r in range(self.ROWS - 3):
            for c in range(self.COLS - 3):
                window = [self.board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    def is_terminal_node(self):
        return self.winning_move(1) or self.winning_move(2) or len(self.get_valid_locations()) == 0

    def get_valid_locations(self):
        valid_locations = []
        for col in range(self.COLS):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def minimax_alpha_beta(self, depth, alpha, beta, maximizing_player):
        valid_locations = self.get_valid_locations()
        is_terminal = self.is_terminal_node()

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(2):
                    return None, 100000000000000
                elif self.winning_move(1):
                    return None, -10000000000000
                else:
                    return None, 0
            else:
                return None, self.score_position(2)

        if maximizing_player:
            value = -np.Inf
            column = np.random.choice(valid_locations)
            for col in valid_locations:
                if self.is_valid_location(col):
                    row = self.get_next_open_row(col)
                    board_copy = self.board.copy()
                    self.drop_piece(board_copy, row, col, 2)
                    _, new_score = self.minimax_alpha_beta(depth - 1, alpha, beta, False)
                    if new_score > value:
                        value = new_score
                        column = col
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return column, value
        else:  # Minimizing player
            value = np.Inf
            column = np.random.choice(valid_locations)
            for col in valid_locations:
                if self.is_valid_location(col):
                    row = self.get_next_open_row(col)
                    board_copy = self.board.copy()
                    self.drop_piece(board_copy, row, col, 1)
                    _, new_score = self.minimax_alpha_beta(depth - 1, alpha, beta, True)
                    if new_score < value:
                        value = new_score
                        column = col
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
            return column, value

    def print_board(self):
        print("COLUMNS: \n1 2 3 4 5 6 7\n-------------")
        for r in range(self.ROWS - 1, -1, -1):
            for c in range(self.COLS):
                print(self.board[r][c], end=" ")
            print()
        print()

    def play(self):
        while True:
            game_over = False
            turn = 0  # Player 1 starts

            while not game_over:
                # Player 1 input
                if turn == 0:
                    col = int(input("Player 1, choose a column (1-7): "))
                    col = col - 1

                    if col > 6 or col < 0:
                        print("Error: La columna debe estar entre 1-7")
                        return self.play()

                    if self.is_valid_location(col):
                        row = self.get_next_open_row(col)
                        self.drop_piece(self.board, row, col, 1)
                        self.PLAYER_PIECES = self.PLAYER_PIECES - 1

                        if self.winning_move(1):
                            print("Player 1 wins!")
                            game_over = True
                    else:
                        print("Error: La fila ya está llena")
                        return self.play()
                else:
                    col, minimax_score = self.minimax_alpha_beta(4, -np.Inf, np.Inf, True)
                    if self.is_valid_location(col):
                        row = self.get_next_open_row(col)
                        self.drop_piece(self.board, row, col, 2)
                        self.AI_PIECES = self.AI_PIECES - 1

                        if self.winning_move(2):
                            print("Player 2 (AI) wins!")
                            game_over = True

                    self.print_board()
                    print('PLAYER_PIECES: {}'.format(self.PLAYER_PIECES))
                    print('AI_PIECES: {}'.format(self.AI_PIECES))
                    print()
                turn = (turn + 1) % 2
            break


def main():
    game = ConnectFour()
    game.play()


if __name__ == "__main__":
    main()
