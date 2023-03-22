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


