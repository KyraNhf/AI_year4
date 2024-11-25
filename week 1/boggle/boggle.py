
test_bord = [['P','I','E','T'],
             ['G','A','A','T'],
             ['A','T','M','S'],
             ['H','U','I','S']]

def make_prefix_dict(file):
    prefixes = dict()
    for word in file.readlines():
        first_char = word[0]
        for i in range(len(word)-1):
            if i==0 and first_char not in prefixes.keys():
                prefixes[first_char] = []
            elif word[0:i] not in prefixes[first_char]:
                prefixes[first_char].append(word[0:i])
    return prefixes

print(make_prefix_dict(open("words_NL.txt")))

def find_words(board):
    for row in board:
        for col in row:
            ...

def find_all_paths(node, path=[], prefixes={}):
    path = path + [node]

    # check for goal state
    if node in prefixes:
        return [path]

    paths = []

    for child in next_states(node):
        if child not in path:
            new_paths = find_all_paths(child, path)
            for new_path in new_paths:
                paths.append(new_path)

    return paths
