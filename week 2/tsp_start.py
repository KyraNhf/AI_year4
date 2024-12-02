import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')

def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)

def try_all_tours(cities):
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = alltours(cities)
    return min(tours, key=tour_length)

def alltours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # note: cities is a set, sets don't support indexing
    start = next(iter(cities)) 
    return [[start] + list(rest) for rest in itertools.permutations(cities - {start})]

def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1]) for i in range(len(tour)))

def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed() # the current system time is used as a seed
                  # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height)) for c in range(n))

def plot_tour(tour): 
    # plot the cities as circles and the tour as lines between them
    start = [tour[0]]
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-') # blue circle markers, solid line style
    plt.plot([p.x for p in start], [p.y for p in start], 'rs')
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()

def plot_tsp(algorithm, cities, altered=False):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.process_time()
    if altered:
        tour = alter_tour(algorithm(cities))
    else:
        tour = algorithm(cities)
    t1 = time.process_time()
    length = tour_length(tour)
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), length, t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)
    return length

def nn_tsp(cities):
    # looks at neighbours of starting city and creates tours with this staring point
    # returns the shortest tour
    start = next(iter(cities))
    tour = [start]
    unvisited = set(cities - {start})
    while unvisited:
        neighbour = nearest_neighbour(tour[-1], unvisited)
        tour.append(neighbour)
        unvisited.remove(neighbour)
    return tour

def nearest_neighbour(city, cities):
    # Find the neighbour n in cities that is nearest to city.
    return min(cities, key=lambda n: distance(n, city))

def difference(len_a, len_b):
    #calculates difference between two tours
    return (abs(len_a - len_b) / ((len_a + len_b) / 2)) * 100


def reverse_segment_if_better(tour, i, j):
    "If reversing tour[i:j] would make the tour shorter, then do it."
    # Given tour [...A-B...C-D...], consider reversing B...C to get [...A-C...B-D...]
    A, B, C, D = tour[i-1], tour[i], tour[j-1], tour[j % len(tour)]
    # Are old edges (AB + CD) longer than new ones (AC + BD)? If so, reverse segment.
    if distance(A, B) + distance(C, D) > distance(A, C) + distance(B, D):
        tour[i:j] = reversed(tour[i:j])

def alter_tour(tour):
    "Try to alter tour for the better by reversing segments."
    original_length = tour_length(tour)
    for (start, end) in all_segments(len(tour)):
        reverse_segment_if_better(tour, start, end)
    # If we made an improvement, then try again; else stop and return tour.
    if tour_length(tour) < original_length:
        return alter_tour(tour)
    return tour

def all_segments(len):
    "Return (start, end) pairs of indexes that form segments of tour of length len."
    return [(start, start + length)
            for length in range(len, 2-1, -1)
            for start in range(len - length + 1)]

if __name__ == '__main__':
    # give a demo with 10 cities using brute force & nn
    places = make_cities(5000)
    # length_force = plot_tsp(try_all_tours, places)
    length_nn = plot_tsp(nn_tsp, places)
    length_altered = plot_tsp(nn_tsp, places, altered=True)
    # plot_tour(alter_tour(nn_tsp(places)))
    # calculate difference
    # print(difference(length_nn, length_force))

# force duurt bij 10 0,3 sec, bij 11 2,2 en bij 12 29,2
# nn duurt bij elke 0,0 sec, zelfs bij 500, bij 5000 doet hij er rond 0,5 sec over
# lengte bij 500 is 19834,1
# bij N = 50 steden zijn er meestal 3 kruisingen

# kruisingen vinden pseudocode:
# kijken voor AB en CD of de coördinaten binnen hetzelfde bereik en domein vallen
# het is niet noodzakelijk om te controleren of de nieuwe route korter is als je de gevonden kruising ongedaan maakt
# want routes zonder kruisingen zijn altijd korter dan routes met kruisingen
"""
def find_intersection(tour):
    squares = []
    for i in range(len(tour)):
        A = tour[i]     # (x, y)
        B = tour[i+1]   # (w, z)
        squares += [[A(x,y), AB(w-x, z-y), B(w, z), BA(w+x, z+y)]]
    
    intersections = []
    
    for i in range(len(squares):
        start = squares[i]  
        for square in squares[i:]:
            if (start[0][0] < square[2][0] 
            and start[2][0] > square[0][0] 
            and start[0][1] < square[2][1] 
            and start[2][1] > square[0][1]): 
                intersections += start
    return intersections

"""

# 2-opt doet over 500 0,1 - 0,2 seconden, over 5000 ongeveer 17 sec
# tijdscomplexiteit van 2-opt is O(n^3), in dit geval is n het aantal cities


