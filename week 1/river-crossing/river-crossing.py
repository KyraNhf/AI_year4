from copy import deepcopy

farmer = 'F'
goat ='G'
cole = 'C'
wolf = 'W'

state = ({farmer, goat, cole, wolf}, set())

def find_all_paths(node, path=[]):
    path = path + [node]
    if {wolf, goat, farmer, cole}.issubset(node[1]):
        return [path]
    if is_invalid_state(node) :
        return [path]
    paths = []
    for child in next_states(node):
        if child not in path:
            new_paths = find_all_paths(child, path)
            for new_path in new_paths:
                paths.append(new_path)
    return paths

def move_items(node, direction, item):
    left, right = node
    if direction == left:
        if item is not farmer:
            right.remove(item)
            left.add(item)
        right.remove(farmer)
        left.add(farmer)
    elif direction == right:
        left.remove(item)
        left.remove(farmer)
        right.add(item)
        right.add(farmer)
    next_node = (left, right)
    return next_node

def is_invalid_state(node):
    left = node[0]
    right = node[1]
    if ({wolf, goat, cole}.issubset(left) and {farmer}.issubset(right)) or ({wolf, goat, cole}.issubset(right) and {farmer}.issubset(left)):
        return True
    elif ({wolf, goat}.issubset(left) and {farmer, cole}.issubset(right)) or ({wolf, goat}.issubset(right) and {farmer, cole}.issubset(left)):
        return True
    elif ({goat, cole}.issubset(left) and {farmer, wolf}.issubset(right)) or ({goat, cole}.issubset(right) and {farmer, wolf}.issubset(left)):
        return True
    else:
        return False

def next_states(node):
    states = []
    left = node[0]
    right = node[1]
    if {farmer}.issubset(left) :
        for item in left:
            if item is not farmer:
                n = deepcopy(node)
                move = move_items(n, right, item=item)
                states.append(move)
    elif {farmer}.issubset(right) :
        for item in right:
            n = deepcopy(node)
            move = move_items(n, left, item=item)
            states.append(move)
    return states

def print_solution(paths):
    for path in paths:
        if path[-1][0] == set():
            for node in path:
                print(f"{''.join(list(map(str, node[0])))}| |{''.join(list(map(str, node[1])))}")
            print('The end!')

solution = find_all_paths(state)
print_solution(solution)

# branching factor = 3
# max_depth = 8
# O(3^8) = 6561 (welke eenheid?)

