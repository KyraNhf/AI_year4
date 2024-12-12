# kruiswoord puzzel
from collections import Counter


def make_domain():
    # domain is a dict key:value where key 1..11 and value is a set of words with correct length
    domain = dict()
    word_lengths = {1:4, 2:11, 3:5, 4:5, 5:6, 6:5, 7:5, 8:4, 9:5, 10:6, 11:7}
    with open("words_NL.txt") as f:
        for word in f.readlines():
            word = word.strip().upper()
            length_word = len(word)
            for key, value in word_lengths.items():
                if value == length_word:
                    if key not in domain.keys():
                        domain[key] = {word}
                    else:
                        domain[key].add(word)
    return domain

def valid(candidate, a, word_x):
    # candidate = word or variable like 3, 6, 9, 10 that we will test
    # a is a dict key:value, where key is like 3, 6, 9, 10 and value is a word (can be None)
    # word_x is a list of tuples defining all crossings
    if a[candidate] is None:
        return True
    for i in word_x:
        var = i[0]
        p1 = i[1]
        var2 = i[2]
        p2 = i[3]
        if var == candidate:
            if var2 in a.keys():
                if a[var2] is not None:
                    if a[candidate][p1] != a[var2][p2]:
                        return False

    return True

def solve(domain, assigned, unassigned_vars, word_x, other_half):
    if all(valid(k, assigned, word_x) for k in assigned.keys()):
        if all(v is not None for v in assigned.values()):
            print(assigned)
            return True
        key = unassigned_vars[0]
        for i in domain[key]:
            if i not in assigned.values() and i not in other_half.values():
                assigned[key] = i
                if solve(domain, assigned, unassigned_vars[1:], word_x, other_half):

                    return True
                assigned[key] = None
        return False

if __name__ == '__main__':
    # (w1,i,w2,j) means word w1 index i crosses word w2 index j (i,j starting from 0)
    word_x_left = [(3, 2, 9, 0), (3, 4, 10, 0), (9, 3, 6, 1), (10, 3, 6, 3)]
    word_x_right = [(1, 1, 2, 6), (1, 3, 4, 4), (4, 3, 5, 0), (5, 4, 11, 0), (7, 3, 11, 3), (8, 3, 11, 6)]
    d = make_domain()
    assigned_left = {3:None, 6:None, 9:None, 10:None}
    assigned_right = {1:None, 2:None, 4:None, 5:None, 7:None, 8:None, 11:None}
    unassigned_vars_left = [3,6,9,10]
    unassigned_vars_right = [1,2,4,5,7,8,11]
    solve(d, assigned_left, unassigned_vars_left, word_x_left, assigned_right)
    solve(d, assigned_right, unassigned_vars_right, word_x_right, assigned_left)


# your code

# vragen:
# 1:
# a:    variabelen zijn het aantal woorden die in het kruiswoord puzzel geplaatst moeten worden in dit geval 11
# b:    domein is het aantal woorden die op de plek van variabele past
# c:    de variabelen kan je het beste representeren in een dictonary die per variabele een lijst bevat met de passende woorden (het domein erachter)
#       bijvoorbeeld {1:[woord1, woord2 .. etc], 2:[woord3, woord4 .. etc]}
# d:    beginnen met het kijken naar het woord met de meeste kruisingen en of de kruisingen overeen komen

# 2:
# a:    de binary constraints zijn het aantal kruisingen, in dit geval 10
# b:    als we bijvoorbeeld naar woord 1 kijken, weten we dat er een kruising is op 1[1] met woord 2 op 2[6]
#       in code kunnen we dat representeren als:
        # 1[1] == 2[7]: return true
# c:    arc-consistency kan gebruikt worden om het gekozen woord voor de variabele uit de domeinen van de andere variabelen met dezelfde lengte te halen,
#       en om woorden uit de andere domeinen te halen die niet valid zijn met het gekozen woord

# 3:    Het is zeker wel mogelijk om alle oplossingen te vinden, het kan alleen lang duren
