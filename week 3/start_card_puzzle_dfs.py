'''Constraints:
    1 every Ace borders a King
    2 every King borders a Queen
    3 every Queen borders a Jack
    4 no Ace borders a Queen
    5 no two of the same cards border each other

'''
import itertools
from copy import deepcopy

# the board has 8 cells, let’s represent the board with a list [0..7]
start_board = ['.'] * 8
cards = ['K', 'K', 'Q', 'Q', 'J', 'J', 'A', 'A']
neighbors = {0:[3], 1:[2], 2:[1,4,3], 3:[0,2,5], 4:[2,5], 5:[3,4,6,7], 6:[5], 7:[5]}

def is_valid(board):
    for i, card in enumerate(board):
        if card != '.':
            current_neighbors = [board[nb] for nb in neighbors[i] if nb != '.']
            if card in current_neighbors:
                return False
            if card == 'K' and ('Q' not in current_neighbors and '.' not in current_neighbors):
                return False
            if card == 'Q' and ('J' not in current_neighbors and '.' not in current_neighbors):
                return False
            if card == 'A' and ('K' not in current_neighbors and '.' not in current_neighbors):
                return False
            if card == 'A' and 'Q' in current_neighbors:
                return False
    return True

def test():
    # is_valid(board) checks all cards, returns False if any card is invalid
    print('f ',is_valid({0: 'J', 1: 'K', 2: 'Q', 3: 'Q', 4: 'J', 5: 'K', 6: 'A', 7: 'A'}))
    print('f ',is_valid({0: 'J', 1: 'J', 2: 'Q', 3: 'Q', 4: 'K', 5: 'K', 6: 'A', 7: 'A'}))
    print('t ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('t ',is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: 'J', 4: 'J', 5: 'A', 6: 'J', 7: 'J'})) # [1]
    print('f ',is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'K', 6: 'J', 7: 'Q'})) # [3]
    print('t ',is_valid({0: '.', 1: 'Q', 2: '.', 3: '.', 4: 'Q', 5: 'J', 6: '.', 7: '.'})) # [3]
    print('f ',is_valid({0: 'Q', 1: '.', 2: '.', 3: 'K', 4: '.', 5: '.', 6: '.', 7: '.'})) # [3]
    print('f ',is_valid({0: '.', 1: 'A', 2: 'Q', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: '.'})) # [4]
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'J', 6: '.', 7: '.'})) # [5]
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: 'Q'})) # [5]
    print('t ',is_valid({0: 'Q', 1: 'Q', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))

def csp(cards, board):
    solutions = []
    iterations = []
    tested = 0
    for permutation in list(itertools.permutations(cards)):
        tested += 1
        test_board = deepcopy(board)
        for i in range(len(test_board)):
            test_board[i] = permutation[i]
        if is_valid(test_board) and test_board not in solutions:
            solutions += [test_board]
            iterations += [tested]
    return solutions, iterations

def solve(cards, board):
    solutions = []
    iterations = []
    count = [0]
    def dfs(cards, board):
        count[0] += 1 # Dit moet als lijst zodat je geen local variable issue krijgt
        if '.' not in board:
            if is_valid(board):
                solutions.append(board) # Append anders krijg je een local variable issue
                iterations.append(count[0])
            return
        idx = board.index('.')
        for i, card in enumerate(cards):
            test_board = deepcopy(board)
            test_board[idx] = card
            remaining_cards = cards[:i] + cards[i+1:] # De kaart die je hebt gelegd moet je uit de kaarten halen
            dfs(remaining_cards, test_board)

    dfs(cards, board)
    return solutions, iterations

def print_board(b):
    return print(f".  .  {b[0]}  .\n{b[1]}  {b[2]}  {b[3]}  .\n.  {b[4]}  {b[5]}  {b[6]}\n.  .  {b[7]}  .")

if __name__ == '__main__':
    # CSP
    solutions, iterations = csp(cards, start_board)
    print_board(solutions[0])
    print(f"CSP 1 ------------- Tested: {iterations[0]}")
    print_board(solutions[1])
    print(f"CSP 2 ------------- Tested: {iterations[1]}")

    # DFS
    solutions, iterations = solve(cards, start_board)
    print_board(solutions[0])
    print(f"DFS 1 ------------- Tested: {iterations[0]}")
    print_board(solutions[1])
    print(f"DFS 2 ------------- Tested: {iterations[1]}")


# Er zijn 8! = 40320 permutaties
# Door te runnen zien we het aantal iteraties
# Er zijn 4 soorten kaarten en deze komen allemaal 2 keer voor, aangezien ze als uniek beschouwt worden kan je elk bord dus 4*4=16 keer tegenkomen.
# Dit zie je ook door CSP te runnen zonder unieke borden op te slaan, dan krijg je i.p.v. 2 borden, 2*16=32 borden terug. Waarvan er dus maar 2 uniek zijn.

"""
Stel 5 is een Aas.
• 3,4,6,7 kunnen geen A zijn vanwege [5]
• 3,4,6,7 kunnen geen V zijn vanwege [4]
• dus 3,4,6,7 moet een K of B zijn
• er zijn maar 2xK en 2xB kaarten, dus 0,1,2 moet een A of V zijn
• dat kan niet want 1 en 2 liggen naast elkaar en kunnen dus niet A en V zijn en ook niet AA of VV.
Ditzelfde verhaal geld ook als 5 een Vrouw is

5 Kan dus alleen nog Boer of Koning zijn.
Stel 5 is een Boer.
• Een V moet aan een B liggen, een K aan een V en een A aan een K.
• De V is dus nodig om een K aan te leggen en moet dus op 3 of 4 gelegd worden.
    • Als we V op 4 leggen moet er een K op 2. Een A moet dan op 1 en 3 want er is geen andere plek waar een K nog kan liggen met ruitme voor een A er aan.
    • Nu kan de tweede K niet naast een V liggen dus dit loopt dood.
    • Als we de V dan op 3 leggen i.p.v. op 4, moet moet er nogsteeds een K op 2 om ruimte voor een A te laten. A moet dan op 1 en 4.
    • Nu kan de tweede K weer niet naast een V liggen
5 Kan dus ook geen Boer zijn.

5 Moet dus wel een K zijn.
Een K kan niet naast een andere K dus de tweede K kan alleen op 0, 1 of 2 gelegd worden.

Stel we leggen de tweede K op 2
• Elke K moet aan een V, maar elke V moet aan een B. V kan dus alleen nog op plek 3 zodat B op 0 kan.
• We moeten nog 2x een V leggen dus 1 plek om deze te leggen is niet genoeg. K kan dus niet op plek 2.

Stel we leggen de tweede K op 1
• Elke K moet aan een V liggen dus er moet een V op 2.
• De andere V moet naast de andere K, maar kan niet naast een V. Dit kan nog op plek 6 of 7.
• In beide gevallen kan er geen B meer aan de tweede V en dus kan K niet op 1.

K moet dus op 5 en op 0 liggen om de puzzel op te lossen.
"""