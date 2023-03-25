def display_board(board):
    for i in range(3):
        print(" | ".join(board[i * 3:i * 3 + 3]))
        if i < 2:
            print("-" * 9)


if __name__ == "__main__":
    example_board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    display_board(example_board)
