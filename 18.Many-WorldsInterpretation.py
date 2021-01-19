import datetime
import numpy as np
from collections import deque
import treelib
exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
## Part 2 testcase 1, answer = 8
# INPUT_TEST = '''####### 
# #a.#Cd#
# ##...##
# ##.@.##
# ##...##
# #cB#Ab#
# #######''' 
## Part 2 testcase 2, answer = 24
# INPUT_TEST = '''###############
# #d.ABC.#.....a#
# ######...######
# ######.@.######
# ######...######
# #b.....#.....c#
# ###############'''
## Part 2 testcase 3, answer = 32
# INPUT_TEST = '''#############
# #DcBa.#.GhKl#
# #.###...#I###
# #e#d#.@.#j#k#
# ###C#...###J#
# #fEbA.#.FgHi#
# #############'''
## Part 2 testcase 4, answer = 72
INPUT_TEST = '''#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############'''
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
def part1(input):
    all_keys, robot, maze = input
    nrows, ncol = maze.shape
    visited = treelib.Tree()
    visited.create_node((*robot,INIT_KEY),(*robot,INIT_KEY))
    bfs_queue = deque([(*robot,INIT_KEY)])
    all_keys_found = False
    while(len(bfs_queue) > 0 and not(all_keys_found)):
        current_node = bfs_queue.popleft()
        x,y,keys = current_node
        for adjacent in [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]:
            if(x < 0 or y < 0 or x >= nrows or y>=ncol): # out of bound
                continue
            adjacent_val = maze[adjacent[0]][adjacent[1]]
            #print((x,y),adjacent, adjacent_val, chr(adjacent_val))
            if adjacent_val == 0: # Walls
                continue
            elif adjacent_val == 1: # Empty space
                new_node = (*adjacent,keys)
            elif (65 <= adjacent_val <= 90): # Doors
                key_bits = bin(keys)[2:].ljust(27, '0') # convert keys value to a bit string of length 27 (=1 + 26 bits), including trailing zeroes
                if key_bits[26 - (adjacent_val - 65)] == '1': # has key to open door
                    new_node = (*adjacent,keys)
                else: # hits a door with no key, cannot pass
                    continue
            elif (97 <= adjacent_val <= 122): # found a key
                new_keys = set_bit(keys, adjacent_val - 97) # set i_th bit to 1 from right to left
                new_node = (*adjacent,new_keys)
            
            if(new_node not in visited):
                visited.create_node(new_node, new_node, parent = current_node)
                bfs_queue.append(new_node)

            if(new_node[2] == all_keys):
                all_keys_found = True
                break
    ending_pos = (new_node[0], new_node[1])
    ending_key = chr(maze[new_node[0]][new_node[1]])
    print('Starting position: {}'.format(robot))
    print('Ending position: {}. Last key found: {}'.format(ending_pos, ending_key))
    return visited.depth(new_node)

def part2(input):
    all_keys, robot, maze = input
    nrows, ncol = maze.shape
    # Split vault into 4 vaults with 4 robots
    #print(all_keys, robot)
    x,y = robot
    robots = [(x-1,y-1),(x+1,y-1),(x+1,y+1),(x-1,y+1)]
    #print(robots)
    for r in robots:
        maze[r[0]][r[1]] = 1
    for t in [robot,(x,y+1),(x,y-1),(x+1,y),(x-1,y)]:
        maze[t[0]][t[1]] = 0

    robots = tuple(robots)
    #visited = treelib.Tree()
    #visited.create_node((robots,INIT_KEY),(robots,INIT_KEY))
    visited = {(robots,INIT_KEY):0}
    bfs_queue = deque([(robots,INIT_KEY)])
    all_keys_found = False
    #visited.show()
    #print(bfs_queue)
    #adjacents = []


    # current_robots = robots
    # adjacents = []
    # for i,r in enumerate(current_robots):
    #     l1 = list(current_robots)
    #     x,y = r
    #     for new_pos in [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]:
    #         l2 = l1.copy()
    #         l2[i] = new_pos
    #         adjacents.append(tuple(l2))
    # for i,adjacent in enumerate(adjacents):
    #     j = i // 4
    #     x,y = adjacent[j]
    #     print(x,y)

    # for a in adjacents:
    #     print(a)
    # print(len(adjacents))
    # exit()

    while(len(bfs_queue) > 0 and not(all_keys_found)):
        #progress tracking
        l = len(bfs_queue)
        if(l%1000 == 0):
            print('Queue length: {:,}. Visited: {:,}'.format(l, len(visited)))

        current_node = bfs_queue.popleft()
        current_robots,keys = current_node

        adjacents = [] # at each state, each robot can possibly move 4 directions => 16 adjacents for each node
        for i,r in enumerate(current_robots):
            l1 = list(current_robots)
            x,y = r
            for new_pos in [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]:
                l2 = l1.copy()
                l2[i] = new_pos
                adjacents.append(tuple(l2))

        for i,adjacent in enumerate(adjacents):
            j = i // 4
            x,y = adjacent[j]
            if(x < 0 or y < 0 or x >= nrows or y>=ncol): # out of bound
                continue
            adjacent_val = maze[x][y]
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
                #visited.create_node(new_node, new_node, parent = current_node)
                visited[new_node] = visited[current_node] + 1
                bfs_queue.append(new_node)

            if(new_node[1] == all_keys):
                all_keys_found = True
                break
    #return visited.depth(new_node)
    return visited[new_node]

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