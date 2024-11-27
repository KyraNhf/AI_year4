import random
import heapq
import math
import config as cf

# global var
grid  = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

class PriorityQueue:
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)[1]

def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get())/10 else 0

def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    return grid[node[0]][node[1]]

def set_grid_value(node, value): 
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    grid[node[0]][node[1]] = value

def search(app, start, goal):
    priority_queue = PriorityQueue()
    priority_queue.put(item = start, priority=0)
    path = {}
    while not priority_queue.empty():
        s = priority_queue.get()
        if s == goal:
            break
        for child in get_children(s):
            cost_child = get_grid_value(child)
            if cost_child == 'b':
                continue
            new_cost = get_grid_value(s) + 1 # new_cost = cost(s) + cost(s, s')
            if cost_child==-1 or new_cost < cost_child :
                set_grid_value(child, new_cost)
                if app.alg.get() == 'A*':
                    priority = heuristic(child, goal)
                else:
                    priority = new_cost
                priority_queue.put(item=child, priority=priority)
                path[child] = s
                app.plot_node(child, color=cf.PATH_C)
                app.pause()
    if goal in path:
        app.draw_path(path)

def get_children(node):
    children = []
    if node[0] > 0:
        children.append((node[0] - 1, node[1]))
    if node[0] < cf.SIZE - 1:
        children.append((node[0] + 1, node[1]))
    if node[1] > 0:
        children.append((node[0], node[1] - 1))
    if node[1] < cf.SIZE - 1:
        children.append((node[0], node[1] + 1))
    return children

def heuristic(node, goal):
    distance = math.dist(node, goal)
    return distance