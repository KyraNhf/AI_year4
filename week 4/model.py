import random
import math
import config as cf
from pprint import pprint
from decimal import *

# global var
grid  = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

#-----------------------------------------------------------------------------
# (x, y) = (0, 0) is the top left of the grid
# a state (x, y, action) is a combination of current position (x,y) and the
# previous action/move
# where: 0 <= x,y <= cf.SIZE-1 and action is one of {'L','R','U','D','S'}
#-----------------------------------------------------------------------------

class Distribution(dict):
    # an extention of a dictionary
    def __missing__(self, key):
        # if the key is missing, return probability 0
        return 0

    def renormalize(self):
        # scale all the probabilities so that they sum up to 1
        # renormalization is necessary for positions at borders/in corners

        normalization_constant = sum(self.values())
        for key in self.keys():
            self[key] /= normalization_constant

def get_all_states():
    # returns a (long) list of all possible states (= position and previous action) ex. (7, 7, 'S')
    # we need this in Viterbi (15*15*5-4*15=1065 states)
    all_states = []
    for x in range(cf.SIZE):
        for y in range(cf.SIZE):
            possible_prev_actions = ['L', 'R', 'U', 'D', 'S']

            if x == 0: # previous action could not have been to go right
                possible_prev_actions.remove('R')
            if x == cf.SIZE - 1: # could not have gone left
                possible_prev_actions.remove('L')
            if y == 0: # could not have gone down
                possible_prev_actions.remove('D')
            if y == cf.SIZE - 1: # could not have gone up
                possible_prev_actions.remove('U')

            for action in possible_prev_actions:
                all_states.append((x, y, action))
    return all_states

def transition_model(state):
    # given a state (position and previous action), 
    # return a dict with k,v = possible next states, probabilities
    # note: top left position is (0,0)
    x, y, prev_move = state
    distr_next_states = Distribution()
    possible_moves=[('S',0,0),('L',-1,0),('R',1,0),('U',0,-1),('D',0,1)]
    new_position={'S':(0,0), 'L':(-1,0), 'R':(1,0),'U':(0,-1), 'D':(0,1)}

    if prev_move == 'S':
        for curr_move, hor_mov, vert_move in possible_moves:
            next_x = x + hor_mov
            next_y = y + vert_move
            # if the move remains on the grid (0..cf.SIZE-1), get the distribution for this move
            if (next_x >= 0) and (next_x < cf.SIZE) and (next_y >= 0) and (next_y < cf.SIZE):
                # previous move = stay, 0.2 prob for all possible positions
                distr_next_states[(next_x, next_y, curr_move)] = 0.2
    else:
        # non_stay -> stay
        distr_next_states[(x, y, 'S')] = 0.1
        next_x = x + new_position[prev_move][0]
        next_y = y + new_position[prev_move][1]
        # if the move remains on the grid (0..cf.SIZE-1), get the distribution for this move
        if (next_x >= 0) and (next_x < cf.SIZE) and (next_y >= 0) and (next_y < cf.SIZE):
            # non_stay -> non-stay
            distr_next_states[(next_x, next_y, prev_move)] = 0.9

    # if were at border or in corner then renormalize
    distr_next_states.renormalize()
    return distr_next_states

def test_transition_model():
    assert transition_model((0, 0, 'R')) == {(0, 0, 'S'): 0.1, (1, 0, 'R'): 0.9}
    assert transition_model((0, 0, 'L')) == {(0, 0, 'S'): 1.0}
    assert transition_model((0, 0, 'U')) == {(0, 0, 'S'): 1.0}
    assert transition_model((0, 2, 'S')) == {(0, 2, 'S'): 0.25, (1, 2, 'R'): 0.25, (0, 1, 'U'): 0.25, (0, 3, 'D'): 0.25}
    assert transition_model((0, 2, 'L')) == {(0, 2, 'S'): 1.0}
    assert transition_model((2, 0, 'L')) == {(2, 0, 'S'): 0.1, (1, 0, 'L'): 0.9}
    assert transition_model((2, 2, 'S')) == {(2, 2, 'S'): 0.2, (1, 2, 'L'): 0.2, (3, 2, 'R'): 0.2, (2, 1, 'U'): 0.2, (2, 3, 'D'): 0.2}
    assert transition_model((2, 2, 'L')) == {(2, 2, 'S'): 0.1, (1, 2, 'L'): 0.9}

def get_next_state(distr_next_states):
    pass

def observation_model(pos):
    # given an observed position, return the distribution for possible (real) positions
    x, y = pos
    possible_pos = Distribution()
    probs = [(0, 0, 0.2), (-1, 0, 0.2), (1, 0, 0.2), (0, -1, 0.2), (0, 1, 0.2)]

    for dx, dy, prob in probs:
        # position is on the grid (0..cf.SIZE-1), get the observation prob for this position
        if (x + dx >= 0) and (x + dx < cf.SIZE) and (y + dy >= 0) and (y + dy < cf.SIZE):
            possible_pos[(x + dx, y + dy)] = prob

    # at edge or in corner less than 5 positions
    possible_pos.renormalize()
    return possible_pos

def test_observation_model():
    assert observation_model((0, 0)) == {(0, 0): 0.3333333333333333, (1, 0): 0.3333333333333333, (0, 1): 0.3333333333333333}
    assert observation_model((0, 2)) == {(0, 2): 0.25, (1, 2): 0.25, (0, 1): 0.25, (0, 3): 0.25}
    assert observation_model((1, 0)) == {(1, 0): 0.25, (0, 0): 0.25, (2, 0): 0.25, (1, 1): 0.25}
    assert observation_model((1, 1)) == {(1, 1): 0.2, (0, 1): 0.2, (2, 1): 0.2, (1, 0): 0.2, (1, 2): 0.2}
    assert observation_model((2, 0)) == {(2, 0): 0.25, (1, 0): 0.25, (3, 0): 0.25, (2, 1): 0.25}
    assert observation_model((2, 1)) == {(2, 1): 0.2, (1, 1): 0.2, (3, 1): 0.2, (2, 0): 0.2, (2, 2): 0.2}
    assert observation_model((2, 2)) == {(2, 2): 0.2, (1, 2): 0.2, (3, 2): 0.2, (2, 1): 0.2, (2, 3): 0.2}
    assert observation_model((2, 3)) == {(2, 3): 0.25, (1, 3): 0.25, (3, 3): 0.25, (2, 2): 0.25}
    assert observation_model((3, 0)) == {(3, 0): 0.3333333333333333, (2, 0): 0.3333333333333333, (3, 1): 0.3333333333333333}

def load_data(filename):
    real_states = []
    observations = []

    with open(filename, 'r') as f:
        for line in f:
            if line[0] == '#':
                continue
            line = line.strip()
            parts = line.split()

            prev_action = parts[0]

            # get real position
            string_xy = parts[1].split(',')
            real_x = int(string_xy[0])
            real_y = int(string_xy[1])
            real_states.append((real_x, real_y, prev_action))

            # get observed position
            if parts[2] == 'missing':
                observations.append(None)
            else:
                string_xy = parts[2].split(',')
                observed_x = int(string_xy[0])
                observed_y = int(string_xy[1])
                observations.append((observed_x, observed_y))

    return real_states, observations


def Viterbi(all_possible_states, observations):
    V = [{}]

    for s in all_possible_states:
        tm = transition_model(s)[s]
        V[0][s] = {
            'prob': math.log(tm) if tm > 0 else float('-inf') ,
            'prev': None
        }
    for t in range(1, len(observations)):
        V.append({})
        for s in all_possible_states:
            mx_prob = float('-inf')
            prev_state_selected = None

            for prev_s in all_possible_states:
                transition_prob = transition_model(prev_s)[s]
                if transition_prob > 0:
                    prob = V[t - 1][prev_s]['prob'] + math.log(transition_prob)
                else:
                    prob = float('-inf')

                # kijk of die hogere kans heeft dan de vorige
                if prob > mx_prob:
                    mx_prob = prob
                    prev_state_selected = prev_s

            # backpointer
            x, y, state = s
            ob_prob = observation_model((x, y))[observations[t]]
            if ob_prob > 0:
                mx_observation_prob = math.log(ob_prob)
            else:
                mx_observation_prob = float('-inf')
            V[t][s] = {
                'prob': mx_prob + mx_observation_prob,
                'prev': prev_state_selected
            }

    max_prob = max(val['prob'] for val in V[T - 1].values())
    max_state = None
    for state, data in V[T - 1].items():
        if data['prob'] == max_prob and not None:
            max_state = state

    best = [max_state]
    for t in range(T - 1, 0, -1):
        prev_s = V[t][max_state]['prev']
        best.insert(0, prev_s)
        max_state = prev_s

    return best

def print_trellis(TR):
    THRESHOLD = -10
    for i in (range(len(TR))):
        d = TR[i]
        # filter dictionary on probability
        #f = dict((k,prob) for (k,prob) in d.items() if prob > THRESHOLD)
        print()
        print(f'**** step {i} ****')
        # dicts are sorted by key before printed
        pprint(d)

def move_robot (app, start):
    # plot a fully random path for demonstration
    # start[0]=x and start[1]=y
    prev = start
    for i in range(100):
        dir = random.choice(['L', 'R', 'U', 'D'])
        match dir:
            case 'L': current = prev[0]-1, prev[1]
            case 'R': current = prev[0]+1, prev[1]
            case 'D': current = prev[0], prev[1]-1
            case 'U': current = prev[0], prev[1]+1

        # check if new position is valid
        if (current[0] >= 0 and current[0] <= cf.SIZE-1 and current[1] >= 0 and current[1] <= cf.SIZE-1):
            app.plot_line_segment(prev[0], prev[1], current[0], current[1], color=cf.ROBOT_C)
            app.pause()
            app.plot_line_segment(prev[0], prev[1], current[0], current[1], color=cf.PATH_C)
            prev = current
            app.pause()

    app.plot_node(current, color=cf.ROBOT_C)

real_states, observations = load_data("observations_v1.txt")
states = get_all_states()
print(Viterbi(states, observations))