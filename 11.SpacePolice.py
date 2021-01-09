import datetime
exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input
import matplotlib.pyplot as plt

# Puzzle input
INPUT_TEST = '''
'''
INPUT = '''3,8,1005,8,318,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,1002,8,1,28,1,107,14,10,1,107,18,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,58,1006,0,90,2,1006,20,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,88,2,103,2,10,2,4,7,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,118,1,1009,14,10,1,1103,9,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1002,8,1,147,1006,0,59,1,104,4,10,2,106,18,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,181,2,4,17,10,1006,0,36,1,107,7,10,2,1008,0,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,217,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,240,1006,0,64,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,1002,8,1,264,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1001,8,0,287,1,1104,15,10,1,102,8,10,1006,0,2,101,1,9,9,1007,9,940,10,1005,10,15,99,109,640,104,0,104,1,21102,932700857236,1,1,21101,335,0,0,1106,0,439,21101,0,387511792424,1,21101,346,0,0,1106,0,439,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,46372252675,0,1,21102,393,1,0,1106,0,439,21101,97806162983,0,1,21102,404,1,0,1105,1,439,3,10,104,0,104,0,3,10,104,0,104,0,21102,1,825452438376,1,21101,0,427,0,1106,0,439,21102,709475586836,1,1,21101,0,438,0,1106,0,439,99,109,2,22101,0,-1,1,21101,40,0,2,21102,1,470,3,21102,1,460,0,1106,0,503,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,465,466,481,4,0,1001,465,1,465,108,4,465,10,1006,10,497,1101,0,0,465,109,-2,2105,1,0,0,109,4,2102,1,-1,502,1207,-3,0,10,1006,10,520,21102,1,0,-3,21202,-3,1,1,21202,-2,1,2,21101,0,1,3,21101,0,539,0,1106,0,544,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,567,2207,-4,-2,10,1006,10,567,22101,0,-4,-4,1106,0,635,21202,-4,1,1,21201,-3,-1,2,21202,-2,2,3,21102,586,1,0,1105,1,544,22101,0,1,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,605,21102,0,1,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,627,22101,0,-1,1,21102,1,627,0,106,0,502,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0'''

# Intcode computer class, taken from Day 09
# Change: Added attribute outputs to hold all outputs since computer is initialized
class IntcodeComputer:
    def __init__(self):
        self.mem = {}
        self.pointer = 0 # current instruction pointer
        self.input = None 
        self.output = None # result of the latest Output instruction
        self.outputs = []
        self.finished = False # track if all instructions in memory has been executed
        self.relative_base = 0
    
    def init_memory(self, mem):
        self.mem = mem.copy()

    def set_input(self, new_input):
        self.input = new_input

    # Read parameter of an instruction in position, immediate or relative mode
    def read_param(self, param_mode, param_val):
        if(param_mode == 0): # position mode
            if param_val not in self.mem: # memory slot has NOT been initialized. Initialize it with 0
                self.mem[param_val] = 0
            return self.mem[param_val]
        if (param_mode == 2): # relative mode
            pos = self.relative_base + param_val
            if pos not in self.mem:
                self.mem[pos] = 0
            return self.mem[pos]
        return param_val # immediate mode

    # Identify memory location to write for instructions 1,2,3,7,8 
    def write_param(self, param_mode, param_val):
        if(param_mode == 0): # write to absolute position
            write_pos = param_val
        elif(param_mode == 2): # write to relative position
            write_pos = self.relative_base + param_val
        else: # immediate mode - invalide
            print('Input instruction does NOT support immediate mode')
            return None
        return write_pos

    # Run instruction at the current pointer. Code taken from Day 5 Part 2
    def run_instruction(self):
        if self.pointer >= len(self.mem):
            return None
        
        instruction = self.mem[self.pointer]
        cmd = instruction % 100
        param1_mode = (instruction // 100) % 10
        param2_mode = (instruction // 1000) % 10
        param3_mode = (instruction // 10000) % 10
        if  (cmd==1): # Add
            param_1 = self.read_param(param1_mode, self.mem[self.pointer+1])
            param_2 = self.read_param(param2_mode, self.mem[self.pointer+2])
            param_3 = self.mem[self.pointer+3]
            write_pos = self.write_param(param3_mode, param_3)
            self.mem[write_pos] = param_1 + param_2
            self.pointer+=4
        elif (cmd==2): # Multiply
            param_1 = self.read_param(param1_mode, self.mem[self.pointer+1])
            param_2 = self.read_param(param2_mode, self.mem[self.pointer+2])
            param_3 = self.mem[self.pointer+3]
            write_pos = self.write_param(param3_mode, param_3)
            self.mem[write_pos] = param_1 * param_2
            self.pointer+=4
        elif (cmd==3): # Input
            if(self.input is None):
                return 98 # Special return code to notify that computer pauses because of no input
            param1 = self.mem[self.pointer+1]
            write_pos = self.write_param(param1_mode, param1)
            self.mem[write_pos] = self.input
            self.pointer+=2
            self.input = None
        elif (cmd==4): # 0utput
            self.output = self.read_param(param1_mode, self.mem[self.pointer+1])
            self.outputs.append(self.output)
            #print('Position: {}, output: {}'.format(self.pointer, self.output))
            self.pointer+=2
        elif (cmd == 5): # Jump-if-true
            param_1 = self.read_param(param1_mode, self.mem[self.pointer+1])
            param_2 = self.read_param(param2_mode, self.mem[self.pointer+2])
            if(param_1 != 0): # jump
                self.pointer = param_2
            else: # no jump, skip 2 params & proceed to next instruction
                self.pointer += 3
        elif (cmd == 6): # Jump-if-false
            param_1 = self.read_param(param1_mode, self.mem[self.pointer+1])
            param_2 = self.read_param(param2_mode, self.mem[self.pointer+2])
            if(param_1 == 0):
                self.pointer = param_2
            else: # no jump, skip 2 params & proceed to next instruction
                self.pointer += 3
        elif (cmd == 7): # Less than
            param_1 = self.read_param(param1_mode, self.mem[self.pointer+1])
            param_2 = self.read_param(param2_mode, self.mem[self.pointer+2])
            param_3 = self.mem[self.pointer+3]
            write_pos = self.write_param(param3_mode, param_3)
            if(param_1 < param_2):
                self.mem[write_pos] = 1
            else:
                self.mem[write_pos] = 0
            self.pointer += 4
        elif (cmd == 8): # Equals
            param_1 = self.read_param(param1_mode, self.mem[self.pointer+1])
            param_2 = self.read_param(param2_mode, self.mem[self.pointer+2])
            param_3 = self.mem[self.pointer+3]
            write_pos = self.write_param(param3_mode, param_3)
            if(param_1 == param_2):
                self.mem[write_pos] = 1
            else:
                self.mem[write_pos] = 0
            self.pointer += 4
        elif (cmd == 9): # Modify relative base
            param_1 = self.read_param(param1_mode, self.mem[self.pointer+1])
            self.relative_base += param_1
            self.pointer+=2
        else: # cmd == 99 - Terminate
            self.finished = True
        return cmd
    
    # Run instructions one by one until it reaches an Input command
    # At an Input command, if self.input is None, computer pauses execution
    def run_until_input(self):
        while(True):
            cmd = self.run_instruction()
            if (cmd == 98):
                break
            if (cmd == 99):
                self.finished = True
                break

def parse_input(input):
    input_lst = list(map(int,input.split(',')))
    input_dict = {}
    for i, val in enumerate(input_lst):
        input_dict[i] = val
    return input_dict

# Same painting function for part1 and part2
def paint_panels(input, start_panel):
    comp = IntcodeComputer()
    comp.init_memory(input)
    pos = (0,0)
    direction = (0,1) # up
    visited = {(0,0):start_panel}
    while (not comp.finished): 
        current_panel = visited[pos]    
        comp.set_input(current_panel)
        comp.run_until_input()
        paint, turn = comp.outputs[-2], comp.outputs[-1]

        # Paint current panel according to 1st output
        visited[pos] = paint 
        # Change direction according to 2nd output
        x, y = direction
        if(turn) == 0: # Turn left: vector (x, y) rotated 90 degrees counter clockwise around (0, 0) is (-y, x)        
            direction = (-y,x)
        else: # Turn right: vector (x, y) rotated 90 degrees clockwise around (0, 0) is (y, -x)
            direction = (y,-x)
        # Move robot 
        pos = (pos[0] + direction[0], pos[1] + direction[1])
        if not(pos in visited):
            visited[pos] = 0
    return visited

def part1(input):
    visited = paint_panels(input, 0)
    # Just for fun Part 1 - plot black & white panels
    whites = [p for p in visited if visited[p] == 1]
    plt.scatter(*zip(*whites), color='blue')
    plt.show()
    return len(visited)

def part2(input):
    visited = paint_panels(input, 1)
    # Plot white panels
    whites = [p for p in visited if visited[p] == 1]
    plt.scatter(*zip(*whites), color='blue')
    plt.show()
    return 0

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