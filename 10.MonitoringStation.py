import datetime
import numpy as np
from itertools import combinations
import math
exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
INPUT_TEST = '''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##'''
INPUT = '''#.#.##..#.###...##.#....##....###
...#..#.#.##.....#..##.#...###..#
####...#..#.##...#.##..####..#.#.
..#.#..#...#..####.##....#..####.
....##...#.##...#.#.#...#.#..##..
.#....#.##.#.##......#..#..#..#..
.#.......#.....#.....#...###.....
#.#.#.##..#.#...###.#.###....#..#
#.#..........##..###.......#...##
#.#.........##...##.#.##..####..#
###.#..#####...#..#.#...#..#.#...
.##.#.##.........####.#.#...##...
..##...#..###.....#.#...#.#..#.##
.#...#.....#....##...##...###...#
###...#..#....#............#.....
.#####.#......#.......#.#.##..#.#
#.#......#.#.#.#.......##..##..##
.#.##...##..#..##...##...##.....#
#.#...#.#.#.#.#..#...#...##...#.#
##.#..#....#..##.#.#....#.##...##
...###.#.#.......#.#..#..#...#.##
.....##......#.....#..###.....##.
........##..#.#........##.......#
#.##.##...##..###.#....#....###.#
..##.##....##.#..#.##..#.....#...
.#.#....##..###.#...##.#.#.#..#..
..#..##.##.#.##....#...#.........
#...#.#.#....#.......#.#...#..#.#
...###.##.#...#..#...##...##....#
...#..#.#.#..#####...#.#...####.#
##.#...#..##..#..###.#..........#
..........#..##..#..###...#..#...
.#.##...#....##.....#.#...##...##'''


def parse_input(input):
    return np.array([list(map(int,row)) for row in input.replace('.','0').replace('#','1').split('\n')])

# Euclidean distance
def euc_dist(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def part1(input):
    coordinates_lists = np.where(input == 1)
    coordinates = list(zip(coordinates_lists[1], coordinates_lists[0]))
    # List all possible pairs of asteroids 
    combs = combinations(coordinates, 2)
    # Initialize counter dict for each asteroid
    detect_count = {}
    for c in coordinates:
        detect_count[c] = 0
    # For each pair, create equation of line between 2 asteroids. 
    # For each of remaining asteroids, see if any asteroid is on this line & BETWEEN 2 asteroids
    all_combs = list(combs)
    b = int(len(all_combs) / 20) # update progress every 5%
    for i,pair in enumerate(all_combs):
        # progress tracking
        if i%b  == 0:
            print('Processed {:,}/{:,} pairs of asteroids ({:.2%})'.format(i, len(all_combs),i/len(all_combs)))     
        a1,a2 = pair
        x1,y1 = tuple(map(float,a1))
        x2,y2 = tuple(map(float,a2))

        coordinates_excluded = set(coordinates)
        coordinates_excluded.remove(a1)
        coordinates_excluded.remove(a2)
        clear_line = True
        for a in coordinates_excluded:
            x,y = tuple(map(float,a))
            # Generic equation of line between (x1,y1) & (x2,y2): (y1−y2)(x−x1)+(x2−x1)(y−y1)=0 
            if ((y1-y2)*(x-x1)+(x2-x1)*(y-y1) == 0) and (euc_dist(a,a1) < euc_dist(a1,a2)) and (euc_dist(a,a2) < euc_dist(a1,a2)):
                clear_line = False
                break
        if(clear_line):
            detect_count[a1] += 1
            detect_count[a2] += 1
    max_detect = 0
    for a in detect_count:
        if (detect_count[a]) > max_detect:
            best_asteroid = a
            max_detect = detect_count[a]
    print('Best location: {} - can detect {} asteroids'.format(best_asteroid, max_detect))    
    return max_detect

# Function to find counter clockwise angle in degrees between 2 vectors
# https://stackoverflow.com/questions/14066933/direct-way-of-computing-clockwise-angle-between-2-vectors
def find_angle_clockwise(v1, v2):
    x1, y1 = v1
    x2, y2 = v2
    dot = x1*x2 + y1*y2 
    det = x1*y2 - y1*x2
    deg = math.degrees(math.atan2(det, dot))
    if(deg < 0):
        deg += 360
    return deg

def part2(input):
    #station_pos = (11, 13) # testcase
    station_pos = (22, 28) # best position from part 1
    coordinates_lists = np.where(input == 1)
    coordinates = set(list(zip(coordinates_lists[1], coordinates_lists[0])))
    coordinates.remove(station_pos)
    
    # Calculate angles formed by (1) starting direction of laser beam with (2) vector from station to asteroids
    angles = {} 
    v0 = (0, -1) # Vector showing initial position of laser - pointing up
    while (len(coordinates) > 0):
        a = coordinates.pop() # pick a random asteroid in the remainings
        vsa = (a[0] - station_pos[0], a[1] - station_pos[1]) # Vector from station to asteroid
        beam_angle = find_angle_clockwise(v0, vsa)
        dist = euc_dist(station_pos, a)
        if beam_angle not in angles:
            angles[beam_angle] = [(a, dist)]
        else:
            angles[beam_angle].append((a, dist))
    
    # Dictionary to hold angles that of each asteroid being vaporated by a laser beam
    # If several asteroids line up, ex. X -> 1 -> 2 ->3 and (1: 45 deg), then (2: 45 + 360 deg), (3: 45 + 720 deg) and so on
    rotate_beams = {}
    for angle in angles:
        asteroids = [item[0] for item in angles[angle]]
        distances = [item[1] for item in angles[angle]]
        distance_ranks = [sorted(distances).index(x) for x in distances]
        for i, r in enumerate(distance_ranks):
            asteroid = asteroids[i]
            rotate_angle = angle + r*360
            rotate_beams[asteroid] = rotate_angle
    
    # sort asteroids on the rotating angles (considering rotations) that they are vaporated by laser beam
    rotate_beams = dict(sorted(rotate_beams.items(), key=lambda item: item[1])) 
    asteroid_200th = list(rotate_beams.keys())[200-1]
    print('From station at {}, 200th asteroid to be vaporized is {}'.format(station_pos, asteroid_200th))  
    return asteroid_200th[0] * 100 + asteroid_200th[1]

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