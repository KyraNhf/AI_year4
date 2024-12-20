import itertools
import time

S = ["U", "D", "L", "R", "S"]
STEPS = 10

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

t0 = time.process_time()
count = paths(STEPS)
t1 = time.process_time()
print(f'Er zijn {count} mogelijkheden bij {STEPS} steps. Berekend in {t1-t0} seconden')