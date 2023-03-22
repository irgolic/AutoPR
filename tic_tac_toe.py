def initialize_board():
    return [[' ' for _ in range(3)] for _ in range(3)]


def print_board(board):
    for row in board:
        print('|'.join(row))
        if row != board[-1]:
            print('-' * 5)


def main():
    board = initialize_board()
    print_board(board)

def get_player_input(player):
    while True:
        try:
            row, col = map(int, input(f"Player {player}, enter your move (row, col): ").split(','))
            if 0 <= row < 3 and 0 <= col < 3:
                return row, col
            else:
                print("Invalid input. Please enter a valid row and column (0-2).")
        except ValueError:
            print("Invalid input. Please enter a valid row and column (0-2).")

def is_board_full(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def game_loop(board):
    players = ['X', 'O']
    current_player = 0

    while not is_board_full(board):
        row, col = get_player_input(players[current_player])
        board[row][col] = players[current_player]
        print_board(board)
        current_player = (current_player + 1) % 2

    print("It's a draw!")

