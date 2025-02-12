"""

Othello is a turn-based two-player strategy board game.

-----------------------------------------------------------------------------
Board representation

We represent the board as a flat-list of 100 elements, which includes each square on
the board as well as the outside edge. Each consecutive sublist of ten
elements represents a single row, and each list element stores a piece. 
An initial board contains four pieces in the center:

    ? ? ? ? ? ? ? ? ? ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . o @ . . . ?
    ? . . . @ o . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? ? ? ? ? ? ? ? ? ?

The outside edge is marked ?, empty squares are ., black is @, and white is o.

This representation has two useful properties:

1. Square (m,n) can be accessed as `board[mn]`, and m,n means m*10 + n. This avoids conversion
   between square locations and list indexes.
2. Operations involving bounds checking are slightly simpler.
"""
import random
import time

# The black and white pieces represent the two players.
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}
HUMAN, RANDOM, MINIMAX = 0, 1, 2

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
# in total 8 directions.
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

def squares():
    # list all the valid squares on the board.
    # returns a list of valid integers [11, 12, ...]; e.g. 19,20,21 are invalid
    # 11 means first row, first col, because the board size is 10x10
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

def initial_board():
    # create a new board with the initial black and white positions filled
    # returns a list ['?', '?', '?', ..., '?', '?', '?', '.', '.', '.', ...]
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # the middle four squares should hold the initial piece positions.
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board

def print_board(board):
    # get a string representation of the board
    # heading '  1 2 3 4 5 6 7 8\n'
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    # begin,end = 11,19 21,29 31,39 ..
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    print(rep)
    return rep

# -----------------------------------------------------------------------------
# Playing the game

# We need functions to get moves from players, check to make sure that the moves
# are legal, apply the moves to the board, and detect when the game is over.

# Checking moves. A move must be both valid and legal: it must refer to a real square,
# and it must form a bracket with another piece of the same color with pieces of the
# opposite color in between.

def is_valid(move):
    # is move a square on the board?
    # move must be an int, and must refer to a real square
    return isinstance(move, int) and move in squares()

def opponent(player):
    # get player's opponent piece
    return BLACK if player is WHITE else WHITE

def find_bracket(square, player, board, direction):
    # find and return the square that forms a bracket with square for player in the given
    # direction; returns None if no such square exists
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    # if last square board[bracket] not in (EMPTY, OUTER, opp) then it is player
    return None if board[bracket] in (OUTER, EMPTY) else bracket

def is_legal(move, player, board):
    # is this a legal move for the player?
    # move must be an empty square and there has to be a bracket in some direction
    # note: any(iterable) will return True if any element of the iterable is true
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(hasbracket(x) for x in DIRECTIONS)

def make_move(move, player, board):
    # when the player makes a valid move, we need to update the board and flip all the
    # bracketed pieces.
    board[move] = player
    # look for a bracket in any direction
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board

def make_flips(move, player, board, direction):
    # flip pieces in the given direction as a result of the move by player
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    # found a bracket in this direction
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction

# Monitoring players

# define an exception
class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board
    
    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

def legal_moves(player, board):
    # get a list of all legal moves for player
    # legal means: move must be an empty square and there has to be is an occupied line in some direction
    return [sq for sq in squares() if is_legal(sq, player, board)]

def any_legal_move(player, board):
    # can player make any moves?
    return any(is_legal(sq, player, board) for sq in squares())

# Putting it all together. Each round consists of:
# - Get a move from the current player.
# - Apply it to the board.
# - Switch players. If the game is over, get the final score.

def play(black_strategy=HUMAN, white_strategy=HUMAN):
    # play a game of Othello and return the final board and score
    print("Game starts!")
    board = initial_board()
    player = random.choice(('@', 'o'))
    while any_legal_move(player, board):
        print_board(board)
        print(f"{player} to move.")
        if player == '@':
            move = get_move(black_strategy, player, board)
        if player == 'o':
            move = get_move(white_strategy, player, board)
        make_move(move, player, board)
        prev_player = player[:]
        player = next_player(board, player)
    print_board(board)
    player_score = score(prev_player, board)
    opp_score = score(opponent(prev_player), board)
    print("Game ends!")
    print(f"{prev_player} ends the game with {player_score}!\n{opponent(prev_player)} ends the game with {opp_score}!")
    if player_score > opp_score:
        winner = prev_player
    elif opp_score > player_score:
        winner = opponent(prev_player)
    else:
        winner = None
    if winner:
        print(f"The winner is {winner}!")
    else:
        print("It's a tie!")

def next_player(board, prev_player):
    # which player should move next?  Returns None if no legal moves exist
    next_player = opponent(prev_player)
    if any_legal_move(next_player, board):
        return next_player
    elif any_legal_move(prev_player, board):
        return prev_player
    else:
        return None

def get_move(strategy, player, board):
    # call strategy(player, board) to get a move
    if strategy == HUMAN:
        print(f"{player} turn. What is your next move? (0-{len(board)-1})")
        move = int(input())
        while not is_legal(move, player, board):
            print("Cannot play that move!")
            move = int(input())
    if strategy == RANDOM:
        move = random.choice(legal_moves(player, board))
    if strategy == MINIMAX:
        t0 = time.process_time()
        evaluation_move = minimax(board, 5, player, player)
        move = evaluation_move[1]
        t1 = time.process_time()
        print(f"Zet bedacht in {t1 - t0} sec")
    return move

def score(player, board):
    # compute player's score (number of player's pieces minus opponent's)
    score = 0
    for i in range(len(board)):
        if board[i] == player:
            score += 1
    return score

def minimax(board, depth, player, maxi_player, alpha=float('-inf'), beta=float('inf')):
    # Als we ver genoeg hebben gekeken of als er geen zetten meer zijn
    if depth == 0 or not any_legal_move(player, board):
        return evaluate_board(maxi_player, board), None
    
    best_move = None
    if player == maxi_player:
        max_evaluation = float('-inf') # Heel laag want dat wordt overtroffen door elke zet
        for move in legal_moves(player, board):
            board_copy = board[:]
            make_move(move, player, board_copy)
            evaluation_move = minimax(board_copy, depth - 1, opponent(player), maxi_player, alpha, beta)
            evaluation = evaluation_move[0]
            if evaluation > max_evaluation:
                max_evaluation = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_evaluation, best_move
    else:
        min_evaluation = float('inf') # Heel hoog want dat wordt onderdaan door elke zet
        for move in legal_moves(player, board):
            board_copy = board[:]
            make_move(move, player, board_copy)
            evaluation_move = minimax(board_copy, depth - 1, opponent(player), maxi_player, alpha, beta)
            evaluation = evaluation_move[0]
            if evaluation < min_evaluation:
                min_evaluation = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_evaluation, best_move

def evaluate_board(player, board):
    # Bekijk de score voor beide spelers
    player_score = score(player, board)
    opp_score = score(opponent(player), board)
    # Geef hoeken een hoge score
    corners = [11, 18, 81, 88]
    corner_score = 0
    for corner in corners:
        if board[corner] == player:
            corner_score += 10
        if board[corner] == opponent(player):
            corner_score -= 10
    # Jouw mogelijke moves - het aantal moves dat de tegenstander kan maken
    move_count = len(legal_moves(player, board)) - len(legal_moves(opponent(player), board))
    return player_score - opp_score + corner_score + move_count

# Play strategies (HUMAN, RANDOM, MINIMAX)
play(MINIMAX, MINIMAX)

# Het tellen van stenen alleen is geen goede strategie omdat je dan geen rekening houdt met de toekomst en omdat niet alle plekken even goed zijn, hoeken zijn bijvoorbeeld veel waard.
# Om beter te evalueren is het wijs om hoeken een grotere waarde te geven, en om mee te nemen hoeveel zetten beide spelers kunnen doen na een gemaakte zet. De tegenstander in het nauw werken is een goede strategie!

# Als je binnen twee seconden wilt blijven zonder pruning is een diepte van 3, op Matthias zijn desktop, maximaal, zetten lopen bij diepte 4 van 0 tot 2.5 seconden.
# Met pruning is de maximale diepte om onder 2 seconden te blijven 5 (Laptop: loopt op tot 3.6 sec). Dat is dus al een stuk beter. Wel zie je dat bij een diepte van 6 de zetten wel tot 10 seconden op kunnen lopen!

# Als je nog een betere performance wil bereieken zou je een minimale threshhold voor socre aan een mogelijke zet kunnen stellen. Als deze threshold niet geraakt wordt bekijk je die tak niet.
# Echter kan je dan goede zetten gaan missen, en doet pruning al iets vergelijkbaars.
# Wat ook zou kunnen is dat je een tijdslimiet meenemeen in het algoritme. Je kunt dan beginnen met een standaard diepte, en als er genoeg tijd is ga je bij elke tak nog een laag dieper, totdat de tijp te krap is.