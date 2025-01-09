import numpy as np

# place triominoes in matrix 3 rows x 4 cols

NR_OF_COLS = 16 # 4 triominoes HB VB L RL + 12 cells
NR_OF_ROWS = 22 # 6*HB 4*VB 6*L 6*RL

triominoes = [np.array(piece) for piece in [
        # horizontal bar (HB)
        [[1,1,1]],
        # vertical bar (VB)
        [[1],[1],[1]],
        # normal L (L)
        [[1,0], [1,1]],
        # rotated L (RL)
        [[1,1], [0,1]]
    ]
]

def make_matrix(triominoes):

    # create and return matrix as input for alg-x
    # matrix has 22 rows x 16 cols
    # and has the following cols: HB VB L RL (0,0) (0,1) (0,2) (0,3) (1,0) .... (3,3)

    def all_positions(triominoes):
        # find all positions to place triomino T in matrix M (3 rows x 4 cols)
        rows, cols = triominoes.shape
        for i in range(3+1 - rows):
            for j in range(4+1 - cols):
                M = np.zeros((3, 4), dtype='int')
                # place T in M
                M[i:i+rows, j:j+cols] = triominoes
                yield M

    rows = []
    for i, P in enumerate(triominoes):
        # i points to the 4 triominoes HB VB L RL
        for A in all_positions(P):
            # add 4 zeros to each row
            A = np.append(np.zeros(4, dtype='int'), A)
            A[i] = 1
            rows.append(list(A))
    return rows


def prepare(mx):
    # note that when applying alg-x we're only interested in 1's
    # so we add 2 lists that define where the 1's are
    rows = mx    
    # note that zip(*b) is the transpose of b
    cols = [list(i) for i in zip(*rows)]

    print(np.array(rows))
    print()

    def find_ones(rows):
        # returns indexes in rows where the ones are
        # example: [[0, 3], [1, 3], [1, 2], [2]]
        lv_row_has_1_at = []
        for row in rows:
            x = []
            for i in range(len(row)):
                if row[i] == 1:
                    x.append(i)
            lv_row_has_1_at.append(x.copy())
        return lv_row_has_1_at

    row_has_1_at = find_ones(rows) # read-only list; example: [[0, 3], [1, 3], [1, 2], [2]]
    col_has_1_at = find_ones(cols) # read-only list; example: [[0], [1, 2], [2, 3], [0, 1]]

    # if there's a col without ones, then there is no exact cover possible
    halt_fl = False
    for l in col_has_1_at:
        if l == []:
            print("No solution possible!")
            halt_fl = True

    row_valid = NR_OF_ROWS * [1]
    col_valid = NR_OF_COLS * [1]

    return halt_fl, row_valid, col_valid, row_has_1_at, col_has_1_at

def cover(r, row_valid, col_valid, row_has_1_at, col_has_1_at):
    # given a row r:
    #   cover all cols that have a 1 in row r
    #   cover all rows r' that intersect/overlap with row r
    # returns row_valid, col_valid

    # cover row r
    row_valid[r] = 0

    # bijhouden welke rows gecoverd zijn:
    rows_covered = []

    for col in row_has_1_at[r]:
        if col_valid[col]:
            # cover alle collumns die overlap hebben met row r
            col_valid[col] = 0
            for row in col_has_1_at[col]:
                if row_valid[row]:
                    # cover alle rows die overlap hebben met col
                    rows_covered.append(row)
                    row_valid[row] = 0
    return row_valid, col_valid, rows_covered

def uncover(r, row_valid, col_valid, row_has_1_at, col_has_1_at, rows_covered):
    # given a row r:
    #   uncover all cols that have a 1 in row r
    #   uncover all rows r' that intersect/overlap with row r
    # returns row_valid, col_valid

    for row in rows_covered:
        row_valid[row] = 1

    for col in row_has_1_at[r]:
        col_valid[col] = 1

    row_valid[r] = 1
    return row_valid, col_valid

def print_solution(solution, row_has_1_at):
    # place triominoes in matrix D 3 rows x 4 cols
    D = [[0 for i in range(4)] for j in range(3)]

    for row_number in solution:
        #print(row_number) # 1 6 14 21
        row_list = row_has_1_at[row_number]
        #print(row_list)   # 0 5 6 7
        idx = row_list[0]
        assert idx in [0,1,2,3]
        symbol = ['HB','VB','L ','RL'][idx]
        for c in row_list[1:]: # skip first one
            rownr = c//4-1
            colnr = c%4
            D[rownr][colnr] = symbol
    print('------------------------')

    for i in D:
        print(i)

def solve(row_valid, col_valid, row_has_1_at, col_has_1_at, solution, all_solutions):
    # using Algoritm X, find all solutions (= set of rows) given valid/uncovered rows and cols
    # base case: er zijn geen columns meer over, er is een exacte cover
    if all(col==0 for col in col_valid):
        print("solution found!")
        print_solution(solution, row_has_1_at)
        all_solutions.append(solution.copy())
        return False # doorzoeken naar meer oplossingen

    # selecteer col met minste ones
    min_col = None
    min_count = max(len(col) for col in col_has_1_at)
    for i in range(len(col_valid)):
        if col_valid[i]:
            count = len(col_has_1_at[i])
            if count < min_count:
                min_count = count
                min_col = i
    # als er geen columns meer over zijn: backtrack
    if min_col is None:
        return False

    # selecteerd de rows die gecoverd moeten worden
    rows_to_cover = col_has_1_at[min_col]

    for row in rows_to_cover:
        if row_valid[row]:
            # voeg row aan de solution toe
            solution.append(row)

            # Cover deze row en alle kruisende collumns en de rows die overlappen met deze row

            row_valid, col_valid, rows_covered = cover(row, row_valid, col_valid, row_has_1_at, col_has_1_at)

            if solve(row_valid, col_valid, row_has_1_at, col_has_1_at, solution, all_solutions):
                pass

            # Backtrack als er geen oplossing is gevonden
            row_valid, col_valid = uncover(row, row_valid, col_valid, row_has_1_at, col_has_1_at, rows_covered)
            solution.pop()
    return False




if __name__ == '__main__':
    mx = make_matrix(triominoes)
    halt_fl, row_valid, col_valid, row_has_1_at, col_has_1_at = prepare(mx)
    if not halt_fl:
        print("solving")
        all_solutions = []
        solve(row_valid, col_valid, row_has_1_at, col_has_1_at, [], all_solutions)
        if not all_solutions :
            print("no solution found!")
        else:
            print(f"solutions found: {len(all_solutions)}")

# er zijn 4 oplossingen