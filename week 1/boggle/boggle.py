def load_file(file):
    prefixes = set()
    words = set()
    with open(file) as f:
        for word in f.readlines():
            word = word.strip().upper()
            words.add(word)
            for i in range(1, len(word)):
                prefixes.add(word[:i])
    return words, prefixes

def is_valid_move(x, y, n, visited):
    return (x, y) not in visited and 0 <= x < n and 0 <= y < n

def find_all_words(board, n, words, prefixes):
    def dfs(x, y, path=[], visited=set()):
        word = ''.join(path)
        if word in words:
            found_words.add(word)

        if word not in prefixes:
            return

        visited.add((x, y))
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = (x + dx) % n, (y + dy) % n
            if is_valid_move(nx, ny, n, visited):
                dfs(nx, ny, path + [board[nx][ny]], visited)
        visited.remove((x, y))

    found_words = set()
    visited = set()
    for i in range(n):
        for j in range(n):
            dfs(i, j, [board[i][j]], visited)
    return found_words

if __name__ == '__main__':
    words, prefixes = load_file("words_NL.txt")
    test_board = [['P', 'I', 'E', 'T'],
                ['G', 'A', 'A', 'T'],
                ['A', 'T', 'M', 'S'],
                ['H', 'U', 'I', 'S']]
    N = len(test_board)
    found_words = find_all_words(test_board, N, words, prefixes)

    print("\nGevonden woorden:")
    for word in sorted(found_words):
        print(word)

# tijds complexiteit:
