# kruiswoord puzzel

def make_domain():
    # domain is a dict key:value where key 1..11 and value is a set of words with correct length
    domain = dict()
    word_lengths = {1:4, 2:11, 3:5, 4:5, 5:6, 6:5, 7:5, 8:4, 9:5, 10:6, 11:7}

    # your code

    return domain

def valid(candidate, a, word_x):
    # candidate = word or variable like 3, 6, 9, 10 that we will test
    # a is a dict key:value, where key is like 3, 6, 9, 10 and value is a word (can be None)
    # word_x is a list of tuples defining all crossings

    pass

def solve(domain, assigned, unassigned_vars, word_x):

    pass

#(w1,i,w2,j) means word w1 index i crosses word w2 index j (i,j starting from 0)
word_x_left = [(3, 2, 9, 0), (3, 4, 10, 0), (9, 3, 6, 1), (10, 3, 6, 3)]
word_x_right = [(1, 1, 2, 6), (1, 3, 4, 4), (4, 3, 5, 0), (5, 4, 11, 0), (7, 3, 11, 3), (8, 3, 11, 6)]

# your code