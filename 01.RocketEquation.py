exec_part = 1 # which part to execute
exec_test_case = 1 # 1 = test input; 0 = real puzzle input
INPUT_TEST = '''12'''
INPUT = '''
'''
def parse_input(input):
    return input.split('\n')

def part1():
    result = 0
    return result

def part2():
    result = 0
    return result

if __name__ == "__main__":
    if(exec_test_case == 1):
        input = INPUT_TEST
    else:
        input = INPUT

    if (exec_part == 1):
        a = parse_input(input)
        print(a)
        result = part1()
    else:
        result = part2()
    print('Part {} answer: {}'.format(exec_part, result))