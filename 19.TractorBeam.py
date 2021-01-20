import datetime
from IntcodeComputer import IntcodeComputer
import matplotlib.pyplot as plt
exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
INPUT_TEST = '''
'''
INPUT = '''109,424,203,1,21102,11,1,0,1106,0,282,21102,18,1,0,1105,1,259,1202,1,1,221,203,1,21102,31,1,0,1106,0,282,21101,38,0,0,1106,0,259,21002,23,1,2,22102,1,1,3,21102,1,1,1,21102,1,57,0,1105,1,303,2101,0,1,222,21002,221,1,3,20101,0,221,2,21101,0,259,1,21102,1,80,0,1105,1,225,21102,1,8,2,21101,91,0,0,1106,0,303,1202,1,1,223,21002,222,1,4,21102,1,259,3,21101,225,0,2,21101,225,0,1,21101,0,118,0,1105,1,225,21001,222,0,3,21101,0,48,2,21102,133,1,0,1106,0,303,21202,1,-1,1,22001,223,1,1,21102,1,148,0,1105,1,259,1201,1,0,223,20101,0,221,4,21001,222,0,3,21101,0,6,2,1001,132,-2,224,1002,224,2,224,1001,224,3,224,1002,132,-1,132,1,224,132,224,21001,224,1,1,21102,1,195,0,105,1,108,20207,1,223,2,21001,23,0,1,21101,-1,0,3,21101,0,214,0,1105,1,303,22101,1,1,1,204,1,99,0,0,0,0,109,5,2101,0,-4,249,21201,-3,0,1,22102,1,-2,2,21202,-1,1,3,21102,1,250,0,1106,0,225,21201,1,0,-4,109,-5,2106,0,0,109,3,22107,0,-2,-1,21202,-1,2,-1,21201,-1,-1,-1,22202,-1,-2,-2,109,-3,2106,0,0,109,3,21207,-2,0,-1,1206,-1,294,104,0,99,22101,0,-2,-2,109,-3,2106,0,0,109,5,22207,-3,-4,-1,1206,-1,346,22201,-4,-3,-4,21202,-3,-1,-1,22201,-4,-1,2,21202,2,-1,-1,22201,-4,-1,1,22102,1,-2,3,21101,0,343,0,1105,1,303,1105,1,415,22207,-2,-3,-1,1206,-1,387,22201,-3,-2,-3,21202,-2,-1,-1,22201,-3,-1,3,21202,3,-1,-1,22201,-3,-1,2,22101,0,-4,1,21101,384,0,0,1106,0,303,1106,0,415,21202,-4,-1,-4,22201,-4,-3,-4,22202,-3,-2,-2,22202,-2,-4,-4,22202,-3,-2,-3,21202,-4,-1,-2,22201,-3,-2,1,21201,1,0,-4,109,-5,2106,0,0'''

def scan_point(comp, mem, x, y):
    comp.reset(mem) # Intcode program terminates after each run, need to reset 
    comp.input = x
    comp.run_until_input()
    comp.input = y
    comp.run_until_input()
    return comp.output

def part1(input):
    comp = IntcodeComputer()
    comp.parse_input_string(input)
    mem = comp.mem
    affected_count = 0
    for i in range(50):
        for j in range(50):
            affected_count += scan_point(comp, mem, i, j)
    return affected_count

def part2(input):
    comp = IntcodeComputer()
    comp.parse_input_string(input)
    mem = comp.mem
    x, y = 5, 2 # From part 1: y=1 is an empty row. (5,2) is the first point after (0,0)
    square_size = 100 - 1
    
    while(True):
        # Progress tracking
        if(y%50 == 0):
            print('Trying y = {}, x = {} ...'.format(y,x))

        out = scan_point(comp, mem, x, y)
        if(out == 0):
            x += 1
        else:
            xs = x
            while(True):
                top_right = (xs + square_size, y)
                bottom_left = (xs, y + square_size)
                if(scan_point(comp, mem, *top_right) == 0):
                    y += 1
                    x = xs
                    break
                if(scan_point(comp, mem, *bottom_left) == 0):
                    xs += 1
                else: # square fits into the beam
                    print('Square {} x {} fits into the beam. Top left corner: {}'.format(square_size + 1, square_size + 1, (xs,y)))
                    return xs * 10000 + y
    return 0        

if __name__ == "__main__":
    if(exec_test_case == 1):
        input = INPUT_TEST
    else:
        input = INPUT

    start_time = datetime.datetime.now() 
    if (exec_part == 1):
        result = part1(input)
    else:
        result = part2(input)
    end_time = datetime.datetime.now() 
    print('Part {} time: {}'.format(exec_part, end_time - start_time))
    print('Part {} answer: {}'.format(exec_part, result))