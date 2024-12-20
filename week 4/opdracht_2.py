import itertools

S = ["U", "D", "L", "R", "S"]

def paths(steps):
    count = 0
    product = tuple(itertools.product(S,repeat = steps+1))
    for steps in product:
        for i in range(len(steps)):
            if i != len(steps)-1:
                if steps[i] != steps[i+1] and steps[i] != 'S' and steps[i+1] != 'S':
                    break
        else:
            count+= 1
    return count

count = paths(10)
print(count)