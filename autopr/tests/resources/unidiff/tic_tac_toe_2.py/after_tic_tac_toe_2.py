def display_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)


def check_winner(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True

    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True

    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True

    return False


def alternate_player(player):
    return "X" if player == "O" else "O"

def is_board_full(board):
    for row in board:
        if " " in row:
            return False
    return True



if __name__ == "__main__":
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    display_board(board)

    while not check_winner(board, current_player) and not is_board_full(board):
        row, col = map(int, input("Enter your move (row, col): ").split(","))
        board[row-1][col-1] = current_player
        display_board(board)
        current_player = alternate_player(current_player)

    print("Game Over!")
