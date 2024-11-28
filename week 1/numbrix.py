def find_solution(board, x, y, steps_taken):
    if board[x][y] == len(board)**2:
        return board
    og_value = board[x][y]
    board[x][y] = steps_taken
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if is_inbound(board, nx, ny) and (board[nx][ny] == steps_taken+1 or board[nx][ny] == 0):
            solution = find_solution(board, nx, ny, steps_taken+1)
            if solution:
                return solution
    board[x][y] = og_value
    return

def is_inbound(board, x, y):
    return 0 <= x < len(board) and 0 <= y < len(board)

def print_board(board):
    if board == None:
        print("There is no solution.")
    else:
        for row in board:
            line = ""
            for col in row:
                line += '{: <4}'.format(col)
            print(line)

if __name__ == '__main__':
    test_board = [[0,0,0,0,0,0,0,0,81],
                    [0,0,46,45,0,55,74,0,0],
                    [0,38,0,0,43,0,0,78,0],
                    [0,35,0,0,0,0,0,71,0],
                    [0,0,33,0,0,0,59,0,0],
                    [0,17,0,0,0,0,0,67,0],
                    [0,18,0,0,11,0,0,64,0],
                    [0,0,24,21,0,1,2,0,0],
                    [0,0,0,0,0,0,0,0,0]] # Start 7,5
    print_board(test_board + "\n")
    solution = find_solution(board=test_board, x=7, y=5, steps_taken=1)
    print_board(solution)

# tijds complexiteit:
# dfs heeft een tijdscomplexiteit van O(b^D) branchfactor is 4, diepte is N (N = grootte van het bord)
# de nested forloop heeft een tijdscomplexiteit van O(N^2)
# dus 0(4^N) * 0(N^2) = O(4^N * N^2)
# Eigenlijk: Worst case 4^81