import datetime
exec_part = 2 # which part to execute
exec_test_case = 1 # 1 = test input; 0 = real puzzle input

# Puzzle input
INPUT_TEST = '''206938-679128'''
INPUT = '''206938-679128'''

def parse_input(input):
    return list(map(int,input.split('-')))

def check_valid_pwd(num):
    digits = list(map(int,str(num)))
    contain_adjacent = False
    for i in range(1,len(digits)):
        if digits[i] < digits[i-1]:
            return False
        if digits[i] == digits[i-1]:
            contain_adjacent = True
    return contain_adjacent

# similar to password check in part1, but now repeated digits must be exactly 2 digit long
def check_valid_pwd_p2(num):
    digits = list(map(int,str(num)))
    contain_adjacent = False
    adjacent_count = 1
    for i in range(1,len(digits)):
        if digits[i] < digits[i-1]:
            return False

    digits.append('a') # append an extra character to the end of password to check if 2 last digits are same
    for i in range(1,len(digits)):
        if digits[i] == digits[i-1]:
            adjacent_count += 1
        else: 
            if(adjacent_count == 2):
                contain_adjacent = True
                break
            else:
                adjacent_count = 1
    return contain_adjacent

def part1(input):
    valid_count = 0
    for num in range(input[0], input[1]+1):
        if(check_valid_pwd(num)):
            valid_count += 1
    return valid_count

def part2(input):
    valid_count = 0
    for num in range(input[0], input[1]+1):
        if(check_valid_pwd_p2(num)):
            valid_count += 1
    return valid_count

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