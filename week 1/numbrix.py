def is_valid_move(board, x, y, visited, steps_taken):
    return (x, y) not in visited and 0 <= x < len(board) and 0 <= y < len(board) and (board[x][y] == 0 or board[x][y] == steps_taken)

def find_path(board, path, x, y, visited, steps_taken):
    if board[x][y] == len(test_board)**2:
        return path

    visited.add((x, y))
    steps_taken += 1
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx = dx+x
        ny = dy+y
        if is_valid_move(board, nx, ny, visited, steps_taken):
            find_path(board, path+[board[nx][ny]], nx, ny, visited, steps_taken)
    visited.remove((x, y))

if __name__ == '__main__':
    test_board = [[0,0,0,0,0,0,0,0,81],
                  [0,0,46,45,0,55,74,0,0],
                  [0,38,0,0,43,0,0,78,0],
                  [0,35,0,0,0,0,0,71,0],
                  [0,0,33,0,0,0,59,0,0],
                  [0,17,0,0,0,0,0,67,0],
                  [0,18,0,0,11,0,0,64,0],
                  [0,0,24,21,0,1,2,0,0],
                  [0,0,0,0,0,0,0,0,0]]
    visited = set()
    path = find_path(board=test_board, path=[], x=7, y=5, visited=visited, steps_taken=1)
    print(path)