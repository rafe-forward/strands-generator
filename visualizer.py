import matplotlib.pyplot as plt
board = [
    ['S', 'T', 'R', 'A', 'N', 'D'],
    ['E', 'G', 'A', 'M', 'E', 'S'],
    ['L', 'O', 'W', 'Q', 'B', 'R'],
    ['K', 'T', 'I', 'U', 'X', 'O'],
    ['V', 'H', 'Z', 'P', 'Y', 'C'],
    ['N', 'F', 'J', 'D', 'L', 'M'],
    ['A', 'S', 'U', 'T', 'O', 'K'],
    ['R', 'E', 'C', 'A', 'P', 'S']
]


def draw_board(board):
    rows, cols = len(board), len(board[0])
    fig, ax = plt.subplots()
    ax.set_xticks(range(cols))
    ax.set_yticks(range(rows))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.invert_yaxis()
    
    for i in range(rows):
        for j in range(cols):
            ax.text(j, i, board[i][j], ha='center', va='center', fontsize=16,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    
    plt.grid(True)
    plt.show()