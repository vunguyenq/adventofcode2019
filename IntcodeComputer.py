# Intcode computer class, shared by multiple day challenges
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
    
    # Parse intcode program and initialize memory
    def parse_input_string(self, input_string):
        input_lst = list(map(int,input_string.split(',')))
        input_dict = {}
        for i, val in enumerate(input_lst):
            input_dict[i] = val
        self.init_memory(input_dict)

    # Reset computer with a new memory
    def reset(self, mem):
        self.__init__()
        self.init_memory(mem)

    # Take ASCII input command. Command terminated with a new linea
    def ascii_command(self, cmd):
        if(cmd[-1] != '\n'): cmd += '\n'
        for c in cmd:
            self.set_input(ord(c))
            self.run_until_input()