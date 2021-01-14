import datetime
import time
from IntcodeComputer import IntcodeComputer
import numpy as np
import pygame
import networkx as nx

# Graphic constants
VISUALIZE = True 
TILE_SIZE = 20 # 20x20 pixels
LEFT_MARGIN = 500
TOP_MARGIN = 500
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)

exec_part = 1 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
INPUT_TEST = '''
'''
INPUT = '''3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,1002,1034,1,1039,102,1,1036,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1106,0,124,1002,1034,1,1039,101,0,1036,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1105,1,124,1001,1034,-1,1039,1008,1036,0,1041,102,1,1035,1040,1002,1038,1,1043,1002,1037,1,1042,1106,0,124,1001,1034,1,1039,1008,1036,0,1041,1002,1035,1,1040,101,0,1038,1043,1002,1037,1,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,9,1032,1006,1032,165,1008,1040,3,1032,1006,1032,165,1102,2,1,1044,1105,1,224,2,1041,1043,1032,1006,1032,179,1101,1,0,1044,1106,0,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,29,1044,1105,1,224,1101,0,0,1044,1105,1,224,1006,1044,247,102,1,1039,1034,1002,1040,1,1035,1001,1041,0,1036,1002,1043,1,1038,102,1,1042,1037,4,1044,1106,0,0,19,27,41,9,17,87,2,1,91,14,15,99,17,13,40,13,7,33,23,28,7,21,75,15,41,83,18,4,28,1,21,99,3,2,4,60,16,5,16,22,59,18,37,21,62,96,11,63,46,16,27,76,7,36,38,28,53,18,84,52,12,47,25,93,10,57,64,21,41,75,52,9,80,60,21,86,60,21,70,21,13,72,78,22,61,17,28,54,51,93,18,3,87,21,4,98,17,59,2,17,18,71,5,20,16,39,66,18,7,62,15,37,25,52,27,17,15,10,48,11,39,18,20,68,83,22,36,9,3,69,56,64,21,39,93,1,90,18,57,52,14,41,32,57,5,7,72,18,35,66,21,22,88,2,31,52,7,35,25,50,14,35,7,11,92,38,14,66,3,28,84,18,17,48,15,34,40,4,21,92,52,27,5,4,53,65,59,24,88,24,66,88,85,26,8,26,10,64,99,9,44,38,14,26,74,75,24,31,7,6,62,9,57,75,18,22,52,57,15,3,87,21,39,24,12,8,70,8,19,3,89,16,36,15,36,16,30,28,8,89,12,99,98,16,78,24,11,63,87,55,51,19,57,18,28,9,90,15,95,56,57,1,93,77,24,36,14,44,46,25,66,37,23,8,12,10,58,27,66,4,72,1,2,16,91,16,66,26,24,53,25,20,41,8,75,23,2,20,91,19,3,12,32,30,3,33,85,17,21,92,17,1,12,73,9,34,12,85,42,5,69,67,4,87,70,6,49,96,12,5,37,62,54,72,13,52,14,21,84,68,54,22,78,11,93,12,90,55,7,19,44,21,98,4,46,50,27,30,2,99,27,35,8,5,62,1,91,65,12,80,16,17,81,14,73,60,69,24,23,13,74,57,10,26,21,80,60,10,79,3,9,37,77,73,16,10,3,13,95,4,91,65,11,86,16,24,71,22,6,63,90,56,15,64,8,25,46,77,71,24,13,72,96,22,8,15,79,39,19,19,47,14,16,92,69,73,23,76,23,28,60,84,14,54,62,11,8,30,75,44,16,4,30,82,14,80,11,1,70,85,10,14,73,70,9,54,25,26,12,51,23,86,92,18,11,19,74,55,51,10,73,7,13,43,89,5,55,2,18,82,2,14,63,71,28,7,94,61,10,51,8,53,63,22,39,19,79,20,99,2,66,22,7,68,71,17,19,45,10,14,42,99,9,9,13,75,84,14,83,75,19,92,22,47,4,83,18,46,91,22,61,28,6,71,17,10,1,81,6,60,83,21,14,13,71,11,68,73,52,10,25,30,91,6,25,86,89,19,39,18,95,1,52,23,91,20,14,41,91,26,59,16,85,99,4,15,96,51,19,25,51,73,3,48,79,14,14,41,5,17,59,8,51,43,21,15,47,3,28,53,12,22,23,2,94,74,23,53,20,20,98,21,14,46,61,26,6,55,20,69,28,6,41,19,70,48,6,9,32,32,28,20,21,62,22,38,7,90,3,32,24,92,49,23,72,63,17,18,89,85,33,28,23,27,5,42,52,7,54,18,17,21,63,98,8,9,84,31,24,80,70,22,51,28,61,77,6,25,68,66,8,47,22,7,44,26,37,15,28,68,23,18,18,14,34,3,85,99,31,41,53,28,20,43,90,22,13,70,27,27,17,35,48,11,92,4,60,84,4,38,27,25,89,99,74,2,31,63,13,50,1,54,4,59,3,59,2,54,15,37,19,74,45,75,7,84,19,96,72,75,9,34,18,52,23,99,11,45,81,53,7,71,24,80,26,31,11,74,27,57,0,0,21,21,1,10,1,0,0,0,0,0,0'''

def parse_input(input):
    input_lst = list(map(int,input.split(',')))
    input_dict = {}
    for i, val in enumerate(input_lst):
        input_dict[i] = val
    return input_dict

# Move 1 step
def move(comp, instruction):
    comp.input = instruction
    comp.run_until_input()
    return comp.output

def draw_tile(screen, pos, color):
    x,y = pos
    x = x * TILE_SIZE + LEFT_MARGIN
    y = y * TILE_SIZE + TOP_MARGIN
    pygame.draw.rect(screen, color, [x, y, TILE_SIZE, TILE_SIZE])

def draw_lines(screen, nodes, color):
    for i in range(1,len(nodes)):
        node1 = nodes[i-1]
        node2 = nodes[i]

        x1,y1 = node1
        x2,y2 = node2
        x1 = x1 * TILE_SIZE + int(TILE_SIZE/2) + LEFT_MARGIN
        y1 = y1 * TILE_SIZE + int(TILE_SIZE/2) + TOP_MARGIN
        x2 = x2 * TILE_SIZE + int(TILE_SIZE/2) + LEFT_MARGIN
        y2 = y2 * TILE_SIZE + int(TILE_SIZE/2) + TOP_MARGIN
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 3)

def draw_frame(screen, droid, walls, oxy_pos, font, line_nodes = None):
    # Fill the background with white
    screen.fill((255, 255, 255))
    # Draw walls
    for w in walls:
        draw_tile(screen, w, BLACK)
    # Draw droid
    draw_tile(screen, droid, BLUE)
    # Draw root
    draw_tile(screen, (0,0), RED)
    # Draw oxygen system when found
    if oxy_pos is not None:
        draw_tile(screen, oxy_pos, GREEN)
    # Draw lines if any:
    if line_nodes is not None:
        draw_lines(screen, line_nodes, BLUE)
    # Print droid location
    textsurface = font.render('Droid: {}'.format(droid), False, RED)
    screen.blit(textsurface,(400,10))
    # Refresh display & draw frame
    pygame.display.flip()

    # Exit if user clicks close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    #input("Press Enter to next frame...")
    #time.sleep(0.05)

# https://en.wikipedia.org/wiki/Maze_solving_algorithm#Tr%C3%A9maux's_algorithm
def part1(input_data):
    if(VISUALIZE):
        # Set up the drawing window
        screen = pygame.display.set_mode([1000, 1000])
        pygame.display.set_caption('AoC 2019 Day 15 Part 1 - Maze scanner')
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)

    comp = IntcodeComputer()
    comp.init_memory(input_data)
    output = -1
    droid = np.array((0,0))
    walls = []
    oxy_pos = None
    directions = {1:np.array((0,1)), 2:np.array((0,-1)), 3:np.array((-1,0)), 4:np.array((1,0))}
    opposite_directions = {1:2, 2:1, 3:4, 4:3}
    current_direction = 1
    junctions = {}

    # Initialize graph that holds all movable tiles
    path_graph = nx.Graph()

    # Scan whole maze
    running = True
    while (running):
        droid_loc = tuple(droid)
        available_directions = []
        # Scan surrounding tiles
        for d in directions:
            new_loc = droid + directions[d]    
            output = move(comp, d)
            if (output == 0):
                walls.append(new_loc)
            else:
                #droid = new_loc
                available_directions.append(d)
                if (output == 2):
                    oxy_pos = new_loc.copy()
                move(comp, opposite_directions[d]) # fallback to current tile after scanning
        
        # Check if current tile is a junction
        back = opposite_directions[current_direction]
        if len(available_directions) > 2:
            if droid_loc not in junctions: # junction that was not visited before
                junctions[droid_loc] = {}
                for ad in available_directions:
                    junctions[droid_loc][ad] = 0
            # Mark the direction from which droid came to the junction
            junctions[droid_loc][back] +=1
            # Decide which path to follow
            # Check if there any is direction with 0 mark
            has_zero = False
            for ad in available_directions:
                if junctions[droid_loc][ad] == 0:
                    has_zero = True
                    current_direction = ad
                    junctions[droid_loc][ad] += 1
                    break
            if not(has_zero): # all paths have been marked at least once
                if junctions[droid_loc][back] == 1:
                    current_direction = back
                    junctions[droid_loc][back] += 1
                else:
                    for ad in available_directions:
                        if junctions[droid_loc][ad] == 1:
                            current_direction = ad
                            junctions[droid_loc][ad] += 1
        else: # not a junction
            if len(available_directions) == 1:
                current_direction = available_directions[0]
            else:
                current_direction = [dr for dr in available_directions if dr!=back][0]
        
        # Actually move droid to decided direction
        move(comp, current_direction)
        droid = droid + directions[current_direction]

        # Update path graph
        new_droid_loc = tuple(droid)
        if not(path_graph.has_node(droid_loc)):
            path_graph.add_node(droid_loc)
        if not(path_graph.has_node(new_droid_loc)):
            path_graph.add_node(new_droid_loc)
        if not(path_graph.has_edge(droid_loc, new_droid_loc)):
            path_graph.add_edge(droid_loc, new_droid_loc)

        # Visualize maze scanner
        if(VISUALIZE):
            draw_frame(screen, droid, walls, oxy_pos, myfont)
        if(tuple(droid) == (0,0)):
            break
    
    print('Starting position of repair droid: {}'.format((0,0)))
    print('Location of oxy system: {}'.format(tuple(oxy_pos)))
    oxy_path = nx.shortest_path(path_graph, source=(0,0), target = tuple(oxy_pos))
    if(VISUALIZE):
        draw_frame(screen, (0,0), walls, oxy_pos, myfont, oxy_path)
    print('Shortest path from droid to oxy system: {} nodes (including droid and oxy system)'.format(len(oxy_path)))
    input('Press Enter to continue...')
    return len(oxy_path) - 1

def part2(input_data):
    result = 0
    return result

if __name__ == "__main__":
    if(exec_test_case == 1):
        input_data = INPUT_TEST
    else:
        input_data = INPUT
    input_data = parse_input(input_data)

    start_time = datetime.datetime.now() 
    if (exec_part == 1):
        result = part1(input_data)
    else:
        result = part2(input_data)
    end_time = datetime.datetime.now() 
    print('Part {} time: {}'.format(exec_part, end_time - start_time))
    print('Part {} answer: {}'.format(exec_part, result))