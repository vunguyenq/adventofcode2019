import datetime
import numpy as np
from itertools import combinations
from math import gcd

exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
INPUT_TEST = '''<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>'''
INPUT = '''<x=-1, y=-4, z=0>
<x=4, y=7, z=-1>
<x=-14, y=-10, z=9>
<x=1, y=2, z=17>'''

class Moon:
    def __init__(self, starting_pos):
        self.pos = starting_pos
        self.vel = np.zeros(3, dtype = int)
        self.gravity = np.zeros(3, dtype = int)

def parse_input(input):
    return [np.fromstring(row, dtype=int, sep=',') for row in input.replace('x=','').replace('y=','').replace('z=','').replace('<','').replace('>','').split('\n')]

def norm1(x): # Normalize a scalar number to 1, keeps its positive / negative sign
    if (x == 0):
        return 0
    return int(x / abs(x))

def time_step(moons):
    combs = combinations(moons, 2)
    norm_axes = np.vectorize(norm1) # Normalize all axes 1d vector to 1, keeps its positive / negative sign. For exp [4  0 -3] => [1  0 -1]
    # Reset gravity vector of all moons to [0 0 0]
    for moon in moons:
        moon.gravity = np.zeros(3, dtype = int)
    # Apply gravity
    for comb in (list(combs)):
        moon1, moon2 = comb
        moon1.gravity += norm_axes(moon2.pos - moon1.pos)
        moon2.gravity += norm_axes(moon1.pos - moon2.pos)
    # Update velocity after all gravity is calculated, then apply velocity to change position
    for moon in moons:
        moon.vel += moon.gravity
        moon.pos += moon.vel

def part1(input):
    # Initilaize moons
    moons = []
    for pos in input:
        moons.append(Moon(pos))
    # Execute time steps
    for _ in range(1000):
        time_step(moons)
    # Calcuate total energy
    total_energy = 0
    for moon in moons:
        print(moon.pos, moon.vel)
        total_energy += sum(abs(moon.pos)) * sum(abs(moon.vel))
    return total_energy

# Execute a single time step on a single axis
def time_step_axis(axis_pos, axis_vels):
    combs = combinations(range(len(axis_pos)),2)
    gravity = np.zeros(len(axis_pos)).astype(int)
    for comb in combs:
        pos1, pos2 = axis_pos[comb[0]], axis_pos[comb[1]]
        gravity[comb[0]] += norm1(pos2 - pos1)
        gravity[comb[1]] += norm1(pos1 - pos2)
    for i in range(len(axis_pos)):
        axis_vels[i] += gravity[i]
        axis_pos[i] += axis_vels[i]

# Execute time steps on a single axis until position & velocity on that axis repeats a previous state
def step_untill_repeat(pos, vel):
    # Save position + velocity of initial state
    hash_state_0 = hash(tuple(pos + vel))
    # Run time step until state 0 repeats
    i=0
    while(True):
        i+=1
        time_step_axis(pos, vel)
        hash_state = hash(tuple(pos + vel))
        if hash_state == hash_state_0:
            return i
    return 0

# Find least common multiply of a list of integers
def lcm(lst):
    lcm = lst[0]
    for i in lst[1:]:
        lcm = lcm*i//gcd(lcm, i)
    return lcm

# Idea: position and velocity are updated on each axis separately
# Therefore we can brute force minimum time steps for (position + velocity) to repeat on each of 3 axis. Result will be LCM of 3 time steps
def part2(input):
    pos_x, pos_y, pos_z = list(map(list,list(zip(*input))))
    vel_x, vel_y, vel_z = [[0,0,0,0] for _ in range(3)]

    time_x = step_untill_repeat(pos_x, vel_x)
    print('Position and gravity on x axis repeats after {} time steps'.format(time_x))
    time_y = step_untill_repeat(pos_y, vel_y)
    print('Position and gravity on y axis repeats after {} time steps'.format(time_y))
    time_z = step_untill_repeat(pos_z, vel_z)
    print('Position and gravity on z axis repeats after {} time steps'.format(time_z))

    return lcm([time_x,time_y,time_z])

if __name__ == "__main__":
    if(exec_test_case == 1):
        input = INPUT_TEST
    else:
        input = INPUT
    input = parse_input(input)

    start_time = datetime.datetime.now() 
    if (exec_part == 1):
        result = part1(input)
    else:
        result = part2(input)
    end_time = datetime.datetime.now() 
    print('Part {} time: {}'.format(exec_part, end_time - start_time))
    print('Part {} answer: {}'.format(exec_part, result))