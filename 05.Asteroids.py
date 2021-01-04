import datetime
exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
INPUT_TEST = '''3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'''
INPUT = '''3,225,1,225,6,6,1100,1,238,225,104,0,1102,35,92,225,1101,25,55,225,1102,47,36,225,1102,17,35,225,1,165,18,224,1001,224,-106,224,4,224,102,8,223,223,1001,224,3,224,1,223,224,223,1101,68,23,224,101,-91,224,224,4,224,102,8,223,223,101,1,224,224,1,223,224,223,2,217,13,224,1001,224,-1890,224,4,224,102,8,223,223,1001,224,6,224,1,224,223,223,1102,69,77,224,1001,224,-5313,224,4,224,1002,223,8,223,101,2,224,224,1,224,223,223,102,50,22,224,101,-1800,224,224,4,224,1002,223,8,223,1001,224,5,224,1,224,223,223,1102,89,32,225,1001,26,60,224,1001,224,-95,224,4,224,102,8,223,223,101,2,224,224,1,223,224,223,1102,51,79,225,1102,65,30,225,1002,170,86,224,101,-2580,224,224,4,224,102,8,223,223,1001,224,6,224,1,223,224,223,101,39,139,224,1001,224,-128,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,54,93,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,677,224,1002,223,2,223,1005,224,329,101,1,223,223,7,677,677,224,102,2,223,223,1006,224,344,101,1,223,223,108,677,677,224,1002,223,2,223,1006,224,359,1001,223,1,223,7,677,226,224,1002,223,2,223,1005,224,374,1001,223,1,223,1107,677,226,224,1002,223,2,223,1005,224,389,1001,223,1,223,107,226,677,224,102,2,223,223,1005,224,404,1001,223,1,223,1108,226,677,224,1002,223,2,223,1006,224,419,101,1,223,223,107,226,226,224,102,2,223,223,1005,224,434,1001,223,1,223,108,677,226,224,1002,223,2,223,1006,224,449,101,1,223,223,108,226,226,224,102,2,223,223,1006,224,464,1001,223,1,223,1007,226,226,224,1002,223,2,223,1005,224,479,101,1,223,223,8,677,226,224,1002,223,2,223,1006,224,494,101,1,223,223,1007,226,677,224,102,2,223,223,1006,224,509,101,1,223,223,7,226,677,224,1002,223,2,223,1005,224,524,101,1,223,223,107,677,677,224,102,2,223,223,1005,224,539,101,1,223,223,1008,677,226,224,1002,223,2,223,1005,224,554,1001,223,1,223,1008,226,226,224,1002,223,2,223,1006,224,569,1001,223,1,223,1108,226,226,224,102,2,223,223,1005,224,584,101,1,223,223,1107,226,677,224,1002,223,2,223,1005,224,599,1001,223,1,223,8,226,677,224,1002,223,2,223,1006,224,614,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,629,1001,223,1,223,8,226,226,224,1002,223,2,223,1005,224,644,1001,223,1,223,1107,677,677,224,1002,223,2,223,1005,224,659,1001,223,1,223,1007,677,677,224,1002,223,2,223,1005,224,674,101,1,223,223,4,223,99,226'''

def parse_input(input):
    return list(map(int,input.split(',')))

def read_param(mem, param_mode, param_val):
    if(param_mode == 0): # position mode
        return mem[param_val] 
    return param_val # immediate mode

def part1(input):
    i = 0
    output = 0
    input_val = 0
    while i < len(input):
        instruction = input[i]
        cmd = instruction % 100
        param1_mode = (instruction // 100) % 10
        param2_mode = (instruction // 1000) % 10
        param3_mode = (instruction // 10000) % 10
        if  (cmd==1): # Add
            param_1 = read_param(input, param1_mode, input[i+1])
            param_2 = read_param(input, param2_mode, input[i+2])
            param_3 = input[i+3]
            input[param_3] = param_1 + param_2
            i+=4
        elif (cmd==2): # Multiply
            param_1 = read_param(input, param1_mode, input[i+1])
            param_2 = read_param(input, param2_mode, input[i+2])
            param_3 = input[i+3]
            input[param_3] = param_1 * param_2
            i+=4
        elif (cmd==3): # Input
            input[input[i+1]] = input_val
            i+=2
        elif (cmd==4): # 0utput
            output = read_param(input, param1_mode, input[i+1])
            print('Position: {}, output: {}'.format(i, output))
            i+=2
        else: # cmd == 99 - Terminate
            break
    return output

def part2(input):
    i = 0
    output = 0
    input_val = 5
    while i < len(input):
        instruction = input[i]
        cmd = instruction % 100
        param1_mode = (instruction // 100) % 10
        param2_mode = (instruction // 1000) % 10
        param3_mode = (instruction // 10000) % 10
        #print(i,cmd)
        if  (cmd==1): # Add
            param_1 = read_param(input, param1_mode, input[i+1])
            param_2 = read_param(input, param2_mode, input[i+2])
            param_3 = input[i+3]
            input[param_3] = param_1 + param_2
            i+=4
        elif (cmd==2): # Multiply
            param_1 = read_param(input, param1_mode, input[i+1])
            param_2 = read_param(input, param2_mode, input[i+2])
            param_3 = input[i+3]
            input[param_3] = param_1 * param_2
            i+=4
        elif (cmd==3): # Input
            input[input[i+1]] = input_val
            i+=2
        elif (cmd==4): # 0utput
            output = read_param(input, param1_mode, input[i+1])
            print('Position: {}, output: {}'.format(i, output))
            i+=2
        elif (cmd == 5): # Jump-if-true
            param_1 = read_param(input, param1_mode, input[i+1])
            param_2 = read_param(input, param2_mode, input[i+2])
            if(param_1 != 0): # jump
                i = param_2
            else: # no jump, skip 2 params & proceed to next instruction
                i += 3
        elif (cmd == 6): # Jump-if-false
            param_1 = read_param(input, param1_mode, input[i+1])
            param_2 = read_param(input, param2_mode, input[i+2])
            if(param_1 == 0):
                i = param_2
            else: # no jump, skip 2 params & proceed to next instruction
                i += 3
        elif (cmd == 7): # Less than
            param_1 = read_param(input, param1_mode, input[i+1])
            param_2 = read_param(input, param2_mode, input[i+2])
            param_3 = input[i+3]
            if(param_1 < param_2):
                input[param_3] = 1
            else:
                input[param_3] = 0
            i += 4
        elif (cmd == 8): # Equals
            param_1 = read_param(input, param1_mode, input[i+1])
            param_2 = read_param(input, param2_mode, input[i+2])
            param_3 = input[i+3]
            if(param_1 == param_2):
                input[param_3] = 1
            else:
                input[param_3] = 0
            i += 4
        else: # cmd == 99 - Terminate
            break
    return output

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