import datetime
from itertools import permutations
exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
INPUT_TEST = '''3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'''
INPUT = '''3,8,1001,8,10,8,105,1,0,0,21,46,55,76,89,106,187,268,349,430,99999,3,9,101,4,9,9,1002,9,2,9,101,5,9,9,1002,9,2,9,101,2,9,9,4,9,99,3,9,1002,9,5,9,4,9,99,3,9,1001,9,2,9,1002,9,4,9,101,2,9,9,1002,9,3,9,4,9,99,3,9,1001,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,4,9,1001,9,4,9,102,5,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,99'''

# In this problem, there are 5 amplifiers/ Intcode computers, each with its own memory, instruction pointer and execution status
# Therefore Intcode computer should be implemented as an object
class IntcodeComputer:
    def __init__(self):
        self.mem = []
        self.pointer = 0 # current instruction pointer
        self.input = None 
        self.output = None # result of the latest Output instruction
        self.finished = False # track if all instructions in memory has been executed
    
    def init_memory(self, mem):
        self.mem = mem.copy()

    def set_input(self, new_input):
        self.input = new_input

    def read_param(self, param_mode, param_val):
        if(param_mode == 0): # position mode
            return self.mem[param_val] 
        return param_val # immediate mode

    # Run instruction at the current pointer. Code taken from Day 5 Part 2
    def run_instruction(self):
        if self.pointer >= len(self.mem):
            return None
        
        instruction = self.mem[self.pointer]
        cmd = instruction % 100
        param1_mode = (instruction // 100) % 10
        param2_mode = (instruction // 1000) % 10
        if  (cmd==1): # Add
            param_1 = self.read_param(param1_mode, self.mem[self.pointer+1])
            param_2 = self.read_param(param2_mode, self.mem[self.pointer+2])
            param_3 = self.mem[self.pointer+3]
            self.mem[param_3] = param_1 + param_2
            self.pointer+=4
        elif (cmd==2): # Multiply
            param_1 = self.read_param(param1_mode, self.mem[self.pointer+1])
            param_2 = self.read_param(param2_mode, self.mem[self.pointer+2])
            param_3 = self.mem[self.pointer+3]
            self.mem[param_3] = param_1 * param_2
            self.pointer+=4
        elif (cmd==3): # Input
            if(self.input is None):
                return 98 # Special return code to notify that computer pauses because of no input
            self.mem[self.mem[self.pointer+1]] = self.input
            self.pointer+=2
            self.input = None
        elif (cmd==4): # 0utput
            self.output = self.read_param(param1_mode, self.mem[self.pointer+1])
            #print('Position: {}, output: {}'.format(i, output))
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
            if(param_1 < param_2):
                self.mem[param_3] = 1
            else:
                self.mem[param_3] = 0
            self.pointer += 4
        elif (cmd == 8): # Equals
            param_1 = self.read_param(param1_mode, self.mem[self.pointer+1])
            param_2 = self.read_param(param2_mode, self.mem[self.pointer+2])
            param_3 = self.mem[self.pointer+3]
            if(param_1 == param_2):
                self.mem[param_3] = 1
            else:
                self.mem[param_3] = 0
            self.pointer += 4
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
    return list(map(int,input.split(',')))

# create an amplifier, initialize 1st input and run instructions until next input instruction
def create_computer(mem, input):
    comp = IntcodeComputer()
    comp.init_memory(mem)
    comp.set_input(input)
    comp.run_until_input()
    return comp

# set input to an amplifier and run until next input instruction
def next_input(comp, input):
    comp.set_input(input)
    comp.run_until_input()

def part1(input):
    # Generate 120 combinations of phase settings
    phase_combs = list(permutations([0,1,2,3,4])) 
    max_out = 0
    #phase_combs=[(0,1,2,3,4)]
    for phase in phase_combs:
        comp1 = create_computer(input,phase[0])
        comp2 = create_computer(input,phase[1])
        comp3 = create_computer(input,phase[2])
        comp4 = create_computer(input,phase[3])
        comp5 = create_computer(input,phase[4])

        next_input(comp1,0)
        next_input(comp2, comp1.output)
        next_input(comp3, comp2.output)
        next_input(comp4, comp3.output)
        next_input(comp5, comp4.output)
        
        max_out = max(max_out, comp5.output)
    return max_out

def part2(input):
    # Generate 120 combinations of phase settings
    phase_combs = list(permutations([5,6,7,8,9])) 
    max_out = 0
    #phase_combs=[(9,8,7,6,5)]
    for phase in phase_combs:
        comp1 = create_computer(input,phase[0])
        comp2 = create_computer(input,phase[1])
        comp3 = create_computer(input,phase[2])
        comp4 = create_computer(input,phase[3])
        comp5 = create_computer(input,phase[4])

        comp5_out = 0
        while(True):
            next_input(comp1, comp5_out)
            next_input(comp2, comp1.output)
            next_input(comp3, comp2.output)
            next_input(comp4, comp3.output)
            next_input(comp5, comp4.output)
            comp5_out = comp5.output
            if comp5.finished == True:
                break
        max_out = max(max_out, comp5_out)
    return max_out

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