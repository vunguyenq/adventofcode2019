exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input
INPUT_TEST = '''1,1,1,4,99,5,6,0,99'''
INPUT = '''1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,19,1,6,19,23,2,6,23,27,1,5,27,31,2,31,9,35,1,35,5,39,1,39,5,43,1,43,10,47,2,6,47,51,1,51,5,55,2,55,6,59,1,5,59,63,2,63,6,67,1,5,67,71,1,71,6,75,2,75,10,79,1,79,5,83,2,83,6,87,1,87,5,91,2,9,91,95,1,95,6,99,2,9,99,103,2,9,103,107,1,5,107,111,1,111,5,115,1,115,13,119,1,13,119,123,2,6,123,127,1,5,127,131,1,9,131,135,1,135,9,139,2,139,6,143,1,143,5,147,2,147,6,151,1,5,151,155,2,6,155,159,1,159,2,163,1,9,163,0,99,2,0,14,0'''
def parse_input(input):
    return list(map(int,input.split(',')))

def part1(input):
    i = 4
    input[1] = 12
    input[2] = 2
    while i <= len(input):
        opcode, pos1, pos2, out = input[i-4:i]
        #print(i, opcode, pos1, pos2, out, input)
        if(opcode == 1):
            input[out] = input[pos1] + input[pos2]
        elif(opcode == 2):
            input[out] = input[pos1] * input[pos2]
        else: #99
            break
        i += 4
    #print(input)
    return input[0]

def part2(input):
    for noun in range(0,100):
        for verb in range(0,100):
            mem = input.copy()
            i = 4
            mem[1] = noun
            mem[2] = verb
            while i <= len(mem):
                opcode, pos1, pos2, out = mem[i-4:i]
                #print(i, opcode, pos1, pos2, out, input)
                if(opcode == 1):
                    mem[out] = mem[pos1] + mem[pos2]
                elif(opcode == 2):
                    mem[out] = mem[pos1] * mem[pos2]
                else: #99
                    break
                i += 4
            if(mem[0] == 19690720):
                print('Found a match at noun = {}, verb = {}, output = {}'.format(noun, verb, mem[0]))
                return 100 * noun + verb
    return 0

if __name__ == "__main__":
    if(exec_test_case == 1):
        input = INPUT_TEST
    else:
        input = INPUT
    input = parse_input(input)
    if (exec_part == 1):
        result = part1(input)
    else:
        result = part2(input)
    print('Part {} answer: {}'.format(exec_part, result))