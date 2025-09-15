import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def draw_board(board):
    plt.clf()
    fig, ax = plt.subplots(figsize=(5,5))
    ax.set_xlim(0,3)
    ax.set_ylim(0,3)
    ax.set_xticks([1,2])
    ax.set_yticks([1,2])
    ax.grid(True, which='both', color='black', linewidth=3)

    # Draw X and O
    for r in range(3):
        for c in range(3):
            if board[r][c] == 'X':
                ax.text(c + 0.5, 2.5 - r, 'X', fontsize=40, ha='center', va='center', color='blue')
            elif board[r][c] == 'O':
                ax.text(c + 0.5, 2.5 - r, 'O', fontsize=40, ha='center', va='center', color='red')

    ax.axis('off')
    plt.pause(0.5)

def is_moves_left(board):
    return any(cell == ' ' for row in board for cell in row)

def evaluate(board):
    lines = []
    lines.extend(board)  # rows
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])  # cols
    lines.append([board[i][i] for i in range(3)])  # diagonal
    lines.append([board[i][2-i] for i in range(3)])  # anti-diagonal

    for line in lines:
        if line == ['O', 'O', 'O']:
            return +10
        elif line == ['X', 'X', 'X']:
            return -10
    return 0

def alpha_beta(board, depth, alpha, beta, is_max):
    score = evaluate(board)

    if score == 10 or score == -10:
        return score
    if not is_moves_left(board):
        return 0

    if is_max:
        best = -math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == ' ':
                    board[r][c] = 'O'
                    val = alpha_beta(board, depth+1, alpha, beta, False)
                    board[r][c] = ' '
                    best = max(best, val)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
        return best
    else:
        best = math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == ' ':
                    board[r][c] = 'X'
                    val = alpha_beta(board, depth+1, alpha, beta, True)
                    board[r][c] = ' '
                    best = min(best, val)
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
        return best

def find_best_move(board):
    best_val = -math.inf
    best_move = (-1, -1)

    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                board[r][c] = 'O'
                move_val = alpha_beta(board, 0, -math.inf, math.inf, False)
                board[r][c] = ' '
                if move_val > best_val:
                    best_move = (r, c)
                    best_val = move_val
    return best_move

def main():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    print("Tic-Tac-Toe: You (X) vs Computer (O)")

    plt.ion()  # interactive mode on
    draw_board(board)

    while True:
        # Human move
        while True:
            try:
                inp = input("Enter your move (row col) 0-2 (e.g. '1 2'): ")
                r, c = map(int, inp.split())
                if 0 <= r <= 2 and 0 <= c <= 2 and board[r][c] == ' ':
                    board[r][c] = 'X'
                    break
                else:
                    print("Invalid move! Cell occupied or out of range.")
            except:
                print("Invalid input format. Please enter two numbers separated by space.")

        draw_board(board)

        if evaluate(board) == -10:
            print("You win! Congrats!")
            break
        if not is_moves_left(board):
            print("It's a tie!")
            break

        # Computer move
        print("Computer is thinking...")
        r, c = find_best_move(board)
        board[r][c] = 'O'
        draw_board(board)

        if evaluate(board) == 10:
            print("Computer wins! Better luck next time.")
            break
        if not is_moves_left(board):
            print("It's a tie!")
            break

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()

