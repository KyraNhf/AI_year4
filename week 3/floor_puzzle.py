import itertools

def test(L,M,N,E,J):
    if E <= M:
        return False
    if N == 1 or N == 5:
        return False
    if J == N+1 or J == N-1:
        return False
    if N == M+1 or N == M-1:
        return False
    if L == 5:
        return False
    if M == 1:
        return False
    return True

def csp(floors):
    for (L, M, N, E, J) in list(itertools.permutations(floors)):
        if test(L, M, N, E, J):
            return (L, M, N, E, J)

if __name__ == '__main__':
    floors = [1, 2, 3, 4, 5]
    (L, M, N, E, J) = csp(floors)
    print(f"Loes: {L}, Marja: {M}, Niels: {N}, Erik: {E}, Joep: {J}")