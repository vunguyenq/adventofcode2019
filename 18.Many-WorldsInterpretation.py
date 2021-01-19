import datetime
import numpy as np
from collections import deque
exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
INPUT_TEST = '''########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################'''

INPUT = '''#################################################################################
#.#...........#...#.....#.......#...#...#.....#.....#.....#...#...#..g.........x#
#.#.#####.###Z#.#.#.###.#.#.###.#.###.#.#.###.#.#####.#.#.#.#.#.###.###########.#
#...#...#.#.....#.#.#.#...#.#...#.#...#.#.#.#.#.#.....#p#.#.#.#.......#...#.....#
#.#####.#.#########.#.#####.#.###.#.###.#.#.#.#.#.#####.#.#.#.#######.###.#.###.#
#.......#...#.......#.....#.#.#.....#...#.#.....#...#...#...#.#.....#.....#.#...#
###########.#.#########.###.#.###.###.###.#####.###.#.#######.#.###.#####.#.#.###
#...V.....#.......#...#.#...#...#...#...#.#...#...#.#.#.......#.#.#.#.....#.#...#
#.#######.#######.#.#.#.#.#####.#######.#.#.#.#.###.#.#######.#.#.#.#.#####B###.#
#.#.......#...#.....#...#.....#.....#...#...#.#.#...#.......#...#...#.....#...#.#
#.#.#####.#.#K#.#############.#####.#.#.#####.###.#########.#####.#######.###.###
#.#.#.....#.#.#...#...#.......#...#.#.#.#...#.#...#...#.....#.....#....l..#.#...#
#.#.#####.#.#.###.#.#.#.#######.#.#.#.###.#.#.#.###.#.#.#####.#######.#####.###.#
#.#.....#.#.#...#.#.#.#.....#...#...#...#.#...#.#...#.#...#...#.....#.........#.#
#.#####.#.#.###.#.#.#.#####.#####.#####.#.#####.#.#.#####.#.###.###.#######.###.#
#.#...#.#.#...#.#.#.#..j..#.....#.......#.#...#...#.#...#.#.....#...#.......#...#
#.#.###.#Q###.#.###.#####.#####I#######.#.#.#.#.#####.#.#.#######.#######.###.#.#
#...#...#.#...#.....#...#.....#.....#...#.#.#...#.....#.#.#.#.....#.....#h..#.#.#
###.#.#####.#########.#.#####.#.###.#.###.#.#####.#####.#.#.#.#####.###.#####.#.#
#...#...#...#.......#.#.......#...#.#...#.#.#.....#.....#.#.....#.....#.......#.#
#.#####.#.###.#####.#.###########.#.#####.#.#.#####.#####.#.###.#####.###########
#.....#.#...#.#.....#.#.......#...#.#...#...#.#.......#...#.#.#.....#.....#.....#
#####.#.###.#.#.###.###.###.###.###.#.#.#####.#######.###.###.#####.#####.#.###.#
#.#...#...#.#.#.#...#.....#...#.#.#.#.#.#.....#...#.#.....#...#...#.....#.....#.#
#.#.###.###.###.#.###########.#.#.#.#.#.#.#.###.#.#.#####.#.#####.#####.#######.#
#.#...#...#.....#.#..e....#...#...#...#.#.#.#...#.#...#...#.....#.....#.#.......#
#.###.###.#######.#.#####.#.#####.#####.#.###.###.#.#.#.#######.#.#.###.#.#####.#
#.#...#.#...#...#...#.....#.#.........#.#.#.....#.#.#.#.......#.#.#.....#...#...#
#.#.###.#.###.#.#####.#####.#.#########.#.#.#####.###.###.#####.#.#########.#.###
#...#...#...#.#.....#.#.#.......#...#...#.#o#.#...#...#...#.....#.#.........#...#
#.#####.###.#.#.#####.#.#.#######.#.#.#.#.#.#.#.###.###.###.#####.#####.#######U#
#.........#...#...#...#...#.......#...#.#.....#...#.....#.#.#...#.#.....#.....#.#
#########.#######.#.###.###.###########.#.#######.#.#####.#.#.#.#.#.#########.#.#
#.......#.......#...#.....#...#.#.....#.#.#.....#.#.......#.#.#.#.#.#.......#...#
#.#####.#######.#############.#.#.#.###.#.#.###.#.#########.#.###.#.#.#####.#####
#.....#.#.......#.....#.......#.#.#.#...#.#.#.....#...#.....#.#...#.....#.#..tE.#
#.###.###.#######.###.#.#######.#.#.#.###.#.#######.#.#.#####.#.#######.#.#####.#
#.S.#...#.....#...#.#c..#...#.....#.#.#.#.#...#.....#..s#.....#.#.....#...#...#.#
###.###.#####.#.###.#####.#.#.#####.#.#.#.###.#.#########.###.#.###.#.#####.#.#.#
#.....#.........#.........#.......#.........#...#...........#.....F.#.......#...#
#######################################.@.#######################################
#m........#.............#...........#.........#.....#.........#.....#...#.......#
###.#####.#########.#####.#####.###.#.#.#.#.#.#.###.#.#####.#.#.###.#.#.#.###.#.#
#...#.#...#.......#...#...#...#.#.#...#.#.#.#.#...#...#...#.#.....#.#.#.#.#...#.#
#.###W#.###.#####.#.#.#O###.#.#.#.#####.###.#####.#####.#.#########.#.#.#.#.###.#
#.#.......#...#.#.#.#.#...#.#.#.#...#...#...#...#.....#.#.#...#...#.C.#.#.#.#...#
#.#######.###.#.#.#.#.###.#.#.#.#.###.###.###.#.#.#####.#.#.#.#.#.#####.#.#.###.#
#.#...#.#.#...#...#.#.#...#.#...#.......#.....#...#.....#.#.#.#.#.....#...#...#.#
#.#.#.#.#.#.###.###.#.#.###.#####.#######.#########.#####.#.#.#.#####.#.#####.#.#
#.#f#.#.#.#.#.#.#...#...#...#...#...#...#.#.......#...#.....#.#.#...#.#...#.#.#.#
#.#.#.#.#.#.#.#.#.#######.###.###.###.#D#.###.#.#####.#######.#.#.###.###.#.#.#.#
#...#.#...#.#...#.....#.#...#.....#...#.#...#.#.#...#.....#.#.#.#.....#.....#.#.#
#####.#.###.#.#######.#.###.###.###.###.###.#.###.#.#####.#.#.#.#.#####.#####.#.#
#.....#...#.#.#...#...#...#...#.#a..#.#.#.#.#.....#.....#.#...#.#w#...#...#...#.#
#.#######.#.#.#.#.#.###.#####.###.###.#.#.#.#.#######.###.#.###.#.#.#####.#.###.#
#.#.....#.#.#.#.#.#...#.#...#...#...#.#.#...#.....#...#...#...#.#.#.......#.#...#
#.###.#.#.#.#.#.#.###.#.#.#.#.#.###.#.#.#.#########.#.#.#####.#M#.#########.###.#
#...#.#...#.#...#.#.....#.#.#.#...#.#..d#.#.........#.#.#.......#...#.....#...#.#
#.#.#.#####.#####.#######.#.#####.#.#.###.###.#####.###.#.#########.#.###.###.#.#
#.#.#...#...#.............#.......#.#...#.#i..#.....#...#.#.......#...#.#...#.#.#
###.###.#.###.#################.###A###.#.#.###.#####.###.#.#####.#####.###.#.###
#...#.....#.#.#.....#.Y...#...#.#...#.#.#...#.#.#.#...#...#.#.N...#.........#...#
#.###.#####.#.#.###.#####.###.#.#.###.#.#####.#.#.#.###.###.#############.#####.#
#...#.#...#...#.#.#.....#...#...#.#...R.#.#.....#.#...#...#.....#...#...#q....#.#
#.#.###.#.#.###.#.###.#.###.#####.#.#####.#.#####.###.#########.#.#.#.#.#####.#.#
#.#...#.#.#.#...#...#.#...#..y....#.#...#.#.#.......#.........#...#...#...#.#.#.#
#####.#.#.###.###.#.#.###.#########.#.#.#.#.#.#####.#########.###########.#.#.#.#
#...#.#.#...#.#...#.#...#.....#...#.#.#.#.#.#.#.............#.#...#.....#.#.#.#.#
#.#.#.#.###.#.#.#######.#####.#.#.#.###.#.#.#.#.#######.#####.#.#.#.###.#.#.#.#.#
#.#...#.#.#.#...#.......#...#.#.#r..#...#...#.#.#.....#.#...#...#.#...#...#.#.#.#
#T###.#.#.#.###.#.#######.#.###.#####.###.#####.#.###.#.#.#.#####.###.#####.#.#.#
#.#...#u..#.....#...#...#n#...#.#.#.....#.#...#.#...#.#.#.#.#.......#.....#.....#
#.#.#####.#########.#.#H#.###.#.#.#.###.#.#.#.#.#.###.#.#.#J#.###########.#####.#
#.#.....#.#...#...#.#.#...#.#...#.#...#.#...#.#...#...#.#.#...#.........#.....#.#
#.#######.#.###.#.#.#.#####.#####.###.#.#####.#.###.#####.#.###.#####.#######.#.#
#.#.......#.#...#...#...#.....L.#.....#.#.#...#..v#z..#...#.#...#...#.......#.#.#
#.#.#######.#.###.#####.#.#####.#######.#.#.#########.#.#####.###.#.###.#####.#.#
#.#.#k......#...#.#...#...#.....#.....#.#.#.....#...#.#..b....#...#...#...#...#.#
#.#.#.#####.###.###.#.#####.#####.###.#.#.#####.#.#.#.#############.#.###X#.###.#
#.....#.......#...G.#.............#.....#.........#...P.............#...#...#...#
#################################################################################'''

INIT_KEY = int('1' + '0' * 26,2) # Integer to track all keys appearing in maze. 0st bit = 1, 1st bit = z, 2nd bit = y, ... , 27th bit = a

def parse_input(input):
    data = []
    keys = INIT_KEY 
    for i,row in enumerate(input.split('\n')):
        row_data = []
        for j,c in enumerate(row):
            if(c=='#'):
                row_data.append(0)
            elif(c=='.'):
                row_data.append(1)
            elif(c=='@'):
                robot = (i,j)
                row_data.append(1)
            else:
                val = ord(c)
                row_data.append(val)
                if (97 <= val <= 122):
                    keys = set_bit(keys, val - 97) # key
        data.append(row_data)
    return keys, robot, np.array(data)

# Returns an integer with the bit at 'offset' set to 1.
def set_bit(int_num, offset):
    mask = 1 << offset # rotate bit "1" offset steps to the right, producing mask "10000..." (_offset_ zeroes)
    return(int_num | mask)

# https://www.reddit.com/r/adventofcode/comments/ednz2o/2019_day_18_for_dummies/
# https://medium.com/@werner.altewischer/advent-of-code-day-18-2019-the-real-challenge-aea3d4e96708
# General idea: 
#   - BFS, each node is a combination of (robot position) + (all keys found so far) = (X,Y,PossessedKeys). 
#   - Shortest path is the first node that contains all keys in PossessedKeys. Length of path is the depth of this node in BFS tree
#   - Use bitmask to encode PossessedKeys, for example 26 bit sequence 100101... => PossessedKeys = a,d,e,...
def bfs(robot, maze, all_keys):
    nrows, ncol = maze.shape
    visited = {(robot,INIT_KEY):0}
    bfs_queue = deque([(robot,INIT_KEY)])
    all_keys_found = False

    while(len(bfs_queue) > 0 and not(all_keys_found)):
        current_node = bfs_queue.popleft()
        coordinates,keys = current_node
        x,y = coordinates
        for adjacent in [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]:
            if(x < 0 or y < 0 or x >= nrows or y>=ncol): # out of bound
                continue
            adjacent_val = maze[adjacent[0]][adjacent[1]]
            #print((x,y),adjacent, adjacent_val, chr(adjacent_val))
            if adjacent_val == 0: # Walls
                continue
            elif adjacent_val == 1: # Empty space
                new_node = (adjacent,keys)
            elif (65 <= adjacent_val <= 90): # Doors
                key_bits = bin(keys)[2:].ljust(27, '0') # convert keys value to a bit string of length 27 (=1 + 26 bits), including trailing zeroes
                if key_bits[26 - (adjacent_val - 65)] == '1': # has key to open door
                    new_node = (adjacent,keys)
                else: # hits a door with no key, cannot pass
                    continue
            elif (97 <= adjacent_val <= 122): # found a key
                new_keys = set_bit(keys, adjacent_val - 97) # set i_th bit to 1 from right to left
                new_node = (adjacent,new_keys)
            
            if(new_node not in visited):
                visited[new_node] = visited[current_node] + 1
                bfs_queue.append(new_node)

            if(new_node[1] == all_keys):
                all_keys_found = True
                break
    return visited[new_node]

def part1(input):
    all_keys, robot, maze = input
    return bfs(robot, maze, all_keys)

# Idea for part 2:
# Theoretically can be solved by the same approach with Part 1. However instead of (X,Y,PossessedKeys), a state (node in the graph) is now (X1,Y1,X2,Y2,X3,Y3,X4,Y4,PossessedKeys) because of 4 robots
# Reality: 
#   + Implemented, yielded correct result on 4 test cases of Part 2.
#   + However, on real puzzle input, queue & visisted grew to 2.5M & 32M nodes respectively without returning an answer. Search space became too large
# Another approach: apply BFS (Part 1) in each quadrant/ quarter. Change: let robot go through doors in a quater if keys for such doors are not in the same quarter
# This is NOT a generalized solution, but worked
def part2(input):
    _, robot, maze = input
    # Split vault into 4 vaults with 4 robots
    x,y = robot
    robots = [(x-1,y-1),(x+1,y-1),(x+1,y+1),(x-1,y+1)]
    #print(robots)
    for r in robots:
        maze[r[0]][r[1]] = 1
    for t in [robot,(x,y+1),(x,y-1),(x+1,y),(x-1,y)]:
        maze[t[0]][t[1]] = 0

    # Apply bfs scan to each of 4 quarters
    quarters = [maze[:41,:41],maze[40:,:41],maze[:41,40:],maze[40:,40:]]
    robots = [(39,39),(1,39),(39,1),(1,1)]
    result = 0
    for q,quarter in enumerate(quarters):
        quarter_keys = INIT_KEY
        # If quarter contains doors without keys in the same quarter, robot can go pass such doors
        for i in range(quarter.shape[0]):
            for j in range(quarter.shape[0]):
                val = quarter[i][j]
                # Remove doors that don't have keys in the same quarter
                if(65 <= val <= 90) and ((val + 97 - 65) not in quarter):
                    quarter[i][j] = 1 
                elif (97 <= val <= 122): # keys in that quarter
                    quarter_keys = set_bit(quarter_keys, val - 97) 
        quarter_shortest = bfs(robots[q], quarter, quarter_keys)
        print('Shortest part on quarter {}: {}'.format(q+1, quarter_shortest))
        result += quarter_shortest
    return result

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