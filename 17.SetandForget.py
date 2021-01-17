import datetime
from IntcodeComputer import IntcodeComputer
import numpy as np

exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
INPUT_TEST = '''
'''
INPUT = '''1,330,331,332,109,4014,1101,1182,0,15,1102,1,1429,24,1001,0,0,570,1006,570,36,1002,571,1,0,1001,570,-1,570,1001,24,1,24,1106,0,18,1008,571,0,571,1001,15,1,15,1008,15,1429,570,1006,570,14,21101,58,0,0,1106,0,786,1006,332,62,99,21101,333,0,1,21101,0,73,0,1106,0,579,1101,0,0,572,1102,1,0,573,3,574,101,1,573,573,1007,574,65,570,1005,570,151,107,67,574,570,1005,570,151,1001,574,-64,574,1002,574,-1,574,1001,572,1,572,1007,572,11,570,1006,570,165,101,1182,572,127,1001,574,0,0,3,574,101,1,573,573,1008,574,10,570,1005,570,189,1008,574,44,570,1006,570,158,1105,1,81,21101,0,340,1,1105,1,177,21101,0,477,1,1105,1,177,21101,514,0,1,21102,176,1,0,1106,0,579,99,21102,1,184,0,1105,1,579,4,574,104,10,99,1007,573,22,570,1006,570,165,102,1,572,1182,21101,375,0,1,21101,211,0,0,1106,0,579,21101,1182,11,1,21102,222,1,0,1105,1,979,21101,0,388,1,21102,1,233,0,1105,1,579,21101,1182,22,1,21102,1,244,0,1106,0,979,21101,401,0,1,21101,255,0,0,1106,0,579,21101,1182,33,1,21102,1,266,0,1106,0,979,21102,1,414,1,21102,277,1,0,1106,0,579,3,575,1008,575,89,570,1008,575,121,575,1,575,570,575,3,574,1008,574,10,570,1006,570,291,104,10,21101,0,1182,1,21102,1,313,0,1105,1,622,1005,575,327,1102,1,1,575,21102,1,327,0,1106,0,786,4,438,99,0,1,1,6,77,97,105,110,58,10,33,10,69,120,112,101,99,116,101,100,32,102,117,110,99,116,105,111,110,32,110,97,109,101,32,98,117,116,32,103,111,116,58,32,0,12,70,117,110,99,116,105,111,110,32,65,58,10,12,70,117,110,99,116,105,111,110,32,66,58,10,12,70,117,110,99,116,105,111,110,32,67,58,10,23,67,111,110,116,105,110,117,111,117,115,32,118,105,100,101,111,32,102,101,101,100,63,10,0,37,10,69,120,112,101,99,116,101,100,32,82,44,32,76,44,32,111,114,32,100,105,115,116,97,110,99,101,32,98,117,116,32,103,111,116,58,32,36,10,69,120,112,101,99,116,101,100,32,99,111,109,109,97,32,111,114,32,110,101,119,108,105,110,101,32,98,117,116,32,103,111,116,58,32,43,10,68,101,102,105,110,105,116,105,111,110,115,32,109,97,121,32,98,101,32,97,116,32,109,111,115,116,32,50,48,32,99,104,97,114,97,99,116,101,114,115,33,10,94,62,118,60,0,1,0,-1,-1,0,1,0,0,0,0,0,0,1,18,18,0,109,4,2101,0,-3,586,21001,0,0,-1,22101,1,-3,-3,21101,0,0,-2,2208,-2,-1,570,1005,570,617,2201,-3,-2,609,4,0,21201,-2,1,-2,1105,1,597,109,-4,2106,0,0,109,5,1201,-4,0,630,20102,1,0,-2,22101,1,-4,-4,21102,1,0,-3,2208,-3,-2,570,1005,570,781,2201,-4,-3,653,20102,1,0,-1,1208,-1,-4,570,1005,570,709,1208,-1,-5,570,1005,570,734,1207,-1,0,570,1005,570,759,1206,-1,774,1001,578,562,684,1,0,576,576,1001,578,566,692,1,0,577,577,21102,1,702,0,1106,0,786,21201,-1,-1,-1,1105,1,676,1001,578,1,578,1008,578,4,570,1006,570,724,1001,578,-4,578,21101,731,0,0,1105,1,786,1105,1,774,1001,578,-1,578,1008,578,-1,570,1006,570,749,1001,578,4,578,21102,756,1,0,1106,0,786,1106,0,774,21202,-1,-11,1,22101,1182,1,1,21101,0,774,0,1105,1,622,21201,-3,1,-3,1106,0,640,109,-5,2106,0,0,109,7,1005,575,802,21002,576,1,-6,20101,0,577,-5,1105,1,814,21101,0,0,-1,21102,1,0,-5,21101,0,0,-6,20208,-6,576,-2,208,-5,577,570,22002,570,-2,-2,21202,-5,47,-3,22201,-6,-3,-3,22101,1429,-3,-3,2101,0,-3,843,1005,0,863,21202,-2,42,-4,22101,46,-4,-4,1206,-2,924,21102,1,1,-1,1106,0,924,1205,-2,873,21102,1,35,-4,1105,1,924,1202,-3,1,878,1008,0,1,570,1006,570,916,1001,374,1,374,2102,1,-3,895,1101,2,0,0,2101,0,-3,902,1001,438,0,438,2202,-6,-5,570,1,570,374,570,1,570,438,438,1001,578,558,921,21002,0,1,-4,1006,575,959,204,-4,22101,1,-6,-6,1208,-6,47,570,1006,570,814,104,10,22101,1,-5,-5,1208,-5,55,570,1006,570,810,104,10,1206,-1,974,99,1206,-1,974,1101,0,1,575,21101,973,0,0,1105,1,786,99,109,-7,2106,0,0,109,6,21101,0,0,-4,21101,0,0,-3,203,-2,22101,1,-3,-3,21208,-2,82,-1,1205,-1,1030,21208,-2,76,-1,1205,-1,1037,21207,-2,48,-1,1205,-1,1124,22107,57,-2,-1,1205,-1,1124,21201,-2,-48,-2,1105,1,1041,21102,-4,1,-2,1105,1,1041,21102,-5,1,-2,21201,-4,1,-4,21207,-4,11,-1,1206,-1,1138,2201,-5,-4,1059,1201,-2,0,0,203,-2,22101,1,-3,-3,21207,-2,48,-1,1205,-1,1107,22107,57,-2,-1,1205,-1,1107,21201,-2,-48,-2,2201,-5,-4,1090,20102,10,0,-1,22201,-2,-1,-2,2201,-5,-4,1103,1202,-2,1,0,1105,1,1060,21208,-2,10,-1,1205,-1,1162,21208,-2,44,-1,1206,-1,1131,1105,1,989,21101,439,0,1,1105,1,1150,21102,1,477,1,1106,0,1150,21101,0,514,1,21102,1,1149,0,1106,0,579,99,21102,1157,1,0,1105,1,579,204,-2,104,10,99,21207,-3,22,-1,1206,-1,1138,1201,-5,0,1176,1201,-4,0,0,109,-6,2105,1,0,14,11,36,1,9,1,36,1,9,1,9,7,20,1,9,1,9,1,5,1,20,1,9,1,9,1,5,1,20,1,9,1,9,1,5,1,20,1,9,1,9,1,5,1,20,1,9,1,9,1,5,1,20,1,9,11,5,1,20,1,25,1,20,11,15,7,24,1,21,1,20,7,19,1,20,1,3,1,1,1,19,1,20,1,3,1,1,1,19,1,20,1,3,1,1,1,19,1,20,1,3,1,1,1,11,9,20,1,3,1,1,1,11,1,26,11,9,1,28,1,3,1,1,1,1,1,9,1,28,1,3,7,7,1,28,1,5,1,1,1,1,1,7,1,18,11,5,11,1,1,18,1,17,1,1,1,5,1,1,1,18,1,17,1,1,1,5,1,1,1,18,1,17,1,1,1,5,1,1,1,18,1,17,11,18,1,19,1,5,1,12,9,19,7,12,1,46,1,46,1,46,1,46,1,46,7,46,1,46,1,46,1,46,1,46,1,46,1,46,1,46,1,46,1,38,9,38,1,46,1,46,1,46,1,46,1,46,1,46,1,46,1,46,1,46,11,36'''

def parse_input(input):
    return input

def part1(input):
    comp = IntcodeComputer()
    comp.parse_input_string(input)
    comp.run_until_input()
    output = comp.outputs
    # Visualize surface
    #layout = ''.join(list(map(str,output))).replace('35','#').replace('46','.').replace('10','\n').replace('94',chr(94))
    #print(layout)
    nodes = []
    x = y = 0
    # Add nodes
    for c in output:
        if (c==46):
            x += 1
        elif (c==10):
            x = 0
            y += 1
        else: # 46 or robot direction, for example 94
            nodes.append((x,y))
            x += 1
    # Count intersections
    align_param = 0
    for n in nodes:
        x,y = n
        neigbor_count = 0
        for neigbor in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            if neigbor in nodes:
                neigbor_count += 1
        if (neigbor_count) > 2:
            align_param += x*y
    return align_param

def ascii_input(comp, input_str):
    if(len(input_str) > 21):
        print('Input string too long: {} characters'.format(len(input_str)))
        return
    for k in [ord(c) for c in input_str]:
        comp.set_input(k)
        comp.run_until_input()
    

def part2(input):
    # Init computer
    comp = IntcodeComputer()
    comp.parse_input_string(input)
    comp.mem[0] = 2 # wake up vaccum robot
    # Run computer for the first time to get scaffold layout & starting position
    comp.run_until_input()
    nodes = []
    x = y = 0

    # Add nodes
    for c in comp.outputs:
        if (c==46):
            x += 1
        elif (c==10):
            x = 0
            y += 1
        elif (c==35): 
            nodes.append((x,y))
            x += 1
        elif (c==94): # robot
            robot = np.array((x,y))
            nodes.append((x,y))
            x += 1
        else:
            continue

    # Print initial scaffold map
    # print(''.join([chr(d) for d in comp.outputs]))
    # print(robot)
    # Find path to visit all scaffolds: Move robot forward, skip all intersections, turn only at corners 
    robot_direction = np.array((0,-1)) # start facing up
    steps = 0
    last_turn = 'R'
    path = []
    while(True):
        x,y = tuple(robot_direction)
        directions = {'F':robot_direction, 'R':np.array((-y,x)), 'L':np.array((y,-x))} # forward, right, left
        dead_end = True
        for d in directions:
            next_step = tuple(robot + directions[d])
            if next_step in nodes:
                robot = next_step
                robot_direction = directions[d]
                dead_end = False
                break
        if(d == 'L' or d == 'R'):
            path.append(last_turn + ',' + str(steps))
            last_turn = d
            steps = 0
        steps += 1    
        if (dead_end):
            break

    print('Location of robot at last scaffold: {}'.format(robot))
    print('Path to visit all scaffolds: {}'.format(path))

    # Break down path manually into 3 functions A,B,C
    func_a = 'R,10,R,8,L,10,L,10\n'
    func_b = 'R,8,L,6,L,6\n'
    func_c = 'L,10,R,10,L,6\n'
    main_routine = 'A,B,B,A,C,B,C,C,B,A\n'
 
    ascii_input(comp, main_routine)
    ascii_input(comp, func_a)
    ascii_input(comp, func_b)
    ascii_input(comp, func_c)
    ascii_input(comp, 'n\n')
    print(''.join([chr(d) for d in comp.outputs]))
    print(comp.output)

    return comp.output

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