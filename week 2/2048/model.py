import random
import itertools
import math
import copy

MAX_DEPTH = 6
CHANCE = 1
MAX = 2

def merge_left(b):
    # merge the board left
    # this is the function that is reused in the other merges
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    def merge(row, acc):
        # recursive helper for merge_left

        # if len row == 0, return accumulator
        if not row:
            return acc

        x = row[0]
        # if len(row) == 1, add element to accumulator
        if len(row) == 1:
            return acc + [x]

        # if len(row) >= 2
        if x == row[1]:
            # add row[0] + row[1] to accumulator, continue with row[2:]
            return merge(row[2:], acc + [2 * x])
        else:
            # add row[0] to accumulator, continue with row[1:]
            return merge(row[1:], acc + [x])

    new_b = []
    for row in b:
        # merge row, skip the [0]'s
        merged = merge([x for x in row if x != 0], [])
        # shift left: add zeros to the right if necessary
        merged = merged + [0] * (len(row) - len(merged))
        new_b.append(merged)
    # return [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    return new_b

def merge_right(b):
    # merge the board right
    # strategy: is like merge_left with all rows reversed
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    def reverse(x):
        return list(reversed(x))

    rev = [reverse(x) for x in b]
    ml = merge_left(rev)
    # return [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    return [reverse(x) for x in ml]


def merge_up(b):
    # merge the board upward
    # note that zip(*b) is the transpose of b
    trans = merge_left(zip(*b))
    return [list(x) for x in zip(*trans)]


def merge_down(b):
    # merge the board downward
    # note that zip(*b) is the transpose of b
    trans = merge_right(zip(*b))
    return [list(x) for x in zip(*trans)]


# translate directions to functions
MERGE_FUNCTIONS = {
    'L': merge_left,
    'R': merge_right,
    'U': merge_up,
    'D': merge_down
}

def give_moves(b):
    # a move is legal if (1) at least one tile can be shifted to an empty place or
    # (2) if two adjacent tiles have the same value != 0
    # return all possible moves for board b as a list with values L, R, U, D
    # if no move is possible an empty list is returned

    # note: in the original js-code the strategy is: try to do a move, only if move was possible
    # then add random tiles: if (moved) {this.addRandomTile(); ...}. Here we could call all four
    # merge-functions and then check, but this no so good performance-wise

    def inner(b, left, right):
        rlis = []
        flag = False
        for row in b:
            # special case where row contains only zeros
            if not all(val == 0 for val in row):
                # evaluate all pairs of adjacent tiles
                for x, y in zip(row[:-1], row[1:]):
                    # check if they are equal
                    if x == y and x != 0:
                        rlis = [left, right]
                        flag = True # no need to continue
                        break
                    # check first if shift left is possible
                    if x == 0 and y != 0:
                        rlis.append(left) if left not in rlis else rlis
                    # then check if shift right is possible
                    if x != 0 and y == 0:
                        rlis.append(right) if right not in rlis else rlis
            if flag:
                break

        return rlis

    res1 = inner(b, 'L', 'R')
    # check columns: zip(*b) is the transpose of b
    trans = [list(x) for x in zip(*b)]
    res2 = inner(trans, 'U', 'D')

    return res1 + res2

def start():
    # make initial board
    b = [[0] * 4 for _ in range(4)]
    add_two_four(b)
    add_two_four(b)
    return b


def play_move(b, direction):
    # get merge function and apply it to board
    b = MERGE_FUNCTIONS[direction](b)
    add_two_four(b)
    return b


def add_two_four(b):
    # add a random tile to the board at open position.
    # chance of placing a 2 is 90%; chance of 4 is 10%
    rows, cols = list(range(4)), list(range(4))
    random.shuffle(rows)
    random.shuffle(cols)
    distribution = [2] * 9 + [4]
    for i, j in itertools.product(rows, cols):
        if b[i][j] == 0:
            b[i][j] = random.sample(distribution, 1)[0]
            return (b)
        else:
            continue

def test():
    b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    assert merge_left(b) == [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    assert merge_right(b) == [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    assert merge_up(b) == [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert merge_down(b) == [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    b = [[2, 8, 4, 0], [16, 0, 0, 0], [2, 0, 2, 0], [2, 0, 0, 0]]
    assert (merge_left(b)) == [[2, 8, 4, 0], [16, 0, 0, 0], [4, 0, 0, 0], [2, 0, 0, 0]]
    assert (merge_right(b)) == [[0, 2, 8, 4], [0, 0, 0, 16], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert (merge_up(b)) == [[2, 8, 4, 0], [16, 0, 2, 0], [4, 0, 0, 0], [0, 0, 0, 0]]
    assert (merge_down(b)) == [[0, 0, 0, 0], [2, 0, 0, 0], [16, 0, 4, 0], [4, 8, 2, 0]]

    b = [[0, 1, 2, 3], [0, 4, 5, 6], [0, 1, 2, 3], [0, 4, 5, 6]]
    assert (give_moves(b)) == ['L']
    b = [[0, 0, 0, 0], [1, 2, 3, 4], [5, 6, 7, 8], [1, 2, 3, 4]]
    assert (give_moves(b)) == ['U']
    b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    assert (give_moves(b)) == ['L','R','U','D']
    b = [[2, 8, 4, 2], [16, 0, 0, 0], [2, 4, 2, 8], [8, 0, 0, 0]]
    assert give_moves(b) == ['R','D','U']
    b = [[32, 64, 2, 16], [8, 32, 8, 2], [4, 16, 8, 4], [2, 8, 4, 2]]
    assert (give_moves(b)) == ['U','D']

    # no left
    b = [[4, 0, 0, 0], [8, 2, 0, 0], [8, 4, 0, 0], [8, 16, 2, 0]]
    assert (give_moves(b)) == ['R','U','D']
    # no right
    b = [[2, 4, 2, 16], [0, 0, 16, 8], [0, 8, 16, 2], [0, 0, 4, 2]]
    assert (give_moves(b)) == ['L','U','D']
    # no up
    b = [[4, 4, 4, 8], [0, 2, 2, 4], [0, 0, 0, 16], [0, 0, 0, 0]]
    assert (give_moves(b)) == ['L','R','D']
    # no down
    b = [[0, 0, 0, 2], [0, 0, 2, 16], [0, 4, 32, 8], [4, 8, 4, 4]]
    assert (give_moves(b)) == ['L','R','U']

    #for i in range(11):
    #    add_two_four(b)
    #    print(b)

def get_random_move():
    return random.choice(list(MERGE_FUNCTIONS.keys()))

MIN_INF = -999999999

def get_expectimax_move(b):
    depth = 5
    best_value = MIN_INF
    moves = give_moves(b)
    best_move = moves[0]
    for move in moves:
        b_copy = copy.deepcopy(b)
        b_copy = MERGE_FUNCTIONS[move](b_copy)
        value, new_move = expectimax(b_copy, CHANCE, depth, move)
        if value > best_value:
            best_value = value
            best_move = new_move
    return best_move

def expectimax(b, player, depth, old_move):
    best_move = old_move
    moves = give_moves(b)
    if len(moves) == 0:
        return MIN_INF, best_move
    if depth == 0:
        return heuristic(b), best_move

    if player == MAX:
        best_value = MIN_INF
        for move in moves:
            b_copy = copy.deepcopy(b)
            b_copy = MERGE_FUNCTIONS[move](b_copy)
            value = expectimax(b_copy, CHANCE, depth-1, move)[0]
            if value > best_value:
                best_value = value
                best_move = move
    else:
        best_value = 0
        cells = get_empty_cells(b)
        for cell in cells:
            for value in [2, 4]:
                board_copy = copy.deepcopy(b)
                board_copy[cell[0]][cell[1]] = value
                best_value += (
                        (0.9 if value == 2 else 0.1)
                        * (1 / len(cells))
                        * expectimax(board_copy, MAX, depth - 1, best_move)[0]
                )
    return best_value, best_move

def get_empty_cells(b):
    empty_cells = []
    for row in range(len(b)):
        for col in range(len(b[row])):
            if b[row][col] == 0:
                empty_cells.append((row, col))
    return empty_cells

def heuristic(b):
    score = 0
    max_tile = max(max(row) for row in b)
    for i in range(len(b)):
        for j in range(len(b)):
            score += b[i][j] * perfect_heuristic[i][j]

            cell_value = b[i][j]
            # more empty cells is better
            if cell_value == 0:
                score += 4096
            else:
                # check postion of highest number
                if cell_value == max_tile:
                    if i==0 and j==0: # highest nr in left corner
                        score += 4096
                #  check if high value cell is on left side of board
                if cell_value >= 8:
                    if i < (len(b) - 1) / 2:
                        score += 1000
                # check if surrounding cells have same value
                if b[i][j] == b[i][j - 1]:
                    score += 250
                if b[i][j] == b[i-1][j]:
                    score += 250
                if i < len(b)-1:
                    if b[i][j] == b[i+1][j]:
                        score += 250
                if j < len(b)-1:
                    if b[i][j] == b[i][j+1]:
                        score += 250
    return score

perfect_heuristic = [
    [2**16, 2**15, 2**14, 2**13],
    [2**9, 2**10, 2**11,  2**12],
    [2**8, 2**7, 2**6,  2**5],
    [2**1, 2**2, 2**3,  2**4]
]

"""
De maximale diepte waarbij het programma nog een acceptabele performance heeft is 5. 
In de beginfase duurt het lang voordat de AI een keuze heeft gemaakt, maar de AI bereikt wel 2048. 
Met diepte 4 bereikt de AI geen 2048, maar is wel een heel stuk sneller

de performance wordt nu vooral door de deepcopy's van het bord verslechterd, omdat hierdoor de snelheid aanzienlijk trager wordt
Daarnaast kan de heuristic nog verbeterd kunnen worden door te kijken naar hoe het bord gestructureerd is. 
De smoothness van het bord kan dan nog meegenomen worden: https://azaky.github.io/2048-AI/paper.pdf
Ook kan er nog gekeken worden naar de afstand van hoge getallen tot de border. Grote getallen die zich in het midden van het bord bevinden
moeten zwaarder gestraft worden dan kleine getallen in het midden van het bord.
"""
# test()
